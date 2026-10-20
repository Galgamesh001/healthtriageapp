# triage.py
# Core triage logic, separated from Flask so it can be tested directly.

# Phrase-based red flags: flagged if any exact phrase appears in the text
RED_FLAGS = {
    "cardiac": [
        "chest pain", "tightness in my chest", "chest tightness",
        "squeezing in my chest", "pressure in my chest",
        "tight feeling in my chest", "tight band", "band across my chest"
    ],
    "stroke": [
        "face drooping", "slurred speech", "can't speak", "cannot speak",
        "arm weakness", "arm feels weak", "weak arm",
        "one side of my face", "difficulty speaking", "trouble speaking",
        "words are coming out wrong", "can't get my words out"
    ],
    "breathing": [
        "can't breathe", "cannot breathe", "difficulty breathing",
        "gasping", "choking", "lips turning blue", "blue lips"
    ],
    "bleeding_injury": [
        "heavy bleeding", "severe bleeding", "won't stop bleeding",
        "bleeding heavily", "bleeding a lot", "losing a lot of blood",
        "deep cut", "severe injury"
    ],
    "neurological": [
        "seizure", "unconscious", "can't wake", "cannot wake up",
        "sudden confusion", "sudden numbness"
    ],
    "anaphylaxis": [
        "throat swelling", "swelling of my throat", "throat is swelling",
        "swelling in my throat", "swollen tongue", "swollen lips",
        "rapid pulse and dizziness"
    ],
    "self_harm": [
        "want to die", "kill myself", "end my life", "ending my life",
        "suicidal", "hurting myself", "don't want to live",
        "no reason to live", "end it all"
    ],
}

# Sepsis is handled separately as a COMBINATION rule rather than fixed
# phrases, since "fever + confusion" can be worded in too many ways
# to list exhaustively.
SEPSIS_FEVER_WORDS = ["fever", "temperature", "burning up"]
SEPSIS_CONFUSION_WORDS = [
    "confused", "confusion", "disoriented", "can't think straight",
    "doesn't know where", "doesn't seem to know", "not making sense"
]


def check_sepsis_combo(text):
    """True if fever-language AND confusion-language both appear."""
    has_fever = any(w in text for w in SEPSIS_FEVER_WORDS)
    has_confusion = any(w in text for w in SEPSIS_CONFUSION_WORDS)
    return has_fever and has_confusion


def check_red_flags(text):
    """Returns (True, category) on first match, else (False, None)."""
    text = text.lower()
    # Check sepsis first: combination rule + the one fixed phrase
    if "mottled skin" in text or check_sepsis_combo(text):
        return True, "sepsis"
    # Then check all the fixed-phrase categories
    for category, phrases in RED_FLAGS.items():
        for phrase in phrases:
            if phrase in text:
                return True, category
    return False, None


def determine_level(severity, duration):
    """Rule-based triage level from follow-up answers."""
    # Normalize case the same way check_red_flags() does for its text input.
    # Without this, "Severe" (any non-lowercase form) silently falls through
    # to "monitor" instead of "urgent" — the wrong direction for a
    # safety-critical default. See test_KNOWN_ISSUE_severity_is_case_sensitive.
    if severity is not None:
        severity = severity.lower()
    if severity == "severe":
        return "urgent"
    elif severity == "moderate" and duration == "more_than_3":
        return "contact"
    elif severity == "moderate":
        return "monitor"
    else:
        return "monitor"
