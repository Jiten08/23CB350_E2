/*
 * =============================================================================
 * caseModel.js
 * =============================================================================
 *
 * PURPOSE:
 *   The Mongoose schema and model for one fraud case, which defines the exact
 *   shape stored in MongoDB.
 *
 * WHAT TO BUILD:
 *   - caseSchema: a mongoose.Schema matching the CASE SHAPE below
 *   - Pass the option { timestamps: true }, so createdAt is added
 *     automatically
 *   - export default mongoose.model("Case", caseSchema)
 *
 * CASE SHAPE (the same field names are used in gemini.js and CasePage.jsx):
 *   {
 *     text, transcript, language,
 *     category,                // a code from data.js
 *     urgency,                 // "critical" | "high" | "medium" | "low"
 *     details: { suspectName, suspectPhone, suspectUpiId, bank, utr, amount, paymentApp, dateTime },
 *     missingFields: [],       // e.g. ["utr", "bank"]
 *     actions: [],             // first steps in order, e.g. "Call 1930 now"
 *     draft: { en, hi },
 *     legalSections: [],
 *     helplines: [],
 *     usedFallback,            // true if Gemini failed
 *     createdAt
 *   }
 *
 *   Suggested types:
 *     text, transcript, language, category → String
 *     urgency → String, with enum ["critical", "high", "medium", "low"]
 *     details → a nested object. amount → Number; everything else → String.
 *     missingFields, actions → [String]
 *     draft → { en: String, hi: String }
 *     legalSections, helplines → arrays of small objects (copied from data.js)
 *     usedFallback → Boolean, default false
 *
 * TALKS TO:
 *   - server.js → uses Case.create(...) and Case.findById(id)
 *
 * STEPS:
 *   1. Import mongoose.
 *   2. Write the schema with the simple fields first (text, category, urgency).
 *   3. Add the nested details and draft objects, and the arrays.
 *   4. Add { timestamps: true }, then export the model.
 *   5. Test it by saving one fake case from server.js and looking at it in
 *      MongoDB Compass.
 *
 * CONCEPTS TO LEARN:
 *   - Mongoose schema and model
 *   - Field types, nested objects and arrays
 *   - enum validation and default values
 *   - The timestamps option
 */
