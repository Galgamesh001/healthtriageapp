"""
Tests for triage.py — the rule-based triage logic.

Organized in three groups:
  1. check_red_flags() — phrase-based emergency detection per category
  2. check_sepsis_combo() / sepsis handling — the one combination rule
  3. determine_level() — severity/duration -> triage level

Run with:  pytest -v
"""
import pytest
from triage import check_red_flags, check_sepsis_combo, determine_level, RED_FLAGS


# ---------------------------------------------------------------------------
# 1. Red flag detection — one representative phrase per category
# ---------------------------------------------------------------------------

# Build (category, sample_phrase) pairs directly from RED_FLAGS so this test
# stays in sync automatically if phrases are added/removed later.
CATEGORY_SAMPLES = [(cat, phrases[0]) for cat, phrases in RED_FLAGS.items()]


@pytest.mark.parametrize("category,phrase", CATEGORY_SAMPLES)
def test_red_flag_detected_for_each_category(category, phrase):
    flagged, detected_category = check_red_flags(f"I have {phrase} right now")
    assert flagged is True
    assert detected_category == category


def test_red_flag_matches_regardless_of_case():
    flagged, category = check_red_flags("I HAVE CHEST PAIN AND FEEL DIZZY")
    assert flagged is True
    assert category == "cardiac"


def test_red_flag_matches_as_substring_within_longer_sentence():
    """
    Documents intentional design: phrase matching is substring-based, so a
    red-flag phrase anywhere in a sentence triggers detection. This is the
    safe failure direction (over-flagging) for a medical safety layer.
    """
    flagged, category = check_red_flags(
        "so basically since this morning I've had this awful chest pain "
        "that won't go away and I don't know what's causing it"
    )
    assert flagged is True
    assert category == "cardiac"


def test_no_red_flag_for_clearly_benign_text():
    flagged, category = check_red_flags("I have a mild headache and feel a bit tired")
    assert flagged is False
    assert category is None


def test_self_harm_phrase_is_detected():
    """Self-harm language must never fail to flag — this is the highest-stakes category."""
    flagged, category = check_red_flags("I don't want to live anymore")
    assert flagged is True
    assert category == "self_harm"


def test_self_harm_negation_still_flags_by_design():
    """
    'not hurting myself' still contains 'hurting myself' and will flag true.
    This is a false positive, but it's the correct failure direction for a
    safety layer — flag the ambiguous case rather than risk missing a real one.
    """
    flagged, category = check_red_flags("I promise I am not hurting myself")
    assert flagged is True
    assert category == "self_harm"


# ---------------------------------------------------------------------------
# 2. Sepsis combination rule
# ---------------------------------------------------------------------------

def test_sepsis_combo_requires_both_fever_and_confusion():
    assert check_sepsis_combo("I have a fever and I feel confused") is True


def test_sepsis_combo_false_with_fever_only():
    assert check_sepsis_combo("I have a fever but otherwise feel fine") is False


def test_sepsis_combo_false_with_confusion_only():
    assert check_sepsis_combo("I feel a bit disoriented today") is False


def test_mottled_skin_flags_sepsis_alone():
    flagged, category = check_red_flags("my skin looks mottled skin and cold")
    assert flagged is True
    assert category == "sepsis"


def test_sepsis_combo_flags_via_check_red_flags():
    flagged, category = check_red_flags("burning up with a fever and can't think straight")
    assert flagged is True
    assert category == "sepsis"


def test_sepsis_checked_before_other_categories_when_both_present():
    """
    Pins down the documented priority order: sepsis is checked first, so if
    text matches both sepsis and another category, sepsis wins.
    """
    text = "I have chest pain, a fever, and I'm confused and disoriented"
    flagged, category = check_red_flags(text)
    assert flagged is True
    assert category == "sepsis"


# ---------------------------------------------------------------------------
# 3. determine_level() — severity/duration -> triage level
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("duration", ["less_than_3", "more_than_3", "unknown", None])
def test_severe_severity_is_always_urgent_regardless_of_duration(duration):
    assert determine_level("severe", duration) == "urgent"


def test_moderate_with_long_duration_is_contact():
    assert determine_level("moderate", "more_than_3") == "contact"


def test_moderate_with_short_duration_is_monitor():
    assert determine_level("moderate", "less_than_3") == "monitor"


def test_mild_severity_is_monitor():
    assert determine_level("mild", "less_than_3") == "monitor"
    assert determine_level("mild", "more_than_3") == "monitor"


def test_unrecognized_severity_falls_back_to_monitor():
    """Documents current behavior: any severity string other than 'severe'
    or 'moderate' silently resolves to 'monitor'."""
    assert determine_level("unknown_value", "more_than_3") == "monitor"


def test_severity_case_is_normalized():
    """
    Regression test for a real bug: determine_level() previously did not
    lowercase `severity` the way check_red_flags() lowercases its text,
    so "Severe" (any non-lowercase casing) silently fell through to
    "monitor" instead of "urgent" — the wrong direction for a
    safety-critical default. Fixed by normalizing case at the top of
    determine_level(). This test locks that fix in.
    """
    assert determine_level("Severe", "less_than_3") == "urgent"
    assert determine_level("SEVERE", "less_than_3") == "urgent"
    assert determine_level(None, "less_than_3") == "monitor"  # still safe with no input
