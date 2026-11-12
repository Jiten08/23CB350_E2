/*
 * =============================================================================
 * vite.config.js
 * =============================================================================
 *
 * PURPOSE:
 *   Settings for Vite, the tool that runs the React dev server. Its key job here
 *   is to forward every "/api" request from the browser to our Express server.
 *
 * WHAT TO BUILD:
 *   A default-exported Vite config (use defineConfig) that has:
 *     - plugins: the React plugin from @vitejs/plugin-react
 *     - server.port: 5173
 *     - server.proxy: "/api" → target "http://localhost:5000", changeOrigin: true
 *   With this in place, React code can call fetch("/api/cases"), with no full
 *   URL and no CORS errors during development.
 *
 * TALKS TO:
 *   - server/server.js. It must be running on port 5000 (PORT in server/.env).
 *   - src/api.js. Its "/api/..." URLs go through this proxy.
 *
 * STEPS:
 *   1. Start from the file Vite generated when you created the app.
 *   2. Add a `server` section with port 5173.
 *   3. Inside it, add `proxy` with the "/api" rule above.
 *   4. Restart `npm run dev`, then open http://localhost:5173/api/health
 *      while the server is running. You should see the server's JSON reply.
 *
 * CONCEPTS TO LEARN:
 *   - What a dev server or bundler is (Vite)
 *   - Dev proxies, and why they avoid CORS errors
 *   - export default and ES modules
 */
