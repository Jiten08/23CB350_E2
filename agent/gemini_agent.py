# =============================================================================
# gemini_agent.py
# =============================================================================
#
# PURPOSE:
#   Makes the single call to the Gemini API. It sends the text, voice note and
#   screenshots together and gets back structured JSON about the fraud.
#
# WHAT TO BUILD:
#   - A Gemini client from the google-genai package:
#       from google import genai
#       from google.genai import types
#       client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
#     ⚠️ Do NOT use the old "google-generativeai" package
#        (import google.generativeai). It's deprecated.
#   - The model name from os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
#
#   - PROMPT: a text constant that tells Gemini to
#       1. transcribe the voice note (if one is included)
#       2. pick ONE category code from data.py
#       3. decide the urgency using the URGENCY RULES below
#       4. extract the details. Leave a field empty if it isn't present, and
#          NEVER guess. List the empty fields in missingFields.
#       5. write actions: the first steps in order (e.g. "Call 1930 now")
#       6. write a complaint draft in English (en) and Hindi (hi)
#     It must also say: never ask the user for an OTP, PIN or password.
#
#   - Pydantic models that describe the answer (Gemini fills them in for you):
#       Details:  suspectName, suspectPhone, suspectUpiId, bank, utr,
#                 amount (float), paymentApp, dateTime (all optional)
#       Draft:    en, hi
#       Analysis: transcript, category, urgency, details (Details),
#                 missingFields (list[str]), actions (list[str]), draft (Draft)
#     Keep the field names in camelCase so they match the CASE SHAPE exactly.
#
#   - Function analyze_incident(text, language, audio_path, image_paths) -> dict
#       Input:  the typed text, "en"/"hi", one optional audio file path, and
#               0–3 image file paths
#       Output: a dict with the Analysis fields (use analysis.model_dump())
#       Raises: an error if the API call fails or the answer is missing.
#               main.py then uses fallback.py instead.
#
# FIELDS GEMINI RETURNS (part of the full CASE SHAPE; use these exact names):
#   {
#     text, transcript, language,
#     category,                // a code from data.py
#     urgency,                 // "critical" | "high" | "medium" | "low"
#     details: { suspectName, suspectPhone, suspectUpiId, bank, utr, amount, paymentApp, dateTime },
#     missingFields: [],       // e.g. ["utr", "bank"]
#     actions: [],             // first steps in order, e.g. "Call 1930 now"
#     draft: { en, hi },
#     legalSections: [],       // ← added by main.py from data.py, NOT by Gemini
#     helplines: [],           // ← added by main.py from data.py, NOT by Gemini
#     usedFallback,            // ← set by main.py
#     createdAt                // ← set by MongoDB
#   }
#
# URGENCY RULES (put these in the prompt):
#   - critical: money lost in the last 24 hours, or the fraud is still happening
#   - high:     money lost earlier, or an account or identity is compromised
#   - medium:   threats or harassment, with no money lost
#   - low:      suspicious contact only
#
# TALKS TO:
#   - agent/.env → GEMINI_API_KEY, GEMINI_MODEL
#   - data.py    → the category codes and labels, to put in the prompt
#   - server/uploads/ → reads the audio and image files at the paths it's given
#   - main.py    → calls analyze_incident()
#
# STEPS:
#   1. In a scratch script, send a text-only call ("Say hello") with
#      client.models.generate_content(model=..., contents="Say hello"), and
#      print response.text. This checks that your key works.
#   2. Write the PROMPT and send it with the user's text only.
#   3. Add the Pydantic models and ask for JSON with
#        config=types.GenerateContentConfig(
#            response_mime_type="application/json",
#            response_schema=Analysis,
#        )
#      Then response.parsed gives you a ready Analysis object.
#   4. Add the images: read each file's bytes (open(path, "rb").read()) and
#      add types.Part.from_bytes(data=..., mime_type="image/png") to contents.
#      Use the "mimetypes" module to get the right mime type.
#   5. Add the audio the same way. Chrome records audio/webm, so check the
#      Gemini docs to see if that format is supported, and convert it if not.
#   6. Raise a clear error if anything fails, so the fallback can take over.
#
# CONCEPTS TO LEARN:
#   - google-genai: client.models.generate_content(model, contents, config)
#   - Multimodal contents (a prompt string + types.Part.from_bytes for files)
#   - Structured output with a Pydantic response_schema and response.parsed
#   - Reading binary files in Python (open(path, "rb")) and mime types
# =============================================================================

