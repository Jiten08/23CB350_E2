# =============================================================================
# fallback.py
# =============================================================================
#
# PURPOSE:
#   A simple, offline "triage" that uses regular expressions. main.py calls it
#   when Gemini fails (no key, no internet, quota used up), so the demo never
#   breaks.
#
# WHAT TO BUILD:
#   Function triage(text) -> dict
#     Input:  the user's typed text (a string; may be empty)
#     Output: a dict with the SAME fields Gemini returns (see gemini_agent.py):
#       - transcript: ""          (we can't transcribe audio without AI)
#       - category:  a guess from keywords (e.g. "upi"/"gpay"/"phonepe" →
#                    "UPI", "job"/"task" → "JOB"), otherwise "OTHER"
#       - urgency:   "critical" if an amount was found, otherwise "medium"
#                    (keep it simple and on the safe side)
#       - details:   whatever the regexes below find. Leave the rest as None.
#       - missingFields: the names of the details that stayed empty
#       - actions:   a fixed safe list, e.g. ["Call 1930 now",
#                    "Call your bank to block the account/card",
#                    "Report at cybercrime.gov.in"]
#       - draft:     {"en": ..., "hi": ...}, a simple fill-in-the-blanks
#                    template in English and Hindi
#
#   Regexes to write (use Python's "re" module):
#     - UPI ID: something@handle (e.g. name123@okaxis)
#     - UTR: a number of exactly 12 digits
#     - Amount: ₹ or "Rs" or "INR" followed by a number (allow commas,
#       e.g. ₹1,25,000)
#     - Phone (optional): a 10-digit Indian mobile number starting with 6–9
#
# TALKS TO:
#   - main.py → calls triage() when analyze_incident() raises an error
#   - data.py → the category codes
#
# STEPS:
#   1. Write and test each regex alone, in the Python shell or on regex101.com
#      (choose the "Python" flavour), with fake examples.
#   2. Write triage(), which runs each regex with re.search(...).
#   3. Add the keyword → category guess (text.lower() and the "in" operator).
#   4. Build missingFields, actions and the draft templates (f-strings).
#   5. Test it by removing your Gemini key from agent/.env and submitting a
#      report.
#
# CONCEPTS TO LEARN:
#   - Regular expressions with Python's re module (re.search, groups, \d{12})
#   - Python dicts and lists
#   - f-strings for the draft text
# =============================================================================

import re


# ---------------------------------------------------------------------------
# Regexes
# ---------------------------------------------------------------------------
RE_UPI_ID = re.compile(r"[a-zA-Z0-9.\-_]+@[a-zA-Z]{2,}")
RE_UTR = re.compile(r"\b\d{12}\b")
RE_AMOUNT = re.compile(r"(?:₹|Rs\.?|INR)\s*([\d,]+(?:\.\d{1,2})?)", re.IGNORECASE)
RE_PHONE = re.compile(r"\b[6-9]\d{9}\b")


# ---------------------------------------------------------------------------
# Keyword → category mapping
# ---------------------------------------------------------------------------
KEYWORD_MAP = [
    (["upi", "gpay", "phonepe", "paytm", "bhim", "google pay"], "UPI"),
    (["debit card", "credit card", "atm", "card number", "cvv"],  "CARD"),
    (["phishing", "fake link", "otp", "fake website", "fake site"], "PHISH"),
    (["impersonat", "digital arrest", "fake police", "fake officer", "customer care fraud"], "IMPERS"),
    (["invest", "trading", "stock", "crypto", "bitcoin", "mutual fund scam"], "INVEST"),
    (["job", "task scam", "work from home", "part time"],          "JOB"),
    (["loan app", "loan harassment", "lending app"],               "LOAN"),
    (["sextort", "nude", "video call blackmail", "intimate"],      "SEXT"),
    (["instagram hack", "facebook hack", "social media", "fake profile", "account hack"], "SOCIAL"),
    (["aadhaar", "aadhar", "pan card", "identity theft", "pan misuse"], "IDENT"),
    (["shopping", "flipkart", "amazon", "online order", "delivery fraud"], "SHOP"),
]


