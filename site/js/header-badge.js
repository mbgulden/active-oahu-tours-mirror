/**
 * Active Oahu Tours - Header TripAdvisor Badge Injector
 * 
 * Single source of truth for the TripAdvisor badge in the site header.
 * This ensures all pages always display the correct, up-to-date badge
 * without requiring page-by-page HTML updates.
 * 
 * Usage: Include this script in the site footer or load async.
 * The badge will be injected into .social-links below the Book Online button.
 * 
 * Update the BADGE_CONFIG below to change the badge appearance or URL.
 */
(function() {
  'use strict';

  /**
   * TripAdvisor Attribution ID for Active Oahu Tours
   * Format: Attraction_Review-{destination}-{attractionId}
   */
  const TA_ATTRIBUTION_ID = 'Attraction_Review-g60659-d5079465-Reviews-Active_Oahu_Tours-Kailua_Oahu_Hawaii';

  /**
   * Badge configuration
   * Update here to propagate changes across ALL pages instantly
   */
  const BADGE_CONFIG = {
    rating: 4.8,
    reviewCount: 440,
    url: `https://www.tripadvisor.com/${TA_ATTRIBUTION_ID}.html`,
    ariaLabel: 'See TripAdvisor reviews (4.8, 440 reviews)',
    // Compact 55px star SVG - 5 green stars + 1 white
    starSvg: [
      '<svg viewBox="0 0 88 14" width="55" height="10" aria-hidden="true" style="vertical-align:middle">',
      '<polygon fill="#34E0A1" points="8,0 9.5,5 15,5 11,8 12.5,14 8,10.5 3.5,14 5,8 1,5 6.5,5"/>',
      '<polygon fill="#34E0A1" points="22,0 23.5,5 29,5 25,8 26.5,14 22,10.5 17.5,14 19,8 15,5 20.5,5"/>',
      '<polygon fill="#34E0A1" points="36,0 37.5,5 43,5 39,8 40.5,14 36,10.5 31.5,14 33,8 29,5 34.5,5"/>',
      '<polygon fill="#34E0A1" points="50,0 51.5,5 57,5 53,8 54.5,14 50,10.5 45.5,14 47,8 43,5 48.5,5"/>',
      '<polygon fill="#34E0A1" points="64,0 65.5,5 71,5 67,8 68.5,14 64,10.5 59.5,14 61,8 57,5 62.5,5"/>',
      '<polygon fill="#FFF" points="78,0 79.5,5 85,5 81,8 82.5,14 78,10.5 73.5,14 75,8 71,5 76.5,5"/>',
      '</svg>'
    ].join('')
  };

  /**
   * Build the canonical badge HTML
   */
  function buildBadgeHtml() {
    return (
      '<a href="' + BADGE_CONFIG.url + '" ' +
      'target="_blank" ' +
      'rel="noopener" ' +
      'class="tripadvisor-badge" ' +
      'aria-label="' + BADGE_CONFIG.ariaLabel + '">' +
      '<div class="tripadvisor-inline-badge" style="display:inline-flex;align-items:center;gap:4px;' +
      'padding:2px 6px;font-size:11px;background:#f8f9fa;border:1px solid #e9ecef;border-radius:3px;margin-top:4px;">' +
      BADGE_CONFIG.starSvg +
      '<span class="tripadvisor-badge-rating" style="font-weight:700;color:#34E0A1;font-size:12px;">' +
      BADGE_CONFIG.rating +
      '</span>' +
      '<span class="tripadvisor-badge-reviews" style="color:#666;font-size:11px;">' +
      ' \u00B7 ' + BADGE_CONFIG.reviewCount + ' reviews' +
      '</span>' +
      '</div></a>'
    );
  }

  /**
   * Inject or update the badge in the header's .social-links div
   */
  function injectBadge() {
    var socialLinks = document.querySelector('.social-header .social-links');
    if (!socialLinks) {
      console.warn('[header-badge] .social-header .social-links not found');
      return;
    }

    // Check if badge already exists
    var existingBadge = socialLinks.querySelector('.tripadvisor-badge');
    
    // Build fresh badge HTML
    var badgeHtml = buildBadgeHtml();

    if (existingBadge) {
      // Update existing badge in-place (preserves anchor position)
      var temp = document.createElement('div');
      temp.innerHTML = badgeHtml;
      var newBadge = temp.firstElementChild;
      
      // Replace only the inner badge content, not the <a> tag itself
      // This avoids any DOM reflow issues
      var existingInner = existingBadge.querySelector('.tripadvisor-inline-badge');
      var newInner = newBadge.querySelector('.tripadvisor-inline-badge');
      
      if (existingInner && newInner) {
        existingInner.replaceWith(newInner);
        // Update aria-label on the anchor
        existingBadge.setAttribute('aria-label', BADGE_CONFIG.ariaLabel);
        existingBadge.setAttribute('href', BADGE_CONFIG.url);
      } else {
        // Fallback: replace entire anchor
        existingBadge.replaceWith(newBadge);
      }
    } else {
      // No existing badge - find Book Online button and insert after it
      var bookOnline = socialLinks.querySelector('a[href*="fareharbor"], a[class*="btn"]');
      
      var temp = document.createElement('div');
      temp.innerHTML = badgeHtml;
      var newBadge = temp.firstElementChild;

      if (bookOnline && bookOnline.parentNode === socialLinks) {
        // Insert immediately after the Book Online button
        var nextSibling = bookOnline.nextSibling;
        if (nextSibling) {
          socialLinks.insertBefore(newBadge, nextSibling);
        } else {
          socialLinks.appendChild(newBadge);
        }
      } else {
        // Append to end of social-links
        socialLinks.appendChild(newBadge);
      }
    }
  }

  /**
   * Remove any duplicate badge anchors from the page
   */
  function removeDuplicateBadges() {
    var badges = document.querySelectorAll('.social-header .tripadvisor-badge');
    if (badges.length <= 1) return;

    // Keep only the first one, remove the rest
    for (var i = 1; i < badges.length; i++) {
      badges[i].parentNode.removeChild(badges[i]);
    }
  }

  /**
   * Main initialization
   */
  function init() {
    removeDuplicateBadges();
    injectBadge();
  }

  // Run on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
