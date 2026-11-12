/*
 * =============================================================================
 * main.jsx
 * =============================================================================
 *
 * PURPOSE:
 *   The entry point of the React app. It mounts <App /> into index.html.
 *
 * WHAT TO BUILD:
 *   No functions or components, only a few lines that:
 *     - import index.css (the single stylesheet)
 *     - find the <div id="root"> element
 *     - render <App /> inside <BrowserRouter> (from react-router-dom),
 *       wrapped in <StrictMode>
 *
 * TALKS TO:
 *   - index.html, which loads this file and provides #root
 *   - App.jsx, the component it renders
 *   - index.css, which it imports once for the whole app
 *
 * STEPS:
 *   1. Start from the main.jsx Vite generated.
 *   2. Import BrowserRouter from "react-router-dom".
 *   3. Wrap <App /> in <BrowserRouter> so that /case/:id URLs work.
 *   4. Make sure index.css is imported, and delete Vite's App.css if present.
 *
 * CONCEPTS TO LEARN:
 *   - createRoot(...).render(...)
 *   - <StrictMode>. In dev it runs effects twice on purpose, so don't panic.
 *   - React Router's <BrowserRouter>
 */
