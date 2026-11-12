/*
 * =============================================================================
 * ReportPage.jsx   (route "/")
 * =============================================================================
 *
 * PURPOSE:
 *   The intake form. The victim describes what happened as typed text, a voice
 *   note and/or screenshots, then submits it for analysis.
 *
 * WHAT TO BUILD:
 *   Component ReportPage (no props). It shows:
 *     - A short heading and one line of help text
 *     - A <textarea> for "What happened?"
 *     - <VoiceRecorder onAudio={...} />. It gives back an audio Blob, or null.
 *     - <ImageUpload onImages={...} />. It gives back an array of 0–3 image Files.
 *     - A language pick: English ("en") or Hindi ("hi"). This is the language
 *       the user typed or spoke in. The UI itself stays English.
 *     - A Submit button
 *     - While waiting: the button is disabled and shows "Analysing…"
 *     - On error: a red message
 *   On success, it navigates to /case/<id of the new case>.
 *
 * TALKS TO:
 *   - api.js            → submitReport(formData)
 *   - VoiceRecorder.jsx → receives the audio through a callback prop
 *   - ImageUpload.jsx   → receives the images through a callback prop
 *   - App.jsx           → this page is the "/" route
 *   - useNavigate (react-router-dom) → goes to /case/:id
 *
 * STEPS:
 *   1. Render a static version first: the textarea, select and button only.
 *   2. Add state with useState: text, language ("en"), audio (null),
 *      images ([]), loading (false), error ("").
 *   3. Make the textarea and select "controlled" (value + onChange).
 *   4. Add <VoiceRecorder> and <ImageUpload>, and store what they send back
 *      in state.
 *   5. Write handleSubmit(event):
 *        a. event.preventDefault()
 *        b. If text, audio and images are all empty, show an error and stop.
 *        c. Build a FormData: append "text", "language", "audio" (if any),
 *           and "images" (append once per file).
 *        d. Set loading to true, then call submitReport(formData).
 *        e. On success: navigate(`/case/${newCase._id}`)
 *        f. On error: set the error message. Always set loading back to false.
 *   6. Style it in index.css.
 *
 * CONCEPTS TO LEARN:
 *   - useState and controlled inputs
 *   - Form onSubmit and event.preventDefault()
 *   - Callback props (a child passes data up to its parent)
 *   - FormData and useNavigate
 */
