from flask import Flask, render_template, request

app = Flask(__name__)

# Red-flag keyword groups, adapted from NHS 999/A&E guidance
# Sources: nhs.uk "When to call 999", "When to go to A&E",
# NHS stroke FAST campaign (nidirect.gov.uk), sepsis/anaphylaxis
# guidance summarised by NHS-affiliated GP practice pages.
# Last reviewed: [today's date] — cite these in your project docs.

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

def check_red_flags(text):
    text = text.lower()

    if "mottled skin" in text or check_sepsis_combo(text):
        return True, "sepsis"

    for category, phrases in RED_FLAGS.items():
        for phrase in phrases:
            if phrase in text:
                return True, category

    return False, None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/check", methods=["POST"])
def check():
    symptoms_text = request.form.get("symptoms", "").lower()
    red_flag_hit, category = check_red_flags(symptoms_text)

    if red_flag_hit:
        return render_template(
            "result.html",
            symptoms_text=symptoms_text,
            red_flag=True,
            red_flag_category=category
        )

    return render_template("followup.html", symptoms_text=symptoms_text)

@app.route("/result", methods=["POST"])
def result():
    symptoms_text = request.form.get("symptoms_text", "")
    severity = request.form.get("severity")
    duration = request.form.get("duration")

    # Simple rule-based logic — we'll refine this
    if severity == "severe":
        level = "urgent"
    elif severity == "moderate" and duration == "more_than_3":
        level = "contact"
    elif severity == "moderate":
        level = "monitor"
    else:
        level = "monitor"

    return render_template(
        "result.html",
        symptoms_text=symptoms_text,
        red_flag=False,
        level=level,
        severity=severity,
        duration=duration
    )

if __name__ == "__main__":
    app.run(debug=True)