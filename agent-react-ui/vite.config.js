import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/agents': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/teams': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/workflows': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/sessions': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})
