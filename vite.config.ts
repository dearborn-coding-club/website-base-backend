import { defineConfig } from 'vite';
import { splitVendorChunkPlugin } from 'vite';
import react from '@vitejs/plugin-react';
import tsconfigPaths from 'vite-tsconfig-paths';
import { resolve } from 'path';

// https://vitejs.dev/config/
export default defineConfig({
  build: { 
    manifest: true,
    rollupOptions: {
      input: {
        main: resolve(__dirname, './index.html'),
      }
    },
  },
  base: process.env.mode === "production" ? "/static/" : "./",
  root: "./",
  plugins: [react(), splitVendorChunkPlugin(), tsconfigPaths()],
});