import os
import mimetypes
from typing import Optional

from pydantic import BaseModel
from google import genai
from google.genai import types

from data import CATEGORIES


# ---------------------------------------------------------------------------
# Gemini client and model (created lazily so import doesn't fail without a key)
# ---------------------------------------------------------------------------
_client = None
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


def _get_client():             #helper function
    global _client
    if _client is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set in agent/.env")
        _client = genai.Client(api_key=api_key)
    return _client


# ---------------------------------------------------------------------------
# Pydantic models for structured output
# ---------------------------------------------------------------------------

class Details(BaseModel):
    suspectName: Optional[str] = None
    suspectPhone: Optional[str] = None
    suspectUpiId: Optional[str] = None
    bank: Optional[str] = None
    utr: Optional[str] = None
    amount: Optional[float] = None
    paymentApp: Optional[str] = None
    dateTime: Optional[str] = None


class Draft(BaseModel):
    en: str
    hi: str


class Analysis(BaseModel):
    transcript: str
    category: str
    urgency: str
    details: Details
    missingFields: list[str]
    actions: list[str]
    draft: Draft


# ---------------------------------------------------------------------------
# Prompt
# ---------------------------------------------------------------------------
CATEGORY_LIST = "\n".join(
    f"  {c['code']:8s} — {c['label']}" for c in CATEGORIES
)

PROMPT = f"""\
You are a cyber-fraud triage assistant for Indian citizens.

Analyse the user's fraud report (text, optional voice note, optional screenshots).

TASKS:
1. **Transcribe** the voice note if one is included. If there is no voice note,
   set transcript to an empty string.
2. **Category** — pick exactly ONE code from this list:
{CATEGORY_LIST}
3. **Urgency** — choose one:
   - critical: money lost in the last 24 hours OR the fraud is still happening
   - high:     money lost earlier, OR an account/identity is compromised
   - medium:   threats or harassment with no money lost
   - low:      suspicious contact only
4. **Details** — extract every fact you can find. Leave a field as null/empty
   if it is NOT present, and NEVER guess. List all empty fields in missingFields.
   Fields: suspectName, suspectPhone, suspectUpiId, bank, utr, amount, paymentApp, dateTime.
5. **Actions** — write the first steps the victim should take, in order.
   Example: "Call 1930 (National Cyber Crime Helpline) now".
6. **Draft** — write a formal complaint letter in both English (en) and Hindi (hi).

SAFETY RULE: Never ask the user for an OTP, PIN, or password.

Respond ONLY with valid JSON matching the schema provided.
"""


# ---------------------------------------------------------------------------
# Main function
# ---------------------------------------------------------------------------

def analyze_incident(
    text: str,
    language: str = "en",
    audio_path: str | None = None,
    image_paths: list[str] | None = None,
) -> dict:
    """
    Send the report to Gemini and return the structured Analysis as a dict.
    Raises on any API or parsing error so the caller can fall back.
    """
    image_paths = image_paths or []

    # Build the multimodal contents list
    contents: list = []

    # Add user text
    user_text = f"[Language: {language}]\n\n{text}" if text else f"[Language: {language}]"
    contents.append(user_text)

    # Add audio file if provided
    if audio_path and os.path.isfile(audio_path):
        audio_bytes = open(audio_path, "rb").read()
        mime_type = mimetypes.guess_type(audio_path)[0] or "audio/webm"
        contents.append(types.Part.from_bytes(data=audio_bytes, mime_type=mime_type))

    # Add image files
    for img_path in image_paths:
        if img_path and os.path.isfile(img_path):
            img_bytes = open(img_path, "rb").read()
            mime_type = mimetypes.guess_type(img_path)[0] or "image/png"
            contents.append(types.Part.from_bytes(data=img_bytes, mime_type=mime_type))

    # Add the system prompt
    contents.append(PROMPT)

    # Call Gemini with structured output
    response = _get_client().models.generate_content(
        model=MODEL,
        contents=contents,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=Analysis,
        ),
    )

    # Parse the structured response
    analysis = response.parsed
    if analysis is None:
        raise ValueError("Gemini returned an empty or unparseable response.")

    return analysis.model_dump()
