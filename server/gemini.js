/*
 * =============================================================================
 * gemini.js
 * =============================================================================
 *
 * PURPOSE:
 *   Makes the single call to the Gemini API. It sends the text, voice note and
 *   screenshots together and gets back structured JSON about the fraud.
 *
 * WHAT TO BUILD:
 *   - A Gemini client from the @google/genai package:
 *       new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY })
 *     Do NOT use the old, deprecated @google/generative-ai package.
 *   - The model name from process.env.GEMINI_MODEL (e.g. "gemini-2.5-flash")
 *   - PROMPT: a text constant that tells Gemini to
 *       1. transcribe the voice note (if one is included)
 *       2. pick ONE category code from data.js
 *       3. decide the urgency using the URGENCY RULES below
 *       4. extract the details. Leave a field empty if it isn't present, and
 *          NEVER guess. List the empty fields in missingFields.
 *       5. write actions: the first steps in order (e.g. "Call 1930 now")
 *       6. write a complaint draft in English (en) and Hindi (hi)
 *     It must also say: never ask the user for an OTP, PIN or password.
 *   - RESPONSE SCHEMA: a JSON schema describing the fields below, passed as
 *     config.responseSchema with responseMimeType "application/json", so
 *     Gemini always returns valid JSON in this shape.
 *   - Exported async function analyzeIncident({ text, language, audioFile, imageFiles })
 *       Input:  the typed text, "en"/"hi", and the multer file objects for
 *               the audio (optional) and images (0–3)
 *       Output: an object with transcript, category, urgency, details,
 *               missingFields, actions, and draft
 *       Throws: if the API call fails or the reply isn't valid JSON. server.js
 *               then uses fallback.js instead.
 *
 * FIELDS GEMINI RETURNS (part of the full CASE SHAPE; use these exact names):
 *   {
 *     text, transcript, language,
 *     category,                // a code from data.js
 *     urgency,                 // "critical" | "high" | "medium" | "low"
 *     details: { suspectName, suspectPhone, suspectUpiId, bank, utr, amount, paymentApp, dateTime },
 *     missingFields: [],       // e.g. ["utr", "bank"]
 *     actions: [],             // first steps in order, e.g. "Call 1930 now"
 *     draft: { en, hi },
 *     legalSections: [],       // ← added by server.js from data.js, NOT by Gemini
 *     helplines: [],           // ← added by server.js from data.js, NOT by Gemini
 *     usedFallback,            // ← set by server.js
 *     createdAt                // ← set by MongoDB
 *   }
 *
 * URGENCY RULES (put these in the prompt):
 *   - critical: money lost in the last 24 hours, or the fraud is still happening
 *   - high:     money lost earlier, or an account or identity is compromised
 *   - medium:   threats or harassment, with no money lost
 *   - low:      suspicious contact only
 *
 * TALKS TO:
 *   - .env      → GEMINI_API_KEY, GEMINI_MODEL
 *   - data.js   → the list of category codes, to put in the prompt
 *   - uploads/  → reads the saved audio and image files from disk
 *   - server.js → calls analyzeIncident()
 *
 * STEPS:
 *   1. Send a text-only call ("Say hello") to check your key works.
 *   2. Write the PROMPT and send it with the user's text only.
 *   3. Add the response schema, and check that JSON.parse(response.text) works.
 *   4. Add the images: read each file, turn it into base64, and send it as
 *      { inlineData: { mimeType, data } }.
 *   5. Add the audio the same way. Chrome records audio/webm, so check the
 *      Gemini docs to see if that format is supported, and convert it if not.
 *   6. Throw a clear error if anything fails, so the fallback can take over.
 *
 * CONCEPTS TO LEARN:
 *   - @google/genai: ai.models.generateContent({ model, contents, config })
 *   - Multimodal "parts" (text + inlineData with base64)
 *   - Structured output (responseMimeType + responseSchema)
 *   - fs.promises.readFile and Buffer.toString("base64")
 */
