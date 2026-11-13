# =============================================================================
# data.py
# =============================================================================
#
# PURPOSE:
#   Fixed reference data that WE control: fraud categories, legal sections and
#   helplines. Laws and phone numbers are facts, so they must not come from
#   the AI, which could invent a wrong number or section.
#
# WHAT TO BUILD (three lists of dicts, plus two small helper functions):
#
#   1. CATEGORIES: a list of {"code": ..., "label": ...}
#        UPI    → UPI / payment fraud
#        CARD   → Debit or credit card fraud
#        PHISH  → Phishing (fake links, fake websites, OTP theft)
#        IMPERS → Impersonation (fake police, bank, "digital arrest", customer care)
#        INVEST → Investment or trading scam
#        JOB    → Job or "task" scam
#        LOAN   → Loan app harassment
#        SEXT   → Sextortion
#        SOCIAL → Social media account hacking or fake profile
#        IDENT  → Identity theft (Aadhaar/PAN misuse)
#        SHOP   → Online shopping fraud
#        OTHER  → Other
#
#   2. LEGAL_SECTIONS: a list of {"act", "section", "note", "categories"}
#        - note: a one-line plain-English explanation
#        - categories: a list of the category codes it applies to
#      Add these:
#        IT Act 2000: 43, 66, 66C, 66D, 66E, 67, 67A
#        BNS 2023 (which replaced the IPC from 1 July 2024): 78, 308, 318,
#        319, 336, 351
#      ⚠️ Verify every section and note against the actual text of the Act
#         (e.g. indiacode.nic.in) before writing it. Cite your source in a comment.
#
#   3. HELPLINES: a list of {"name", "phone", "url", "categories"}
#        - 1930: National Cyber Crime Helpline (all categories)
#        - cybercrime.gov.in: National Cyber Crime Reporting Portal (all categories)
#        - "Your bank's customer care": the number on the back of your
#          card or on the bank's official website (UPI, CARD, PHISH, ...)
#        - UIDAI 1947: Aadhaar helpline (IDENT)
#        - National Consumer Helpline 1915 (SHOP)
#        - RBI Sachet: sachet.rbi.org.in (INVEST, LOAN; illegal deposit
#          schemes and lenders)
#      ⚠️ Verify each number and link on the official website.
#
#   Helpers:
#     - get_legal_sections(category_code) -> list: the sections whose
#       categories include the code
#     - get_helplines(category_code) -> list: the helplines for that code.
#       Always include 1930 and the portal.
#
# TALKS TO:
#   - main.py         → adds the matching legal sections and helplines to
#                       each result
#   - gemini_agent.py → puts the category codes and labels in the prompt
#   - fallback.py     → uses the category codes
#
# STEPS:
#   1. Write CATEGORIES. It's the easiest, and everyone needs it first.
#   2. Write HELPLINES, checking each number on its official site.
#   3. Research and write LEGAL_SECTIONS, one at a time.
#   4. Write the two helpers with a list comprehension:
#        [item for item in LEGAL_SECTIONS if code in item["categories"]]
#
# CONCEPTS TO LEARN:
#   - Python lists and dicts
#   - List comprehensions
#   - Importing from your own module (from data import CATEGORIES)
# =============================================================================


# ---------------------------------------------------------------------------
# 1. CATEGORIES
# ---------------------------------------------------------------------------
CATEGORIES = [
    {"code": "UPI",    "label": "UPI / payment fraud"},
    {"code": "CARD",   "label": "Debit or credit card fraud"},
    {"code": "PHISH",  "label": "Phishing (fake links, fake websites, OTP theft)"},
    {"code": "IMPERS", "label": "Impersonation (fake police, bank, digital arrest, customer care)"},
    {"code": "INVEST", "label": "Investment or trading scam"},
    {"code": "JOB",    "label": "Job or task scam"},
    {"code": "LOAN",   "label": "Loan app harassment"},
    {"code": "SEXT",   "label": "Sextortion"},
    {"code": "SOCIAL", "label": "Social media account hacking or fake profile"},
    {"code": "IDENT",  "label": "Identity theft (Aadhaar/PAN misuse)"},
    {"code": "SHOP",   "label": "Online shopping fraud"},
    {"code": "OTHER",  "label": "Other"},
]

ALL_CODES = [c["code"] for c in CATEGORIES]


# ---------------------------------------------------------------------------
# 2. LEGAL_SECTIONS
# ---------------------------------------------------------------------------
# Sources:
#   IT Act 2000 — https://indiacode.nic.in/handle/123456789/1999
#   Bharatiya Nyaya Sanhita 2023 — https://indiacode.nic.in/handle/123456789/20062

