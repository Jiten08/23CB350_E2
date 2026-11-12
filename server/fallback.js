/*
 * =============================================================================
 * fallback.js
 * =============================================================================
 *
 * PURPOSE:
 *   A simple, offline "triage" that uses regular expressions. server.js calls
 *   it when Gemini fails (no key, no internet, quota used up), so the demo
 *   never breaks.
 *
 * WHAT TO BUILD:
 *   Exported function triage(text)
 *     Input:  the user's typed text (a string; may be empty)
 *     Output: an object with the SAME fields Gemini returns (see gemini.js):
 *       - transcript: ""          (we can't transcribe audio without AI)
 *       - category:  a guess from keywords (e.g. "upi"/"gpay"/"phonepe" →
 *                    "UPI", "job"/"task" → "JOB"), otherwise "OTHER"
 *       - urgency:   "critical" if an amount was found, otherwise "medium"
 *                    (keep it simple and on the safe side)
 *       - details:   whatever the regexes below find. Leave the rest empty.
 *       - missingFields: the names of the details that stayed empty
 *       - actions:   a fixed safe list, e.g. ["Call 1930 now",
 *                    "Call your bank to block the account/card",
 *                    "Report at cybercrime.gov.in"]
 *       - draft:     a simple fill-in-the-blanks template in English and Hindi
 *
 *   Regexes to write:
 *     - UPI ID: something@handle (e.g. name123@okaxis)
 *     - UTR: a number of exactly 12 digits
 *     - Amount: ₹ or "Rs" or "INR" followed by a number (allow commas,
 *       e.g. ₹1,25,000)
 *     - Phone (optional): a 10-digit Indian mobile number starting with 6–9
 *
 * TALKS TO:
 *   - server.js → calls triage() when analyzeIncident() throws
 *   - data.js   → the category codes
 *
 * STEPS:
 *   1. Write and test each regex alone, on a tool like regex101.com, with
 *      fake examples.
 *   2. Write triage(), which runs each regex with text.match(...).
 *   3. Add the keyword → category guess.
 *   4. Build missingFields, actions and the draft templates.
 *   5. Test it by turning off your Gemini key and submitting a report.
 *
 * CONCEPTS TO LEARN:
 *   - Regular expressions (character classes, \d{12}, groups, flags)
 *   - String.match and String.includes
 *   - Template literals for the draft text
 */
