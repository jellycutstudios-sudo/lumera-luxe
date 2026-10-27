import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  output: 'static',
  site: 'https://lumeraluxe.com.qa',
  compressHTML: true,
  prefetch: {
    prefetchAll: false,
    defaultStrategy: 'hover'
  },
  integrations: [sitemap()],
  build: {
    format: 'directory'
  },
  devToolbar: {
    enabled: false
  }
});