LEGAL_SECTIONS = [
    # --- IT Act 2000 ---
    {
        "act": "IT Act 2000",
        "section": "43",
        "note": "Penalty for damage to computer, computer system, etc. (unauthorized access, data extraction, virus introduction).",
        "categories": ["UPI", "CARD", "PHISH", "IMPERS", "INVEST", "JOB", "LOAN", "SEXT", "SOCIAL", "IDENT", "SHOP", "OTHER"],
    },
    {
        "act": "IT Act 2000",
        "section": "66",
        "note": "Computer-related offences committed dishonestly or fraudulently (hacking with criminal intent).",
        "categories": ["UPI", "CARD", "PHISH", "SOCIAL", "IDENT", "SHOP"],
    },
    {
        "act": "IT Act 2000",
        "section": "66C",
        "note": "Identity theft — fraudulent use of the electronic signature, password or unique identification feature of another person.",
        "categories": ["PHISH", "IMPERS", "IDENT", "SOCIAL"],
    },
    {
        "act": "IT Act 2000",
        "section": "66D",
        "note": "Cheating by personation using a computer resource or communication device.",
        "categories": ["PHISH", "IMPERS", "INVEST", "JOB", "SHOP"],
    },
    {
        "act": "IT Act 2000",
        "section": "66E",
        "note": "Violation of privacy — intentional capture, publication or transmission of a person's private images without consent.",
        "categories": ["SEXT"],
    },
    {
        "act": "IT Act 2000",
        "section": "67",
        "note": "Publishing or transmitting obscene material in electronic form.",
        "categories": ["SEXT"],
    },
    {
        "act": "IT Act 2000",
        "section": "67A",
        "note": "Publishing or transmitting material containing sexually explicit acts in electronic form.",
        "categories": ["SEXT"],
    },

    # --- BNS 2023 (replaced IPC from 1 July 2024) ---
    {
        "act": "BNS 2023",
        "section": "78",
        "note": "Theft — dishonest taking of movable property (including money) out of a person's possession without consent.",
        "categories": ["UPI", "CARD", "PHISH", "SHOP"],
    },
    {
        "act": "BNS 2023",
        "section": "308",
        "note": "Extortion — intentionally putting a person in fear of injury to obtain property or valuable security.",
        "categories": ["SEXT", "LOAN"],
    },
    {
        "act": "BNS 2023",
        "section": "318",
        "note": "Cheating — deceiving a person and thereby dishonestly inducing delivery of property or alteration/destruction of valuable security.",
        "categories": ["UPI", "CARD", "PHISH", "IMPERS", "INVEST", "JOB", "SHOP"],
    },
    {
        "act": "BNS 2023",
        "section": "319",
        "note": "Cheating by personation — pretending to be another person or using the identity of another to cheat.",
        "categories": ["IMPERS", "PHISH", "SOCIAL", "IDENT"],
    },
    {
        "act": "BNS 2023",
        "section": "336",
        "note": "Forgery — making a false document or electronic record with intent to cause damage or injury, or to support a claim.",
        "categories": ["IDENT", "PHISH", "IMPERS"],
    },
    {
        "act": "BNS 2023",
        "section": "351",
        "note": "Criminal intimidation — threatening a person with injury to person, reputation or property to cause alarm or compel action.",
        "categories": ["SEXT", "LOAN", "IMPERS"],
    },
]


# ---------------------------------------------------------------------------
# 3. HELPLINES
# ---------------------------------------------------------------------------
# Sources: official websites verified as noted below.

HELPLINES = [
    {
        "name": "National Cyber Crime Helpline",
        "phone": "1930",
        "url": "https://cybercrime.gov.in",
        "categories": ALL_CODES,  # all categories
    },
    {
        "name": "National Cyber Crime Reporting Portal",
        "phone": None,
        "url": "https://cybercrime.gov.in",
        "categories": ALL_CODES,  # all categories
    },
    {
        "name": "Your bank's customer care (number on back of card or bank website)",
        "phone": None,
        "url": None,
        "categories": ["UPI", "CARD", "PHISH", "INVEST", "LOAN"],
    },
    {
        # UIDAI toll-free helpline — https://uidai.gov.in/en/contact-support.html
        "name": "UIDAI Aadhaar Helpline",
        "phone": "1947",
        "url": "https://uidai.gov.in",
        "categories": ["IDENT"],
    },
    {
        # National Consumer Helpline — https://consumerhelpline.gov.in
        "name": "National Consumer Helpline",
        "phone": "1915",
        "url": "https://consumerhelpline.gov.in",
        "categories": ["SHOP"],
    },
    {
        # RBI Sachet — https://sachet.rbi.org.in
        "name": "RBI Sachet (illegal deposit schemes & lenders)",
        "phone": None,
        "url": "https://sachet.rbi.org.in",
        "categories": ["INVEST", "LOAN"],
    },
]


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def get_legal_sections(category_code: str) -> list:
    """Return the legal sections whose categories include the given code."""
    return [item for item in LEGAL_SECTIONS if category_code in item["categories"]]


def get_helplines(category_code: str) -> list:
    """Return the helplines for the given category code.
    Always includes 1930 and the portal (they cover all categories)."""
    return [item for item in HELPLINES if category_code in item["categories"]]
