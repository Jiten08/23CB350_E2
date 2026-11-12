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
