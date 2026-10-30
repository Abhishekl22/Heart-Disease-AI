"""Model loading, prediction and the plain-language health analysis."""
import json
from datetime import datetime
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = ROOT / "model" / "heart_pipeline.pkl"
METRICS_PATH = ROOT / "model" / "metrics.json"

FEATURES = ["age", "trestbps", "chol", "thalch", "oldpeak", "ca",
            "sex", "cp", "fbs", "restecg", "exang", "slope", "thal"]

FEATURE_LABELS = {
    "age": "Age", "sex": "Sex", "cp": "Chest pain type", "trestbps": "Resting blood pressure",
    "chol": "Cholesterol", "fbs": "Fasting blood sugar", "restecg": "Resting ECG",
    "thalch": "Max heart rate", "exang": "Exercise angina", "oldpeak": "ST depression",
    "slope": "ST slope", "ca": "Major vessels", "thal": "Thalassemia",
}


@st.cache_resource(show_spinner=False)
def load_pipeline():
    if not MODEL_PATH.exists():
        return None
    return joblib.load(MODEL_PATH)


@st.cache_data(show_spinner=False)
def load_metrics() -> dict:
    if METRICS_PATH.exists():
        return json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    return {}


def to_frame(v: dict) -> pd.DataFrame:
    """v uses friendly values; unknown values are None."""
    row = {k: (np.nan if v.get(k) is None else v[k]) for k in FEATURES}
    return pd.DataFrame([row], columns=FEATURES)


def predict_probability(v: dict) -> float:
    pipe = load_pipeline()
    return float(pipe.predict_proba(to_frame(v))[0, 1])


def risk_level(p: float) -> str:
    return "low" if p < 0.35 else ("mod" if p < 0.60 else "high")


LEVEL_TEXT = {
    "low": ("LOW RISK", "💚 Your heart looks healthy",
            "Based on the numbers you entered, the model sees a low likelihood of heart disease. "
            "Keep up your healthy habits and continue regular check-ups."),
    "mod": ("MODERATE RISK", "🧡 Some things need attention",
            "A few of your readings are in a borderline range. Small, steady lifestyle changes and a "
            "routine check-up with your doctor can make a real difference."),
    "high": ("HIGH RISK", "❤️‍🩹 Please consult a doctor soon",
             "The model found several patterns that are commonly linked with heart disease. "
             "This is not a diagnosis, but please book a visit with a cardiologist for proper tests."),
}


def analyze(v: dict) -> list:
    """Return a list of (icon, title, detail, status[ok|warn|bad])."""
    out = []
    bp = v["trestbps"]
    if bp < 120:
        out.append(("🩸", f"Blood pressure {bp} mmHg", "In the normal range — great.", "ok"))
    elif bp < 140:
        out.append(("🩸", f"Blood pressure {bp} mmHg", "Slightly elevated. Cut salt, stay active and re-check regularly.", "warn"))
    else:
        out.append(("🩸", f"Blood pressure {bp} mmHg", "High (hypertension range). Please get it checked by a doctor.", "bad"))

    ch = v.get("chol")
    if ch is not None:
        if ch < 200:
            out.append(("🧪", f"Cholesterol {ch} mg/dL", "Desirable level.", "ok"))
        elif ch < 240:
            out.append(("🧪", f"Cholesterol {ch} mg/dL", "Borderline high. Reduce fried & processed food, add fibre.", "warn"))
        else:
            out.append(("🧪", f"Cholesterol {ch} mg/dL", "High. A lipid profile and doctor advice are recommended.", "bad"))
    else:
        out.append(("🧪", "Cholesterol unknown", "Consider getting a lipid profile test — it is quick and inexpensive.", "warn"))

    age, hr = v["age"], v["thalch"]
    target = 220 - age
    pct = hr / target * 100
    if pct >= 85:
        out.append(("💓", f"Max heart rate {hr} bpm", f"{pct:.0f}% of your age-predicted maximum ({target}) — good exercise capacity.", "ok"))
    elif pct >= 70:
        out.append(("💓", f"Max heart rate {hr} bpm", f"{pct:.0f}% of the age-predicted maximum ({target}). Build fitness gradually.", "warn"))
    else:
        out.append(("💓", f"Max heart rate {hr} bpm", f"Only {pct:.0f}% of the age-predicted maximum ({target}). Low exercise capacity can be a warning sign.", "bad"))

    if v["oldpeak"] < 1:
        out.append(("📈", f"ST depression {v['oldpeak']}", "Within the normal range.", "ok"))
    elif v["oldpeak"] <= 2:
        out.append(("📈", f"ST depression {v['oldpeak']}", "Mildly raised after exercise — discuss with your doctor.", "warn"))
    else:
        out.append(("📈", f"ST depression {v['oldpeak']}", "Markedly raised; this is strongly linked with reduced blood flow to the heart.", "bad"))

    if v["exang"] == "yes":
        out.append(("🏃", "Chest pain during exercise", "Exercise-induced angina is an important warning sign.", "bad"))
    else:
        out.append(("🏃", "No chest pain during exercise", "Good sign.", "ok"))

    cp = v["cp"]
    cp_map = {
        "typical angina": ("Typical angina", "Classic heart-related chest pain. Medical evaluation is advised.", "bad"),
        "atypical angina": ("Atypical angina", "Chest pain that only partly matches heart pain. Worth mentioning to your doctor.", "warn"),
        "non-anginal": ("Non-anginal pain", "Pain that is usually not heart-related.", "ok"),
        "asymptomatic": ("No chest-pain symptoms", "Many heart problems are silent, so keep up regular screening.", "warn"),
    }
    t, d, s = cp_map[cp]
    out.append(("😮‍💨", t, d, s))

    if v["fbs"] == "yes":
        out.append(("🍬", "Fasting sugar above 120", "May point to pre-diabetes or diabetes, a major heart-risk factor.", "warn"))
    elif v["fbs"] == "no":
        out.append(("🍬", "Fasting sugar normal", "Good blood sugar control.", "ok"))

    if v["restecg"] != "normal":
        out.append(("📟", "Resting ECG not normal", "An abnormal ECG deserves a cardiologist's opinion.", "warn"))
    else:
        out.append(("📟", "Resting ECG normal", "No abnormal rhythm or strain detected.", "ok"))

    if v.get("ca") is not None and v["ca"] >= 1:
        out.append(("🫀", f"{int(v['ca'])} major vessel(s) narrowed", "Blocked vessels are a strong risk signal.", "bad"))
    if v.get("thal") in ("fixed defect", "reversable defect"):
        out.append(("☢️", "Thalassemia test abnormal", "A defect on the stress test can indicate poor blood supply.", "warn" if v["thal"] == "fixed defect" else "bad"))
    if v.get("slope") in ("flat", "downsloping"):
        out.append(("↘️", f"ST slope {v['slope']}", "A flat or downward slope during peak exercise is less healthy.", "warn"))

    if age >= 65:
        out.append(("🎂", f"Age {age}", "Risk naturally rises with age — regular check-ups matter more.", "warn"))
    return out


