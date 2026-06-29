# Active Oahu Tours Mirror

Static HTML mirror for Active Oahu Tours.

## Environments

There are structural differences between the production environment and the staging environment. These exist because production runs WordPress (served dynamically) and staging runs a static Cloudflare Pages export of the mirror.

### URL Shapes & Anchors
* **Production URL Shape:** Production URLs use the `.html` extension (e.g., `/activities.html`, `/contact-us.html`). Hash anchors (query strings and target hashes) are often HTML/URL entity-encoded (e.g., `%20`, `&#038;`).
* **Staging URL Shape:** Staging URLs use a clean trailing-slash format (e.g., `/activities/`, `/contact-us/`) and raw unencoded characters in hash anchors (e.g., spaces and `&`).

### Link Authoring Conventions
* **Authoring NEW content in the mirror:** Use the clean trailing-slash form (staging-native style, e.g., `/activities/`).
* **Porting content from production to the mirror:** Ensure all internal link forms are converted:
  * Remove `.html` extensions and replace with trailing slashes (e.g., `.html` → `/`).
  * Decode HTML/URL entities in path targets.
  * Staging's `_redirects` handles mapping the trailing-slash canonical URLs to the static `.html` export files during staging serving, but direct references within authored HTML should follow these clean patterns to prevent extra redirection hops.

### Japanese Language Switcher (/ja/)
* Staging features a static/hardcoded `<a href="/ja/">` language switcher link in the page body, generated in the static mirror's HTML files.
* Production does not have this hardcoded link in the source HTML; instead, the Weglot JavaScript library dynamically inserts and rewrites the language switcher buttons at runtime.
* The Weglot integration and configuration blocks are identical on both. The static link on staging is correctly handled/rewritten by Weglot JS at runtime and does not break navigation.

### Font Path Caveat
* Staging uses relative font paths prefixed with `../` (e.g., `src: url(../fonts.gstatic.com/...)`).
* This is completely fine when the static mirror is served from the root domain of the Cloudflare Pages deploy (e.g., `active-oahu-tours-mirror.pages.dev`).
* **Caution:** If the mirror is ever deployed or served from a nested sub-path (e.g., `domain.com/sub-path/`), the relative `../` prefix will resolve to a parent directory outside the deploy path and break font loading. If sub-path deployments are planned, these paths must be resolved to root-relative or absolute forms.
