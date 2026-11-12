/*
 * =============================================================================
 * api.js
 * =============================================================================
 *
 * PURPOSE:
 *   Holds the ONLY two fetch calls in the client. Pages call these functions
 *   and never call fetch() directly.
 *
 * WHAT TO BUILD (two exported async functions):
 *
 *   submitReport(formData)
 *     Input:  a FormData object built by ReportPage, with these fields:
 *             text, language ("en" or "hi"), audio (optional, one file),
 *             images (0 to 3 files)
 *     Does:   POST /api/cases with the FormData as the body.
 *             Do NOT set a Content-Type header. The browser adds the
 *             multipart boundary itself.
 *     Output: the saved case object (see "Case shape" in CasePage.jsx),
 *             including its _id
 *
 *   getCase(id)
 *     Input:  the case id (a string from the URL)
 *     Does:   GET /api/cases/<id>
 *     Output: the case object
 *
 *   For both: if response.ok is false, throw an Error that has the server's
 *   message, so the page can show it.
 *
 * TALKS TO:
 *   - server/server.js, through the Vite proxy ("/api" → localhost:5000)
 *   - ReportPage.jsx (uses submitReport) and CasePage.jsx (uses getCase)
 *   - The field names MUST match the multer setup in server.js:
 *     "audio" and "images".
 *
 * STEPS:
 *   1. Write getCase first, because it's simpler. Test it once the server
 *      has a case.
 *   2. Write submitReport.
 *   3. Optional: a small shared helper that checks response.ok and returns
 *      response.json(), so both functions can reuse it.
 *
 * CONCEPTS TO LEARN:
 *   - fetch() with async/await
 *   - response.ok, response.json()
 *   - FormData
 *   - throw new Error(...) and try/catch in the caller
 *
 * SECURITY: The Gemini API key is never used here or anywhere in client/.
 */
