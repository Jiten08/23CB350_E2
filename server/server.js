/*
 * =============================================================================
 * server.js
 * =============================================================================
 *
 * PURPOSE:
 *   The backend's entry point. It holds the Express setup, the MongoDB
 *   connection, the multer file uploads and the two API routes. It does NO AI
 *   work. It asks the Python agent (agent/main.py) to analyse each report.
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
 *       1. Check the input. If text, audio and images are all empty → 400
 *          with a message.
 *       2. Send the report to the agent:
 *            fetch(`${process.env.AGENT_URL}/analyze`, POST, JSON body)
 *            body: { text, language, audio_path, image_paths }
 *          Send ABSOLUTE file paths (path.resolve(file.path)) so the agent can
 *          read the files from server/uploads/. Fetch is built into Node 20,
 *          so there's nothing to install.
 *          The agent does Gemini, falls back to its regex triage if Gemini
 *          fails, and adds the legal sections and helplines.
 *       3. If the agent isn't reachable at all → 503 with
 *          "The AI service is not running. Start the agent (see README)."
 *       4. Save { text, language, ...agentResult } with the Case model
 *          (caseModel.js), and return the saved case as JSON (status 201).
 *
 *   Route 2: GET /api/cases/:id
 *     Output: one case as JSON, 404 if not found, or 400 if the id isn't a
 *             valid MongoDB id.
 *
 * TALKS TO:
 *   - .env         → PORT, MONGO_URI, AGENT_URL
 *   - caseModel.js → the Case model, to save and find cases
 *   - agent/main.py (Python, http://localhost:8000) → POST /analyze
 *   - uploads/     → where multer saves the files (the agent reads them too)
 *   - client/src/api.js → sends the requests. Its field names must match
 *     ("audio", "images").
 *
 * STEPS:
 *   1. Get a basic Express server running with GET /api/health. Test it in the
 *      browser at http://localhost:5000/api/health.
 *   2. Add the Mongo connection and log "Connected to MongoDB".
 *   3. Add GET /api/cases/:id. Test it with a case you insert by hand
 *      (MongoDB Compass).
 *   4. Add multer, then POST /api/cases. Save the files and log their paths.
 *   5. Call the agent's POST /analyze. At first, the agent can return fake
 *      data (see agent/main.py, step 3).
 *   6. Handle the "agent not running" error, and add a final error-handling
 *      middleware that returns { error: message } as JSON.
 *
 * CONCEPTS TO LEARN:
 *   - Express routes (app.get, app.post), req and res
 *   - multer (diskStorage, fileFilter, upload.fields)
 *   - Calling another service with fetch (server-to-server) and try/catch
 *   - HTTP status codes (200, 201, 400, 404, 500, 503)
 */
