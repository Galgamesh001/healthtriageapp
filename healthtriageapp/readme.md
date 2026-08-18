# HealthGuide — Symptom Triage Prototype

**Educational prototype — not a medical diagnostic tool.**

HealthGuide is a small web application that demonstrates how a
symptom-triage system might help someone decide what level of care
they need — without diagnosing conditions or replacing professional
medical judgement.

## What it does

1. User describes their symptoms in free text
2. A red-flag safety layer checks for language associated with
   medical emergencies (see `SOURCES.md`)
3. If a red flag is detected, the user is immediately directed to
   appropriate emergency guidance  bypassing further questions
4. Otherwise, the user answers two follow-up questions (severity,
   duration)
5. A rule-based triage level is returned: monitor / contact a
   professional / seek urgent care

## Why this exists

This project explores whether a lightweight, transparent, rule-based
system can meaningfully help people choose an appropriate level of
care  while being explicit and honest about what such a system
can and cannot safely do.

## Tech stack

- Python / Flask (backend, routing)
- HTML/CSS (frontend)
- Rule-based logic in `triage.py`, kept separate from Flask so it
  can be tested independently

## Project structure