def _guess_category(text: str) -> str:
    """Guess the fraud category from keywords in the text."""
    lower = text.lower()
    for keywords, code in KEYWORD_MAP:
        for kw in keywords:
            if kw in lower:
                return code
    return "OTHER"


def _parse_amount(raw: str) -> float | None:
    """Remove commas from a matched amount string and return a float."""
    try:
        return float(raw.replace(",", ""))
    except (ValueError, AttributeError):
        return None


# ---------------------------------------------------------------------------
# Main fallback function
# ---------------------------------------------------------------------------

def triage(text: str) -> dict:
    """
    Offline triage using regexes and keyword matching.
    Returns a dict with the same shape as Gemini's Analysis output.
    """
    text = text or ""

    # --- extract details with regexes ---
    upi_match = RE_UPI_ID.search(text)
    utr_match = RE_UTR.search(text)
    amount_match = RE_AMOUNT.search(text)
    phone_match = RE_PHONE.search(text)

    suspect_upi_id = upi_match.group(0) if upi_match else None
    utr = utr_match.group(0) if utr_match else None
    amount = _parse_amount(amount_match.group(1)) if amount_match else None
    suspect_phone = phone_match.group(0) if phone_match else None

    details = {
        "suspectName": None,
        "suspectPhone": suspect_phone,
        "suspectUpiId": suspect_upi_id,
        "bank": None,
        "utr": utr,
        "amount": amount,
        "paymentApp": None,
        "dateTime": None,
    }

    # --- missing fields ---
    missing_fields = [key for key, val in details.items() if val is None]

    # --- category ---
    category = _guess_category(text)

    # --- urgency ---
    urgency = "critical" if amount is not None else "medium"

    # --- actions (fixed safe list) ---
    actions = [
        "Call 1930 (National Cyber Crime Helpline) now",
        "Call your bank immediately to block the account/card",
        "Report at https://cybercrime.gov.in",
        "Preserve all evidence — screenshots, messages, transaction IDs",
        "Do NOT share any OTP, PIN or password with anyone",
    ]

    # --- draft complaint templates ---
    amount_str = f"₹{amount:,.2f}" if amount else "[amount not provided]"
    upi_str = suspect_upi_id or "[UPI ID not provided]"
    utr_str = utr or "[UTR not provided]"

    draft_en = (
        f"To,\nThe Cyber Crime Cell\n\n"
        f"Subject: Complaint regarding online fraud\n\n"
        f"I wish to report a case of suspected cyber fraud. "
        f"An amount of {amount_str} was involved. "
        f"The suspect's UPI ID is {upi_str} and the transaction reference (UTR) is {utr_str}. "
        f"I request you to kindly investigate and take necessary action.\n\n"
        f"Details of the incident:\n{text}\n\n"
        f"Thank you."
    )

    draft_hi = (
        f"सेवा में,\nसाइबर क्राइम सेल\n\n"
        f"विषय: ऑनलाइन धोखाधड़ी की शिकायत\n\n"
        f"मैं एक संदिग्ध साइबर धोखाधड़ी की रिपोर्ट करना चाहता/चाहती हूँ। "
        f"इसमें {amount_str} की राशि शामिल है। "
        f"संदिग्ध का UPI ID {upi_str} है और लेन-देन संदर्भ (UTR) {utr_str} है। "
        f"कृपया जाँच करें और आवश्यक कार्रवाई करें।\n\n"
        f"घटना का विवरण:\n{text}\n\n"
        f"धन्यवाद।"
    )

    return {
        "transcript": "",
        "category": category,
        "urgency": urgency,
        "details": details,
        "missingFields": missing_fields,
        "actions": actions,
        "draft": {"en": draft_en, "hi": draft_hi},
    }
