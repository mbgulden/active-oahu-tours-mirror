import { defineConfig } from 'astro/config';
import cloudflare from '@astrojs/cloudflare';

export default defineConfig({
  output: 'static',
  adapter: cloudflare({
    platformProxy: { enabled: true },
    imageService: true,
  }),
  // Route redirects to the static mirror site
  redirects: {},
  site: 'https://activeoahutours.com',
  build: {
    // Output to a subdirectory to avoid conflicting with static site
    assets: '_aot_assets',
  },
});
