# Evaluation Results

## Initial test set (development set)
- Accuracy: 62% → 100% after iterative keyword refinement

## Holdout set (novel phrasing, not used during development)
- Accuracy: 33% (4/12), 8 missed red flags

## Analysis
The gap between 100% on the development set and 33% on the holdout
set demonstrates the core limitation of keyword/phrase matching:
it generalizes well to phrasings it was tuned on, but does not
generalize to genuinely novel ways of describing the same symptom
(e.g. "crushing feeling in the middle of my chest" vs. the tuned
phrase "chest pain").

This is expected behaviour for a rule-based string-matching system
and is the primary reason a production-grade triage tool would need
NLP-based symptom extraction (e.g. embedding-based similarity or a
fine-tuned classifier) rather than exact/substring phrase matching.

## Implication for safety
Missed red flags are the most dangerous failure mode of this system.
This evaluation shows the prototype should not be relied upon as a
safety net for phrasing it hasn't been explicitly tested against —
a limitation clearly disclosed in the app's own messaging.

# Evaluation

## Method

Two separate test sets were used:

1. **Development set** (`eval_cases.py`) — 16 cases used while
   building and iterating on the red-flag keyword lists.
2. **Holdout set** (`eval_cases_holdout.py`) — 12 cases written
   *after* the keyword lists were finalised, deliberately using
   different wording than anything in the keyword lists, to test
   generalisation rather than memorisation.

For both, the key metric tracked is **missed red flags (false
negatives)** — cases where a genuine emergency symptom was not
detected — since this is the most dangerous failure mode for a
triage tool.

## Results

| Test set | Accuracy | Missed red flags |
|---|---|---|
| Development (initial) | 62% (10/16) | 6 |
| Development (after refinement) | 100% (16/16) | 0 |
| Holdout (untuned phrasing) | 33% (4/12) | 8 |
| Holdout (after targeted sepsis fix) | see below | — |

## Analysis

The development set reached 100% only after several rounds of
adding phrase variants directly informed by its own failures — this
is expected and useful for catching bugs, but it does not indicate
the system generalises well.

The holdout set, written independently of the keyword lists,
revealed a large accuracy drop (100% → 33%). Every miss followed
the same pattern: **the underlying symptom was correctly identified
by a human, but expressed in wording not present in the keyword
lists** — e.g. "crushing feeling in the middle of my chest" vs. the
tuned phrase "chest pain," or "struggling to get air in, like I'm
suffocating" vs. "difficulty breathing."

One miss ("burning up and doesn't seem to know where she is")
revealed a genuine gap in the sepsis combination rule's confusion-word
list, which was corrected. This was a targeted, justified fix
rather than a blanket keyword-chase.

## Conclusion

**Keyword/phrase matching reliably catches phrasing it has seen
before, but does not generalise to novel descriptions of the same
symptom.** This is not a fixable bug so much as a structural
limitation of the approach. A production-grade version of this tool
would need semantic similarity (e.g. sentence embeddings) or a
trained classifier to recognise symptom descriptions it hasn't seen
verbatim.

This finding directly shapes the safety framing of the app: users
are told explicitly that the tool may miss emergencies described in
unfamiliar language, and are encouraged to trust their own judgement
and seek help if something feels seriously wrong, regardless of what
the tool says.