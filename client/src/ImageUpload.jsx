/*
 * =============================================================================
 * ImageUpload.jsx
 * =============================================================================
 *
 * PURPOSE:
 *   Lets the user pick up to 3 payment screenshots, shows previews, and hands
 *   the files to ReportPage.
 *
 * WHAT TO BUILD:
 *   Component ImageUpload
 *     Props (input): onImages(filesArray). Call it every time the list
 *                    changes.
 *     Shows:
 *       - <input type="file" accept="image/*" multiple>
 *       - a small preview of each chosen image, each with a "Remove" button
 *       - a message if the user tries to add more than 3 images
 *
 * TALKS TO:
 *   - ReportPage.jsx, the parent that receives the files through onImages
 *   - The server receives them as the "images" form field. The limit of 3
 *     must match the multer setting in server/server.js.
 *
 * STEPS:
 *   1. Render the file input.
 *   2. In onChange: turn event.target.files into an array with Array.from,
 *      add it to the existing files, and keep at most 3.
 *   3. Save the list in state and call onImages(list).
 *   4. Show previews with URL.createObjectURL(file).
 *   5. Add Remove: filter that file out, update state, and call onImages again.
 *
 * CONCEPTS TO LEARN:
 *   - <input type="file"> and the File object
 *   - Array.from, filter and slice (update arrays without mutating them)
 *   - URL.createObjectURL for previews
 *   - Rendering lists with map() and the `key` prop
 */
