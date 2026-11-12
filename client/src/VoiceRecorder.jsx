/*
 * =============================================================================
 * VoiceRecorder.jsx
 * =============================================================================
 *
 * PURPOSE:
 *   Lets the user record a voice note in the browser and hands the recording
 *   to ReportPage.
 *
 * WHAT TO BUILD:
 *   Component VoiceRecorder
 *     Props (input): onAudio(blobOrNull). Call it with the finished
 *                    recording, or with null when the user deletes it.
 *     Shows:
 *       - a "Record" button. It asks for microphone permission, then starts.
 *       - a "Stop" button, shown while recording (a running timer is a nice
 *         extra)
 *       - after stopping: an <audio controls> player to listen back, plus a
 *         "Delete" button
 *       - a friendly message if mic permission is denied
 *
 * TALKS TO:
 *   - ReportPage.jsx, the parent that receives the audio through onAudio
 *   - The server receives the audio as the "audio" form field (see api.js).
 *     Chrome records "audio/webm". Check that Gemini accepts that format
 *     (gemini.js).
 *
 * STEPS:
 *   1. Render the buttons with no logic yet.
 *   2. On Record: navigator.mediaDevices.getUserMedia({ audio: true }),
 *      then create a new MediaRecorder(stream).
 *   3. Collect chunks in recorder.ondataavailable. Keep them in a useRef,
 *      not in state.
 *   4. In recorder.onstop: build one Blob from the chunks, make a preview URL
 *      with URL.createObjectURL, call onAudio(blob), and turn the mic off
 *      (stop every track).
 *   5. On Stop: recorder.stop().
 *   6. On Delete: clear everything and call onAudio(null).
 *
 * CONCEPTS TO LEARN:
 *   - getUserMedia (microphone permission)
 *   - MediaRecorder and Blob
 *   - useRef vs useState
 *   - URL.createObjectURL
 */
