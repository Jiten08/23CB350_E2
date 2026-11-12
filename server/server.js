/*
 * =============================================================================
 * server.js
 * =============================================================================
 *
 * PURPOSE:
 *   The backend's entry point. It holds the Express setup, the MongoDB
 *   connection, the multer file uploads and the two API routes.
 *
 * WHAT TO BUILD:
 *   Setup:
 *     - Load .env with dotenv (import "dotenv/config" as the FIRST import)
 *     - Create the Express app. Add cors() and express.json().
 *     - Configure multer to save files to server/uploads/ with unique
 *       filenames. Accept two fields:
 *         "audio"  : at most 1 file, audio/* only
 *         "images" : at most 3 files, image/* only
 *       Set a size limit too. Gemini's inline data limit is about 20 MB per
 *       request, so keep the total under that.
 *     - Connect to MongoDB with mongoose.connect(process.env.MONGO_URI), then
 *       call app.listen(process.env.PORT || 5000).
 *
 *   Route: GET /api/health (optional, but useful for testing)
 *     Output: { status: "ok" }
 *
 *   Route 1: POST /api/cases
 *     Input:  a multipart form with text, language ("en"/"hi"), audio
 *             (optional), and images (up to 3)
 *     Flow:
 *       1. Call analyzeIncident({ text, language, audioFile, imageFiles }) from
 *          gemini.js. If it throws, call the triage function from fallback.js
 *          with the text instead, and set usedFallback = true.
 *       2. Add the legalSections and helplines from data.js that match the
 *          result's category.
 *       3. Save to MongoDB with the Case model (caseModel.js), and return
 *          the saved case as JSON (status 201).
 *     Errors: if text, audio and images are all empty → 400 with a message.
 *
 *   Route 2: GET /api/cases/:id
 *     Output: one case as JSON, 404 if not found, or 400 if the id isn't a
 *             valid MongoDB id.
 *
 * TALKS TO:
 *   - .env         → PORT, MONGO_URI (plus the Gemini settings used by gemini.js)
 *   - caseModel.js → the Case model, to save and find cases
 *   - gemini.js    → analyzeIncident()
 *   - fallback.js  → the regex triage used when Gemini fails
 *   - data.js      → categories, legalSections, helplines
 *   - uploads/     → where multer saves the files
 *   - client/src/api.js → sends the requests. Its field names must match
 *     ("audio", "images").
 *
 * STEPS:
 *   1. Get a basic Express server running with GET /api/health. Test it in the
 *      browser at http://localhost:5000/api/health.
 *   2. Add the Mongo connection and log "Connected to MongoDB".
 *   3. Add GET /api/cases/:id. Test it with a case you insert by hand
 *      (MongoDB Compass).
 *   4. Add multer, then POST /api/cases using fallback.js only at first.
 *   5. Switch to gemini.js, with fallback.js as the backup when it fails.
 *   6. Add a final error-handling middleware that returns { error: message }
 *      as JSON.
 *
 * CONCEPTS TO LEARN:
 *   - Express routes (app.get, app.post), req and res
 *   - multer (diskStorage, fileFilter, upload.fields)
 *   - async/await with try/catch
 *   - HTTP status codes (200, 201, 400, 404, 500)
 */
