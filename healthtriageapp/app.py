from flask import Flask, render_template, request
from triage import check_red_flags, determine_level

app = Flask(__name__)


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
    level = determine_level(severity, duration)
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
