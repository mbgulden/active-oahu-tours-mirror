# Cloudflare Configuration for AOT

## Account and zone

- **Account**: `3e13f120ec7532f0bc8ac0bc9bfc7108` (AOT account)
- **Zone**: `a8dc4f7db7ab9cea93c04ba315a7a7f7` (activeoahutours.com)
- **Plan**: PRO (20 page rules, custom WAF, no rate-limiting rules)
- **DNS**: Apex + www both CNAME proxied → `active-oahu-tours-mirror.pages.dev`
- **Mail**: Google Workspace, MX records configured, DKIM k2/k3 (Mailchimp)
- **DMARC**: `p=none`, sent to `dmarc_agg@vali.email`

## Auth (two ways)

1. **Global Key + email** (legacy, what the kai profile uses)
   ```
   X-Auth-Email: michael@activeoahu.com
   X-Auth-Key: <cfk_xxxxx>
   ```
   Stored in `~/.hermes/profiles/kai/.env` as `CLOUDFLARE_AOT_*`

2. **API Token (Bearer)** (newer, scoped)
   ```
   Authorization: Bearer <token>
   ```
   Used by GrowthWebDev account scripts. Different scope.

## What lives where

| Concern | Where | How to inspect |
|---|---|---|
| Zone settings (security, TLS, etc.) | `/zones/{id}/settings` | `curl .../settings` |
| Page rules | `/zones/{id}/pagerules` | `curl .../pagerules` |
| DNS records | `/zones/{id}/dns_records` | `curl .../dns_records` |
| WAF custom rules | `/zones/{id}/rulesets?phase=http_request_firewall_custom` | List rulesets, get specific id |
| WAF managed rulesets | `/zones/{id}/rulesets?phase=http_request_firewall_managed` | |
| Transform rules | `/zones/{id}/rulesets?phase=http_response_headers_transform` | |
| Bot management | `/zones/{id}/bot_management` | |
| Security events | GraphQL `viewer.accounts.firewallEventsAdaptive` | |

## Current zone settings (canonical)

| Setting | Value | Set when |
|---|---|---|
| `security_level` | `medium` | 2026-06-23 (Kai GRO-588 hardening) |
| `min_tls_version` | `1.2` | 2026-06-23 (Kai) |
| `tls_1_3` | `on` | default |
| `ssl` | `strict` | default |
| `security_header.strict_transport_security.enabled` | `true` | 2026-06-23 (Kai) |
| `security_header...max_age` | `31536000` | 2026-06-23 |
| `security_header...include_subdomains` | `true` | 2026-06-23 |
| `security_header...nosniff` | `true` | 2026-06-23 |
| `security_header...preload` | `false` | (deliberately off until confident) |

## Current page rules

| Priority | Pattern | Actions |
|---|---|---|
| 1 | `activeoahutours.com/book*` | `cache_level: bypass`, `security_level: high` |

19 rules remaining on PRO tier. See GRO-2214 for planned use cases.

## Current WAF custom ruleset (http_request_firewall_custom phase)

Ruleset ID: `e16d311efb07454d8a6511d2250e0416`

Rules (each blocks its path with HTTP 410):

| Rule ID prefix | Description |
|---|---|
| GRO-588 wp-json | `/wp-json/*` |
| GRO-588 wp-admin | `/wp-admin/*` |
| GRO-588 wp-login | `/wp-login/*` |
| GRO-588 wp-includes | `/wp-includes/*` |
| GRO-588 wp-content/plugins | `/wp-content/plugins/*` |
| GRO-588 xmlrpc | `/xmlrpc.php` |
| GRO-588 wp-cron | `/wp-cron.php` |

## WAF managed rulesets (http_request_firewall_managed phase)

- **Cloudflare Managed Free Ruleset** — deployed in **log-only** mode
  (ruleset ID `a3c9f1d5c7a949fd94ce4c47876df68f`, 26 inner rules all→log)
- 48h observation window: 2026-06-25 15:00 UTC (then promote/log-disable per data)
- See GRO-2210 for the observation review process

## Current transform rules (http_response_headers_transform phase)

Ruleset ID: `a49a3fa6c6bb42f89c287ad266062f73`

| Rule | Expression | Action |
|---|---|---|
| GRO-591 X-UA-Compatible | `http.response.code == 200` | `set X-UA-Compatible: IE=edge` |

## Bot management (zombie-mode)

**Permanently off — Michael's policy 2026-06-23.**

| Setting | Value |
|---|---|
| `sbfm_definitely_automated` | `allow` |
| `sbfm_verified_bots` | `allow` |
| `ai_bots_protection` | `disabled` |
| `crawler_protection` | `disabled` |
| `content_bots_protection` | `disabled` |
| `enable_js` | `true` (default) |

**Why AI bots are allowed:** AOT is a tour business. AI citations = direct
booking attribution. Blocking them loses ChatGPT/Claude citations to
competitors. See [GRO-2211](https://linear.app/growthwebdev/issue/GRO-2211)
comment thread for the policy rationale.

## Editing rules safely

Before changing any CF setting, **always**:
1. Capture current state (curl the relevant endpoint, save to `/tmp/aot_cf_before.json`)
2. Make the change via API or dashboard
3. Verify with a curl that tests the affected behavior
4. Capture new state (`/tmp/aot_cf_after.json`)
5. Diff the two
6. Document in Linear issue + the hardening report

**For destructive changes** (rule deletion, zone setting revert): capture
the API command in the Linear issue BEFORE running it, so the comment thread
has the rollback command ready.

## Useful queries

### Find rules from a specific Linear issue
```bash
# Look for custom rule with description matching GRO-XXXX
curl -sS "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_AOT_ZONE_ACTIVEOAHUTOURS/rulesets/e16d311efb07454d8a6511d2250e0416" \
  -H "X-Auth-Email: $CLOUDFLARE_AOT_EMAIL" -H "X-Auth-Key: $CLOUDFLARE_AOT_API_KEY" \
  | python3 -c "import json,sys; [print(r['description']) for r in json.load(sys.stdin)['result']['rules']]"
```

### Check WAF events for the last 24h
```bash
# Must be <24h window — CF GraphQL quota limit
curl -sS -X POST "https://api.cloudflare.com/client/v4/graphql" \
  -H "X-Auth-Email: $CLOUDFLARE_AOT_EMAIL" -H "X-Auth-Key: $CLOUDFLARE_AOT_API_KEY" \
  -H "Content-Type: application/json" \
  --data '{"query":"{ viewer { accounts(filter: {accountTag: \"'$CLOUDFLARE_AOT_ACCOUNT_ID'\"}) { firewallEventsAdaptive(filter: {datetime_gt: \"'$(date -u -d '23 hours ago' +%Y-%m-%dT%H:%M:%SZ)'\"}, limit: 50, orderBy: [datetime_DESC]) { action clientIP datetime clientRequestPath ruleId } } } }"}'
```

### Test if a path is blocked
```bash
curl -sS -o /dev/null -w "%{http_code}\n" "https://activeoahutours.com/wp-json/"
# Expected: 410
```

## See also

- [deploy-process.md](deploy-process.md) — when CF edge changes take effect (immediately)
- [testing-guidelines.md](testing-guidelines.md) — verify CF changes don't break legit traffic
- The hardening report: https://docs.google.com/document/d/1muTHboWzBXi1TOPlqmOopNqI1NN9bHulww6TgO2CDEc/edit