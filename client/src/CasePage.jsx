/*
 * =============================================================================
 * CasePage.jsx   (route "/case/:id")
 * =============================================================================
 *
 * PURPOSE:
 *   The result page. It loads one analysed case and tells the victim what to
 *   do, most urgent first.
 *
 * WHAT TO BUILD:
 *   Component CasePage (no props; reads :id from the URL). It shows, top to
 *   bottom:
 *     1. Urgency badge: a coloured label from case.urgency
 *     2. First actions: case.actions as a numbered list. Make the first one
 *        big. If it mentions 1930, add a tel:1930 button.
 *     3. Details: each field of case.details with a friendly label, plus a
 *        warning list built from case.missingFields
 *        (e.g. "We couldn't find: UTR, Bank. Add these if you have them.")
 *     4. Complaint draft: "English" and "Hindi" tabs that switch between
 *        draft.en and draft.hi (keep line breaks), and a Print button that
 *        calls window.print()
 *     5. Legal sections: case.legalSections (act, section, plain-English note)
 *     6. Helplines: case.helplines (name, tel: link or website link)
 *     7. AI disclaimer: "This was prepared by AI and may contain mistakes.
 *        AppName has NOT filed anything. File at cybercrime.gov.in or call
 *        1930." If case.usedFallback is true, also say the AI was unavailable
 *        and a basic check was used instead.
 *   Also show a "Loading…" state and an error state (e.g. case not found).
 *
 * CASE SHAPE (the same field names are used in server/caseModel.js and
 * agent/gemini_agent.py):
 *   {
 *     text, transcript, language,
 *     category,                // a code from agent/data.py
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
 * TALKS TO:
 *   - api.js → getCase(id)
 *   - useParams (react-router-dom) → reads id from the URL
 *   - index.css → badge colours, tabs, print styles
 *
 * STEPS:
 *   1. Read id with useParams().
 *   2. Add state: caseData (null), loading (true), error ("").
 *   3. In a useEffect that depends on [id]: call getCase(id), then save the
 *      result or the error.
 *   4. Render the loading and error states first.
 *   5. Build each section in the order above, one at a time. Use optional
 *      chaining (caseData.details?.utr), because fields can be empty.
 *   6. Add the English/Hindi tab state and the Print button.
 *   7. Optional: split big sections into small components inside this file.
 *
 * CONCEPTS TO LEARN:
 *   - useParams and useEffect (load data when the page opens)
 *   - Conditional rendering (loading / error / data)
 *   - Optional chaining (?.) and rendering lists with map()
 *   - window.print() and @media print
 */
