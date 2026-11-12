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
#         (e.g. indiacode.nic.in) before writing it. Don't copy from AI or
#         blogs. Cite your source in a comment.
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
