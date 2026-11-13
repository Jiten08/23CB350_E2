# =============================================================================
# main.py   (the agent's entry point)
# =============================================================================
#
# PURPOSE:
#   A small FastAPI web service that does ALL the AI work. server.js sends it
#   one report, and it sends back the full analysis (Gemini, or the fallback
#   if Gemini fails).
#
# WHAT TO BUILD:
#   - Call load_dotenv() at the top, so agent/.env is read before anything else.
#   - app = FastAPI()
#   - A Pydantic model AnalyzeRequest with these fields:
#       text: str = ""
#       language: str = "en"            ("en" or "hi")
#       audio_path: str | None = None   (absolute path of the saved voice note)
#       image_paths: list[str] = []     (absolute paths of 0–3 screenshots)
#     server.js saves the files in server/uploads/ and sends only their PATHS.
#     The agent reads the files from disk. This works because both run on the
#     same computer, which is fine for a demo.
#
#   Route: GET /health
#     Output: {"status": "ok"}
#
#   Route: POST /analyze
#     Input:  JSON matching AnalyzeRequest
#     Flow:
#       1. Try analyze_incident(...) from gemini_agent.py.
#       2. If it raises ANY error: print the error, call triage(text) from
#          fallback.py, and set used_fallback = True.
#       3. Add legal_sections and helplines from data.py that match the
#          result's category.
#       4. Return one JSON object with the CASE SHAPE fields (camelCase names,
#          so server.js can save it as-is):
#            transcript, category, urgency, details, missingFields, actions,
#            draft, legalSections, helplines, usedFallback
#          (text, language and createdAt are added by server.js and MongoDB.)
#
# TALKS TO:
#   - server/server.js → calls POST /analyze at AGENT_URL (http://localhost:8000)
#   - gemini_agent.py  → analyze_incident()
#   - fallback.py      → triage()
#   - data.py          → get_legal_sections(), get_helplines()
#   - agent/.env       → loaded here with load_dotenv()
#
# STEPS:
#   1. Build GET /health. Run `uvicorn main:app --reload --port 8000` and open
#      http://localhost:8000/health.
#   2. Open http://localhost:8000/docs. FastAPI makes a free test page where
#      you can try every route.
#   3. Write AnalyzeRequest and a POST /analyze that only returns fake data.
#      The server team can connect to it straight away.
#   4. Connect it to fallback.py (no API key needed).
#   5. Connect it to gemini_agent.py, with fallback.py as the backup on errors.
#   6. Add the data.py lookups.
#
# CONCEPTS TO LEARN:
#   - FastAPI routes (@app.get, @app.post) and the auto docs at /docs
#   - Pydantic models (request bodies with type hints)
#   - try / except in Python
#   - Running a server with uvicorn
# =============================================================================

from dotenv import load_dotenv
load_dotenv()  # read agent/.env before anything else

from fastapi import FastAPI
from pydantic import BaseModel

from gemini_agent import analyze_incident
from fallback import triage
from data import get_legal_sections, get_helplines


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
app = FastAPI()


# ---------------------------------------------------------------------------
# Request model
# ---------------------------------------------------------------------------
class AnalyzeRequest(BaseModel):
    text: str = ""
    language: str = "en"
    audio_path: str | None = None
    image_paths: list[str] = []


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    used_fallback = False

    # 1. Try Gemini
    try:
        result = analyze_incident(
            text=req.text,
            language=req.language,
            audio_path=req.audio_path,
            image_paths=req.image_paths,
        )
    except Exception as e:
        # 2. If Gemini fails, use the fallback
        print(f"Gemini failed, using fallback: {e}")
        result = triage(req.text)
        used_fallback = True

    # 3. Add legal sections and helplines from data.py
    category = result.get("category", "OTHER")
    result["legalSections"] = get_legal_sections(category)
    result["helplines"] = get_helplines(category)
    result["usedFallback"] = used_fallback

    # 4. Return the full CASE SHAPE
    return result
