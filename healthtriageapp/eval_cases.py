# eval_cases.py
# Synthetic test cases with known-correct expected outcomes.
# "expected" is what the red-flag check SHOULD return.
# These are invented example phrasings, not real patient data.

RED_FLAG_CASES = [
    # (input text, expected_red_flag: True/False, expected_category or None)
    ("I have crushing chest pain and pressure", True, "cardiac"),
    ("My face is drooping on one side and I can't speak properly", True, "stroke"),
    ("I can't breathe and my lips are turning blue", True, "breathing"),
    ("I'm bleeding heavily and it won't stop", True, "bleeding_injury"),
    ("I had a seizure and can't wake my friend up", True, "neurological"),
    ("I have a high fever and I'm confused", True, "sepsis"),
    ("My throat is swelling and I'm dizzy", True, "anaphylaxis"),
    ("I've been thinking about ending my life", True, "self_harm"),

    # Trickier phrasing — real people don't always use textbook words
    ("There's a really tight feeling in my chest, like a band", True, "cardiac"),
    ("I feel like I want to die", True, "self_harm"),
    ("My arm feels weak and my words are coming out wrong", True, "stroke"),

    # Should NOT trigger a red flag (mild/non-urgent)
    ("I have a mild headache since this morning", False, None),
    ("My stomach feels a bit upset after lunch", False, None),
    ("I have a scratchy throat and slight cough", False, None),
    ("I feel tired and have a runny nose", False, None),
    ("I twisted my ankle a little while walking", False, None),
]

TRIAGE_LEVEL_CASES = [
    # (severity, duration, expected_level)
    ("severe", "today", "urgent"),
    ("severe", "more_than_3", "urgent"),
    ("moderate", "more_than_3", "contact"),
    ("moderate", "today", "monitor"),
    ("mild", "today", "monitor"),
    ("mild", "more_than_3", "monitor"),
]