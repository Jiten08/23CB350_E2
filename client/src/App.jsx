/*
 * =============================================================================
 * App.jsx
 * =============================================================================
 *
 * PURPOSE:
 *   The app's shell: the app name, a top bar with the 1930 helpline, and the
 *   routes that decide which page to show.
 *
 * WHAT TO BUILD:
 *   - A constant: APP_NAME = "AppName". This is the only place the name lives.
 *     Renaming the app later means changing this one line, plus <title> in
 *     index.html.
 *   - Component App (no props). It returns:
 *       * A top bar with APP_NAME and the text "Lost money? Call 1930".
 *         "1930" is a tel: link (<a href="tel:1930">), so phones can tap to call.
 *       * <Routes> with two routes:
 *           "/"         → <ReportPage />
 *           "/case/:id" → <CasePage />   (":id" is the case's MongoDB _id)
 *       * Optional: a catch-all "*" route that shows "Page not found".
 *
 * TALKS TO:
 *   - ReportPage.jsx and CasePage.jsx (the two pages)
 *   - main.jsx (renders App)
 *   - index.css (top bar styles)
 *
 * STEPS:
 *   1. Delete Vite's demo content (the counter and logos).
 *   2. Add the APP_NAME constant at the top.
 *   3. Build the top bar with the app name and the "Call 1930" tel: link.
 *   4. Import Routes and Route from react-router-dom, and add the two routes.
 *   5. Optional: set document.title = APP_NAME inside a useEffect.
 *
 * CONCEPTS TO LEARN:
 *   - JSX (className instead of class, {curly braces} for JS values)
 *   - React Router: <Routes>, <Route>, and URL params (:id)
 *   - tel: links for click-to-call
 */
