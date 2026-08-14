import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  // GitHub Pages 项目站点挂在 /<repo>/ 子路径,用相对 base 保证可移植
  base: './',
})
