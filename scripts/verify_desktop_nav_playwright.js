#!/usr/bin/env node
/**
 * Desktop nav regression verifier for Active Oahu Tours.
 *
 * Usage:
 *   node scripts/verify_desktop_nav_playwright.js [baseUrl] [outputJson]
 *
 * Requires Playwright in the invoking environment. The script crawls the visible
 * desktop nav tree, hovers through every submenu path, verifies each nav link is
 * visible/clickable when revealed, checks link HTTP status, and confirms parent
 * menu links are not blocked by desktop dropdown JavaScript.
 */
const { chromium } = require('playwright');
const fs = require('fs');

const baseUrl = (process.argv[2] || 'https://activeoahutours.com/').replace(/\/?$/, '/');
const out = process.argv[3] || '/tmp/aot-desktop-nav-playwright-report.json';
const WIDTH = 1440;
const HEIGHT = 900;

function absUrl(href) {
  return new URL(href, baseUrl).toString();
}

async function main() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: WIDTH, height: HEIGHT }, deviceScaleFactor: 1 });
  const consoleMessages = [];
  page.on('console', msg => consoleMessages.push({ type: msg.type(), text: msg.text() }));
  page.on('pageerror', err => consoleMessages.push({ type: 'pageerror', text: String(err) }));

  async function gotoHome() {
    await page.goto(baseUrl + '?kai_nav_verify=' + Date.now(), { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForLoadState('networkidle', { timeout: 20000 }).catch(() => {});
  }

  await gotoHome();
  await page.screenshot({ path: out.replace(/\.json$/, '-initial.png'), fullPage: false });

  const tree = await page.evaluate(() => {
    function readLi(li, path) {
      const a = li.querySelector(':scope > a');
      const sub = li.querySelector(':scope > ul.sub-menu');
      return {
        path,
        text: a ? a.textContent.trim().replace(/\s+/g, ' ') : li.textContent.trim().replace(/\s+/g, ' '),
        href: a ? a.getAttribute('href') : null,
        absHref: a ? a.href : null,
        hasSubmenu: !!sub,
        children: sub ? [...sub.children].filter(x => x.matches('li')).map((child, i) => readLi(child, path.concat(i))) : []
      };
    }
    const roots = [...document.querySelectorAll('#primary-menu > li')];
    return roots.map((li, i) => readLi(li, [i]));
  });

  function flatten(nodes, parentPath = []) {
    return nodes.flatMap(n => [n, ...flatten(n.children || [], n.path)]);
  }
  const links = flatten(tree).filter(n => n.href);

  async function revealPath(path) {
    for (let depth = 0; depth < path.length; depth++) {
      const selector = '#primary-menu' + path.slice(0, depth + 1).map(idx => ` > li:nth-child(${idx + 1})${depth === 0 ? '' : ' > ul.sub-menu > li:nth-child(' + (idx + 1) + ')'}`).join('');
      // The selector builder above is awkward for nested levels; use DOM evaluation for hover target instead.
    }
  }

  async function locatorForPath(path) {
    let loc = page.locator('#primary-menu > li').nth(path[0]);
    for (let i = 1; i < path.length; i++) {
      loc = loc.locator(':scope > ul.sub-menu > li').nth(path[i]);
    }
    return loc;
  }

  async function revealParentPath(path) {
    for (let depth = 0; depth < path.length; depth++) {
      const loc = await locatorForPath(path.slice(0, depth + 1));
      await loc.hover({ timeout: 10000 });
      await page.waitForTimeout(120);
    }
  }

  const results = [];
  for (const link of links) {
    await gotoHome();
    if (link.path.length > 1) await revealParentPath(link.path.slice(0, -1));
    else await revealParentPath(link.path);
    const loc = await locatorForPath(link.path);
    const state = await loc.evaluate(li => {
      const a = li.querySelector(':scope > a');
      const r = a.getBoundingClientRect();
      const c = getComputedStyle(a);
      const centerX = Math.min(Math.max(r.x + r.width / 2, 1), innerWidth - 1);
      const centerY = Math.min(Math.max(r.y + Math.min(r.height / 2, 10), 1), innerHeight - 1);
      const top = document.elementFromPoint(centerX, centerY);
      return {
        text: a.textContent.trim().replace(/\s+/g, ' '),
        href: a.href,
        rect: { x: r.x, y: r.y, w: r.width, h: r.height, right: r.right, bottom: r.bottom },
        display: c.display,
        visibility: c.visibility,
        opacity: c.opacity,
        visible: !!(r.width && r.height && c.display !== 'none' && c.visibility !== 'hidden' && Number(c.opacity) !== 0),
        inViewport: r.left >= 0 && r.right <= innerWidth && r.top >= 0 && r.bottom <= innerHeight,
        topElement: top ? `${top.tagName}#${top.id}.${top.className}` : null,
        clickableAtCenter: top === a || a.contains(top)
      };
    });

    let status = null, finalUrl = null, requestError = null;
    try {
      const resp = await page.request.get(state.href, { timeout: 20000, maxRedirects: 10 });
      status = resp.status();
      finalUrl = resp.url();
    } catch (e) {
      requestError = String(e);
    }

    let clickUrl = null, clickError = null;
    // Click all links inside the page context, but do not let bad third-party widgets decide pass/fail.
    try {
      await gotoHome();
      if (link.path.length > 1) await revealParentPath(link.path.slice(0, -1));
      else await revealParentPath(link.path);
      const clickLoc = (await locatorForPath(link.path)).locator(':scope > a');
      await clickLoc.click({ timeout: 10000 });
      await page.waitForLoadState('domcontentloaded', { timeout: 12000 }).catch(() => {});
      clickUrl = page.url();
    } catch (e) {
      clickError = String(e);
    }

    const expected = absUrl(link.href);
    const clickedAway = clickUrl && clickUrl.split('#')[0].replace(/\/$/, '') !== (baseUrl + '?kai_nav_verify=').split('?')[0].replace(/\/$/, '');
    results.push({ ...link, expected, state, status, finalUrl, requestError, clickUrl, clickError, clickedAway });
  }

  const failures = [];
  for (const r of results) {
    if (!r.state.visible) failures.push(`${r.text}: hidden when path revealed`);
    if (!r.state.inViewport) failures.push(`${r.text}: outside viewport ${JSON.stringify(r.state.rect)}`);
    if (!r.state.clickableAtCenter) failures.push(`${r.text}: not topmost/clickable at center (${r.state.topElement})`);
    if (r.requestError) failures.push(`${r.text}: request error ${r.requestError}`);
    if (r.status && (r.status < 200 || r.status >= 400)) failures.push(`${r.text}: bad HTTP status ${r.status}`);
    if (r.clickError) failures.push(`${r.text}: click error ${r.clickError}`);
    if (!r.clickedAway) failures.push(`${r.text}: click did not navigate away from homepage (${r.clickUrl})`);
  }

  const report = {
    baseUrl,
    viewport: { width: WIDTH, height: HEIGHT },
    navTree: tree,
    totalLinks: links.length,
    results,
    consoleMessages,
    failures
  };
  fs.writeFileSync(out, JSON.stringify(report, null, 2));
  await page.screenshot({ path: out.replace(/\.json$/, '-final.png'), fullPage: false });
  await browser.close();

  console.log(JSON.stringify({ baseUrl, totalLinks: links.length, failures: failures.length, out }, null, 2));
  if (failures.length) {
    console.error(failures.join('\n'));
    process.exit(1);
  }
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
