# E2

<<<<<<< HEAD
AppName is a web app that helps Indian cyber-fraud victims get ready to report.
The victim describes what happened by typing, recording a voice note and/or uploading payment screenshots. A Python AI agent sends all of it to Gemini, which returns a fraud category, an urgency level, the key details (UPI ID, UTR, amount, bank) and a complaint draft in English and Hindi.
=======
E2 is a web app that helps Indian cyber-fraud victims get ready to report.
The victim describes what happened by typing, recording a voice note and/or uploading payment screenshots. Gemini AI turns this into a fraud category, an urgency level, the key details (UPI ID, UTR, amount, bank) and a complaint draft in English and Hindi.
>>>>>>> 9e72296679d6a14bc35e2905b8d3a8f96297558c
The result page shows what to do first (for example, "Call 1930 now"), along with helplines and the legal sections that may apply. **The app never files anything. It only prepares the user.**

> ⚠️ **Demo only.** This is a course-project MVP. Use **fake data only**: fake names, fake UPI IDs, fake UTRs and fake screenshots. Never enter real personal or banking details.

## How the three parts fit together

```
 Browser (client/, React)        Server (server/, Node + Express)        Agent (agent/, Python + FastAPI)
 ─────────────────────────       ────────────────────────────────        ────────────────────────────────
 ReportPage ── POST /api/cases ─► saves files to server/uploads/
                                  POST /analyze (JSON + file paths) ───► Gemini call (or regex fallback)
                                                                         + legal sections & helplines
                                  saves the case in MongoDB ◄─────────── returns the analysis JSON
 CasePage ◄── GET /api/cases/:id ─ reads the case from MongoDB
```

- **Client** shows the pages. It only ever talks to the server.
- **Server** handles uploads and the database. It does no AI work.
- **Agent** does all the AI work. It is the only part that holds the Gemini key.

## Stack

- **Client:** React + Vite, React Router, plain CSS, `fetch` (JavaScript, ES modules)
- **Server:** Node 20, Express, Mongoose, multer, dotenv, cors
- **Agent:** Python 3.10+, FastAPI, uvicorn, python-dotenv
- **AI:** Google Gemini through the `google-genai` Python package (*not* the old `google-generativeai`)
- **Database:** MongoDB (local or Atlas)

Right now every file contains **comments only**. Each one explains what to build, which files it talks to, the steps to follow and the concepts to learn first.

## Setup (do this later, when you start coding)

1. **Create the Vite app in `client/`:**
   ```bash
   cd client
   npm create vite@latest . -- --template react
   ```
   Vite overwrites `package.json`, `index.html`, `vite.config.js` and `src/main.jsx`. Copy the comments from our versions back in, or keep a copy before you start.
2. **Install the packages.** Each `package.json` has a `_comment` list, and `agent/requirements.txt` lists the Python packages.
   ```bash
   cd client && npm install react-router-dom
   cd ../server && npm init -y && npm install express mongoose multer dotenv cors && npm install -D nodemon
   cd ../agent
   python -m venv .venv
   .venv\Scripts\activate          # Windows   (macOS/Linux: source .venv/bin/activate)
   pip install -r requirements.txt
   ```
3. **Get a free Gemini API key** from Google AI Studio: https://aistudio.google.com/apikey
4. **Copy both `.env.example` files to `.env`:**
   - `server/.env`: `PORT`, `MONGO_URI`, `AGENT_URL`
   - `agent/.env`: `GEMINI_API_KEY`, `GEMINI_MODEL`, `AGENT_PORT`

   Never commit either `.env` file.
5. **Run the three parts in three terminals:**
   ```bash
   # Terminal 1: agent (activate .venv first)
   cd agent && uvicorn main:app --reload --port 8000   # http://localhost:8000/docs
   # Terminal 2: server
   cd server && npm run dev                             # http://localhost:5000
   # Terminal 3: client
   cd client && npm run dev                             # http://localhost:5173
   ```

## Who builds what

| # | Task | Files |
|---|------|-------|
| 1 | Report page | `client/src/ReportPage.jsx`, `client/src/VoiceRecorder.jsx`, `client/src/ImageUpload.jsx` |
| 2 | Result page | `client/src/CasePage.jsx`, `client/src/index.css` |
| 3 | Server and database | `server/server.js`, `server/caseModel.js`, `client/src/api.js` |
| 4 | Gemini agent | `agent/main.py`, `agent/gemini_agent.py` |
| 5 | Fallback and data | `agent/fallback.py`, `agent/data.py` |

Shared files (`App.jsx`, `main.jsx`, `vite.config.js`, `.gitignore`, the `.env.example` files, `requirements.txt`) are small, so whoever gets there first can set them up.
**Agree on the case shape first.** It's written in the comments of `server/caseModel.js`, `agent/gemini_agent.py` and `client/src/CasePage.jsx`, and all three must use the same field names (camelCase, even in Python).

## The API routes

**Server** (called by the client):
- `POST /api/cases`: multipart form with `text`, `language`, `audio` (optional) and `images` (up to 3). The server saves the files, asks the agent to analyse them, saves the case in MongoDB and returns it.
- `GET /api/cases/:id`: returns one case.

**Agent** (called only by the server):
- `POST /analyze`: JSON `{ text, language, audio_path, image_paths }`. Returns the analysis. Gemini is used first, and `fallback.py` takes over if Gemini fails. Test it at http://localhost:8000/docs.