def recommendations(level: str, factors: list) -> list:
    recs = []
    titles = " ".join(f[1] for f in factors if f[3] != "ok").lower()
    if "blood pressure" in titles:
        recs.append(("🧂", "Control blood pressure", "Keep salt under 5 g a day, eat potassium-rich foods (banana, spinach) and measure BP weekly."))
    if "cholesterol" in titles:
        recs.append(("🥗", "Improve cholesterol", "Choose oats, nuts, fish and olive oil; avoid trans-fats, bakery and deep-fried snacks."))
    if "fasting sugar" in titles:
        recs.append(("🍬", "Watch blood sugar", "Cut sugary drinks and white flour; ask for an HbA1c test."))
    if "heart rate" in titles or "exercise" in titles:
        recs.append(("🚶", "Build fitness slowly", "Start with 20 minutes of brisk walking and increase to 150 minutes a week — only after your doctor says it is safe."))
    recs.append(("😴", "Sleep & stress", "Aim for 7–8 hours of sleep. Try 10 minutes of deep breathing or meditation daily."))
    recs.append(("🚭", "Avoid smoking & limit alcohol", "Quitting smoking cuts heart-attack risk by half within a year."))
    if level == "high":
        recs.insert(0, ("👨‍⚕️", "See a cardiologist", "Book an appointment soon and ask about an ECG, echo and treadmill test."))
    elif level == "mod":
        recs.insert(0, ("📅", "Schedule a check-up", "Plan a routine health check within the next 1–3 months."))
    else:
        recs.insert(0, ("✅", "Keep it up", "Repeat this screening once a year or whenever your health changes."))
    return recs


def build_report_html(name: str, v: dict, prob: float, level: str, factors: list, recs: list) -> str:
    badge, title, text = LEVEL_TEXT[level]
    color = {"low": "#18a864", "mod": "#e08a00", "high": "#e5384f"}[level]
    rows = "".join(
        f"<tr><td>{i} {t}</td><td>{d}</td><td style='color:{ {'ok':'#18a864','warn':'#e08a00','bad':'#e5384f'}[s] };font-weight:700'>{ {'ok':'Normal','warn':'Watch','bad':'Attention'}[s] }</td></tr>"
        for i, t, d, s in factors)
    rec_html = "".join(f"<li><b>{t}:</b> {d}</li>" for _, t, d in recs)
    now = datetime.now().strftime("%d %b %Y, %I:%M %p")
    return f"""<!DOCTYPE html><html><head><meta charset='utf-8'><title>Heart Health Report</title>
<style>body{{font-family:Segoe UI,Arial,sans-serif;max-width:820px;margin:30px auto;color:#27495a;padding:0 20px}}
h1{{color:#0aa5b8;margin-bottom:0}}.box{{border-left:8px solid {color};background:#f3fafc;padding:16px 20px;border-radius:10px;margin:18px 0}}
table{{border-collapse:collapse;width:100%}}td,th{{border-bottom:1px solid #d8e9ee;padding:9px;text-align:left;font-size:14px}}
th{{background:#e8f6f8}}small{{color:#6a8794}}</style></head><body>
<h1>❤ HeartGuard AI — Health Report</h1><small>Generated {now}{(' · Patient: ' + name) if name else ''}</small>
<div class='box'><h2 style='margin:0;color:{color}'>{badge} — {prob*100:.0f}%</h2><p>{title}<br>{text}</p></div>
<h3>Your readings explained</h3><table><tr><th>Factor</th><th>What it means</th><th>Status</th></tr>{rows}</table>
<h3>Recommended next steps</h3><ul>{rec_html}</ul>
<p><small>⚠ This report comes from a demonstration machine-learning model. It is not a medical diagnosis and is no substitute for professional advice.</small></p>
</body></html>"""
