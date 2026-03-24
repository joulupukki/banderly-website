// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  site: 'https://www.banderly.com',
  output: 'static',
  integrations: [
    sitemap({
      filter: (page) =>
        !page.includes('/privacy') && !page.includes('/terms'),
    }),
  ],
});
