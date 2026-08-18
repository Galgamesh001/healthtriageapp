# eval.py
# Runs the triage logic against eval_cases.py and reports results,
# with special attention to MISSED red flags (false negatives) —
# the most dangerous failure mode for a tool like this.

from triage import check_red_flags, determine_level
from eval_cases import RED_FLAG_CASES, TRIAGE_LEVEL_CASES
from eval_cases_holdout import HOLDOUT_CASES

def run_red_flag_eval():
    print("=== Red-flag detection ===\n")
    total = len(RED_FLAG_CASES)
    correct = 0
    missed_red_flags = []      # false negatives — the dangerous ones
    false_alarms = []          # false positives — annoying but safer direction

    for text, expected_flag, expected_category in RED_FLAG_CASES:
        actual_flag, actual_category = check_red_flags(text)
        is_correct = (actual_flag == expected_flag)

        if is_correct:
            correct += 1
        elif expected_flag and not actual_flag:
            missed_red_flags.append(text)
        elif not expected_flag and actual_flag:
            false_alarms.append((text, actual_category))

        status = "PASS" if is_correct else "FAIL"
        print(f"[{status}] \"{text}\" → expected={expected_flag}, got={actual_flag} ({actual_category})")

    print(f"\nAccuracy: {correct}/{total} ({correct/total:.0%})")
    print(f"Missed red flags (false negatives): {len(missed_red_flags)}")
    for m in missed_red_flags:
        print(f"  - \"{m}\"")
    print(f"False alarms (false positives): {len(false_alarms)}")
    for f, cat in false_alarms:
        print(f"  - \"{f}\" (flagged as {cat})")

    return correct, total, missed_red_flags, false_alarms


def run_triage_level_eval():
    print("\n=== Triage level logic ===\n")
    total = len(TRIAGE_LEVEL_CASES)
    correct = 0

    for severity, duration, expected in TRIAGE_LEVEL_CASES:
        actual = determine_level(severity, duration)
        is_correct = (actual == expected)
        if is_correct:
            correct += 1
        status = "PASS" if is_correct else "FAIL"
        print(f"[{status}] severity={severity}, duration={duration} → expected={expected}, got={actual}")

    print(f"\nAccuracy: {correct}/{total} ({correct/total:.0%})")
    return correct, total

def run_holdout_eval():
    print("\n=== Holdout set (untuned phrasing) ===\n")
    total = len(HOLDOUT_CASES)
    correct = 0
    missed = []

    for text, expected_flag, expected_category in HOLDOUT_CASES:
        actual_flag, actual_category = check_red_flags(text)
        is_correct = (actual_flag == expected_flag)
        if is_correct:
            correct += 1
        elif expected_flag and not actual_flag:
            missed.append(text)

        status = "PASS" if is_correct else "FAIL"
        print(f"[{status}] \"{text}\" → expected={expected_flag}, got={actual_flag} ({actual_category})")

    print(f"\nHoldout accuracy: {correct}/{total} ({correct/total:.0%})")
    print(f"Missed on holdout: {len(missed)}")
    for m in missed:
        print(f"  - \"{m}\"")

if __name__ == "__main__":
    run_red_flag_eval()
    run_triage_level_eval()
    run_holdout_eval()

