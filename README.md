# AppName

AppName is a web app that helps Indian cyber-fraud victims get ready to report.
The victim describes what happened by typing, recording a voice note and/or uploading payment screenshots. Gemini AI turns this into a fraud category, an urgency level, the key details (UPI ID, UTR, amount, bank) and a complaint draft in English and Hindi.
The result page shows what to do first (for example, "Call 1930 now"), along with helplines and the legal sections that may apply. **The app never files anything. It only prepares the user.**

> ⚠️ **Demo only.** This is a course-project MVP. Use **fake data only**: fake names, fake UPI IDs, fake UTRs and fake screenshots. Never enter real personal or banking details.

## Stack

- **Client:** React + Vite, React Router, plain CSS, `fetch` (JavaScript, ES modules)
- **Server:** Node 20, Express, Mongoose, multer, dotenv, cors
- **AI:** Google Gemini through the `@google/genai` package (*not* the old `@google/generative-ai`)
- **Database:** MongoDB (local or Atlas)

Right now every file contains **comments only**. Each one explains what to build, which files it talks to, the steps to follow and the concepts to learn first.

## Setup (do this later, when you start coding)

1. **Create the Vite app in `client/`:**
   ```bash
   cd client
   npm create vite@latest . -- --template react
   ```
   Vite overwrites `package.json`, `index.html`, `vite.config.js` and `src/main.jsx`. Copy the comments from our versions back in, or keep a copy before you start.
2. **Install the packages.** Each `package.json` has a `_comment` list with the exact packages and scripts.
   ```bash
   cd client && npm install react-router-dom
   cd ../server && npm init -y && npm install express mongoose multer dotenv cors @google/genai && npm install -D nodemon
   ```
3. **Get a free Gemini API key** from Google AI Studio: https://aistudio.google.com/apikey
4. **Copy `server/.env.example` to `server/.env`** and fill in `PORT`, `MONGO_URI`, `GEMINI_API_KEY` and `GEMINI_MODEL`. Never commit `.env`.
5. **Run the client and the server in two terminals:**
   ```bash
   # Terminal 1
   cd server && npm run dev     # http://localhost:5000
   # Terminal 2
   cd client && npm run dev     # http://localhost:5173 (forwards /api to the server)
   ```

## Who builds what

| # | Task | Files |
|---|------|-------|
| 1 | Report page | `client/src/ReportPage.jsx`, `client/src/VoiceRecorder.jsx`, `client/src/ImageUpload.jsx` |
| 2 | Result page | `client/src/CasePage.jsx`, `client/src/index.css` |
| 3 | Server and database | `server/server.js`, `server/caseModel.js`, `client/src/api.js` |
| 4 | Gemini | `server/gemini.js` |
| 5 | Fallback and data | `server/fallback.js`, `server/data.js` |

Shared files (`App.jsx`, `main.jsx`, `vite.config.js`, `.gitignore`, `.env.example`) are small, so whoever gets there first can set them up.
**Agree on the case shape first.** It's written in the comments of `caseModel.js`, `gemini.js` and `CasePage.jsx`, and all three must use the same field names.

## The two API routes

- `POST /api/cases`: multipart form with `text`, `language`, `audio` (optional) and `images` (up to 3). The server analyses it with Gemini (or `fallback.js` if Gemini fails), adds legal sections and helplines from `data.js`, saves it, and returns the case.
- `GET /api/cases/:id`: returns one case.
