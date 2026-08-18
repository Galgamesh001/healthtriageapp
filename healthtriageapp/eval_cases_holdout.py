# eval_cases_holdout.py
# A SEPARATE batch of red-flag phrasings, written without checking
# against the current keyword list. This tests generalization rather
# than memorization of the exact phrases already tuned for.

HOLDOUT_CASES = [
    ("There's a crushing feeling right in the middle of my chest", True, "cardiac"),
    ("I can't lift my right arm properly and I sound funny when I talk", True, "stroke"),
    ("I'm struggling to get air in, like I'm suffocating", True, "breathing"),
    ("The cut on my leg is gushing blood and I can't get it to slow down", True, "bleeding_injury"),
    ("He just collapsed and won't respond to me shaking him", True, "neurological"),
    ("She's burning up and doesn't seem to know where she is", True, "sepsis"),
    ("My lips feel huge and tight and it's getting hard to swallow", True, "anaphylaxis"),
    ("I don't see the point in going on anymore", True, "self_harm"),

    ("I've had a dull ache in my lower back for a couple of days", False, None),
    ("Bit of a sore throat, nothing major", False, None),
    ("I've felt a little dizzy after standing up quickly today", False, None),
    ("Small bruise on my knee from bumping into the table", False, None),
]