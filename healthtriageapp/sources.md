# Red-flag criteria sources

The red-flag keyword categories in `app.py` are adapted from the
following official guidance. This is a simplified, non-exhaustive
keyword-matching approximation of real clinical triage criteria —
not a clinical tool.

- NHS — "When to call 999"
  https://www.nhs.uk/nhs-services/urgent-and-emergency-care-services/when-to-call-999/

- NHS — "When to go to A&E"
  https://www.nhs.uk/nhs-services/urgent-and-emergency-care-services/when-to-go-to-ae/

- NHS-affiliated GP practice guidance on 999-triggering symptoms
  (heart attack, stroke, breathing, bleeding, seizure) — Humbleyard Practice
  https://www.humbleyard.nhs.uk/home/urgent-appointment/

- Stroke FAST criteria — nidirect (NI government health guidance)
  https://nidirect.gov.uk/node/10349

- Sepsis and anaphylaxis red-flag patterns — summarised from
  clinical guidance referenced by The Women's Health Clinic
  https://thewomenshealth.clinic/faq/what-are-red-flag-symptoms-that-need-urgent-review/

Reviewed: [insert today's date]

## Known limitations

- Keyword matching cannot capture the full range of ways someone
  might describe a symptom (e.g. regional phrasing, typos, indirect
  descriptions).
- This list is not a substitute for validated clinical triage
  criteria such as NHS Pathways or Manchester Triage.
- False negatives (missed red flags) are the most serious failure
  mode and should be tracked explicitly in evaluation (see `/eval`).