import time
from datetime import datetime

import pandas as pd
import streamlit as st

from utils import model as M
from utils.ui import cols, embed, md, page_title, scroll_to

PRESETS = {
    "healthy": dict(age=34, sex="Male", cp="non-anginal", trestbps=116, chol=170, chol_unknown=False, fbs="No",
                    restecg="normal", thalch=178, exang="No", oldpeak=0.0, slope="Upsloping", ca="0", thal="Normal"),
    "risky": dict(age=62, sex="Male", cp="asymptomatic", trestbps=158, chol=286, chol_unknown=False, fbs="Yes",
                  restecg="ST-T abnormality", thalch=108, exang="Yes", oldpeak=2.8, slope="Flat", ca="2", thal="Reversible defect"),
    "default": dict(age=50, sex="Male", cp="atypical angina", trestbps=125, chol=210, chol_unknown=False, fbs="No",
                    restecg="normal", thalch=150, exang="No", oldpeak=1.0, slope="Don't know", ca="Don't know", thal="Don't know"),
}


def _apply(name: str):
    for k, v in PRESETS[name].items():
        st.session_state[f"f_{k}"] = v
    st.session_state.pop("result", None)


def _init():
    if "f_age" not in st.session_state:
        _apply("default")
    st.session_state.setdefault("history", [])


def _collect() -> dict:
    g = lambda k: st.session_state[f"f_{k}"]
    yn = lambda x: {"Yes": "yes", "No": "no"}.get(x)
    return dict(
        age=int(g("age")), sex=g("sex").lower(), cp=g("cp"),
        trestbps=int(g("trestbps")),
        chol=None if g("chol_unknown") else int(g("chol")),
        fbs=yn(g("fbs")), restecg=g("restecg").lower(),
        thalch=int(g("thalch")), exang=yn(g("exang")), oldpeak=float(g("oldpeak")),
        slope=None if g("slope") == "Don't know" else g("slope").lower(),
        ca=None if g("ca") == "Don't know" else float(g("ca")),
        thal=None if g("thal") == "Don't know" else g("thal").lower().replace("reversible", "reversable"),
    )


def _panel(icon, title):
    md(f'<div class="panel-title"><span>{icon}</span>{title}</div>')


def render():
    _init()
    if M.load_pipeline() is None:
        st.error("Model file not found. Please run `python train_model.py` once, then reload this page.")
        return

    page_title("AI Heart Check", "Check your heart health",
               "Fill in the details below. Hover over the ⓘ icons for simple explanations — and choose “Don't know” if you're unsure.")

    main, side = cols([2.2, 1], gap="large")

    with side:
        md("""<div class="side-note"><h4>⚡ Quick start</h4><p style="margin:0 0 .6rem;font-size:.9rem;color:var(--muted)">Try an example to see how results look:</p></div>""")
        c1, c2 = st.columns(2)
        c1.button("😊 Healthy", on_click=_apply, args=("healthy",), use_container_width=True)
        c2.button("⚠️ Risky", on_click=_apply, args=("risky",), use_container_width=True)
        st.button("↺ Reset form", on_click=_apply, args=("default",), use_container_width=True)
        md("""<div class="side-note" style="margin-top:1rem"><h4>📋 Where to find values?</h4><ul>
            <li><b>BP</b>: pharmacy or home monitor</li><li><b>Cholesterol</b>: lipid profile blood test</li>
            <li><b>Sugar</b>: fasting glucose test</li><li><b>ECG, ST, vessels</b>: cardiology reports</li></ul></div>
            <div class="side-note" style="margin-top:1rem;background:linear-gradient(160deg,#fff,#ffe9ed)"><h4>🔒 Private</h4>
            <p style="margin:0;font-size:.9rem;color:var(--muted)">Nothing you enter is uploaded or stored on a server.</p></div>""")

    with main:
        with st.container(key="card_about"):
            _panel("🧑", "About you")
            a, b, n = st.columns([1.3, 1, 1.2])
            a.slider("Age (years)", 20, 90, key="f_age")
            b.selectbox("Sex", ["Male", "Female"], key="f_sex")
            n.text_input("Name (optional, for report)", key="f_name", placeholder="e.g. Abhishek")

        with st.container(key="card_vitals"):
            _panel("🩸", "Vitals & blood tests")
            a, b = st.columns(2)
            a.number_input("Resting blood pressure (mm Hg)", 80, 220, key="f_trestbps",
                           help="Top number (systolic) when relaxed. Normal is below 120.")
            with b:
                st.number_input("Cholesterol (mg/dL)", 100, 600, key="f_chol",
                                disabled=st.session_state.get("f_chol_unknown", False),
                                help="Total cholesterol from a lipid profile. Desirable is below 200.")
                st.checkbox("I don't know my cholesterol", key="f_chol_unknown")
            a, b = st.columns(2)
            a.selectbox("Fasting blood sugar above 120 mg/dL?", ["No", "Yes", "Don't know"], key="f_fbs",
                        help="Blood sugar after 8+ hours without food. 'Yes' can indicate pre-diabetes/diabetes.")
            b.slider("Highest heart rate reached (bpm)", 60, 210, key="f_thalch",
                     help="Max pulse during exercise or a stress test. If unsure, use about 220 minus your age.")

        with st.container(key="card_heart"):
            _panel("🫀", "Heart tests & symptoms")
            a, b = st.columns(2)
            a.selectbox("Chest pain type", ["typical angina", "atypical angina", "non-anginal", "asymptomatic"], key="f_cp",
                        help="Typical: pressure/tightness with effort · Atypical: partly heart-like · Non-anginal: not heart-related · Asymptomatic: no chest pain")
            b.selectbox("Resting ECG result", ["normal", "lv hypertrophy", "ST-T abnormality"], key="f_restecg",
                        help="Result of an electrocardiogram taken at rest.")
            a, b = st.columns(2)
            a.selectbox("Chest pain during exercise?", ["No", "Yes"], key="f_exang", help="Angina brought on by physical effort.")
            b.slider("ST depression (oldpeak)", 0.0, 6.5, step=0.1, key="f_oldpeak",
                     help="How much the ECG ST segment drops during exercise compared with rest. 0 is best.")
            a, b, c = st.columns(3)
            a.selectbox("ST slope at peak exercise", ["Upsloping", "Flat", "Downsloping", "Don't know"], key="f_slope")
            b.selectbox("Major vessels coloured (0–3)", ["0", "1", "2", "3", "Don't know"], key="f_ca",
                        help="Number of major blood vessels showing narrowing on fluoroscopy.")
            c.selectbox("Thalassemia test", ["Normal", "Fixed defect", "Reversible defect", "Don't know"], key="f_thal")

        go = st.button("🔍  Analyse my heart health", type="primary", use_container_width=True)

    md('<div id="results-anchor"></div>')
    holder = st.empty()

    if go:
        values = _collect()
        with holder.container():
            embed("scanner.html", 430, MS=4300)
            scroll_to("results-anchor")
        time.sleep(4.4)
        holder.empty()
        prob = M.predict_probability(values)
        level = M.risk_level(prob)
        factors = M.analyze(values)
        recs = M.recommendations(level, factors)
        st.session_state["result"] = dict(values=values, prob=prob, level=level, factors=factors, recs=recs,
                                          name=st.session_state.get("f_name", "").strip(),
                                          time=datetime.now().strftime("%d %b, %I:%M %p"), fresh=True)
        st.session_state["history"].append(dict(
            Time=st.session_state["result"]["time"], Name=st.session_state["result"]["name"] or "—",
            Age=values["age"], Sex=values["sex"].title(), BP=values["trestbps"],
            Cholesterol=values["chol"] if values["chol"] is not None else "—",
            Risk=f"{prob*100:.0f}%", Level=M.LEVEL_TEXT[level][0].title()))

    res = st.session_state.get("result")
    if res:
        with holder.container():
            _show(res)
        if res.pop("fresh", False):
            scroll_to("results-anchor")

    if st.session_state["history"]:
        with st.expander(f"🕘 Session history ({len(st.session_state['history'])} checks)"):
            df = pd.DataFrame(st.session_state["history"])
            st.dataframe(df, use_container_width=True, hide_index=True)
            d, e = st.columns(2)
            d.download_button("⬇ Export history (CSV)", df.to_csv(index=False).encode(), "heart_check_history.csv", "text/csv", use_container_width=True)
            e.button("🗑 Clear history", on_click=lambda: st.session_state.update(history=[]), use_container_width=True)


def _show(res):
    prob, level = res["prob"], res["level"]
    badge, title, text = M.LEVEL_TEXT[level]
    pct = round(prob * 100)
    who = f"{res['name']}, " if res["name"] else ""
    md(f"""
    <div class="result-hero {level}">
      <div class="gauge"><div class="ring" style="--p:{pct}"></div><div class="num"><b>{pct}%</b><span>risk score</span></div></div>
      <div><span class="badge">{badge}</span><h2>{who}{title}</h2><p>{text}</p></div>
    </div>""")

    md('<div class="sec-head" style="margin:2rem auto 1rem"><div class="eyebrow">YOUR READINGS</div><h2 style="font-size:1.6rem!important">What your numbers say</h2></div>')
    label = {"ok": "Normal", "warn": "Watch", "bad": "Attention"}
    items = "".join(
        f'<div class="factor" style="animation-delay:{i*0.06}s"><div class="fi">{ic}</div><div><b>{t}</b><small>{d}</small></div><span class="st {s}">{label[s]}</span></div>'
        for i, (ic, t, d, s) in enumerate(res["factors"]))
    md(f'<div class="grid g2">{items}</div>')

    n_bad = sum(1 for f in res["factors"] if f[3] == "bad")
    n_warn = sum(1 for f in res["factors"] if f[3] == "warn")
    n_ok = len(res["factors"]) - n_bad - n_warn
    md(f"""<div class="grid g3" style="margin-top:1.2rem">
      <div class="metric-big"><b style="color:var(--green)">{n_ok}</b><span>Healthy readings</span></div>
      <div class="metric-big"><b style="color:var(--amber)">{n_warn}</b><span>Need watching</span></div>
      <div class="metric-big"><b style="color:var(--red)">{n_bad}</b><span>Need attention</span></div></div>""")

    md('<div class="sec-head" style="margin:2rem auto 1rem"><div class="eyebrow">YOUR PLAN</div><h2 style="font-size:1.6rem!important">Recommended next steps</h2></div>')
    cards = "".join(f'<div class="card"><div class="ico">{ic}</div><h3>{t}</h3><p>{d}</p></div>' for ic, t, d in res["recs"][:6])
    md(f'<div class="grid g3">{cards}</div>')

    metrics = M.load_metrics()
    if metrics.get("importance"):
        top = metrics["importance"][:6]
        mx = max(i["importance"] for i in top) or 1
        rows = "".join(
            f'<div class="row"><span>{M.FEATURE_LABELS[i["feature"]]}</span><div class="t"><i style="width:{i["importance"]/mx*100:.0f}%"></i></div><b>{i["importance"]/mx*100:.0f}</b></div>'
            for i in top)
        md(f'<div class="card bars" style="margin-top:1.2rem"><h3>🧠 What the AI pays most attention to</h3><p style="margin-bottom:.6rem">Overall importance of each feature in the model (relative score).</p>{rows}</div>')

    report = M.build_report_html(res["name"], res["values"], prob, level, res["factors"], res["recs"])
    d1, d2 = st.columns(2)
    d1.download_button("📄 Download report (HTML – print to PDF)", report.encode("utf-8"), "heart_health_report.html", "text/html", use_container_width=True)
    d2.markdown('<a class="btn ghost" style="width:100%;justify-content:center;box-sizing:border-box" href="?page=tips" target="_self">🥗 Get heart-healthy tips</a>', unsafe_allow_html=True)
    md('<div class="disclaimer">⚠️ <b>Important:</b> This result comes from a demonstration machine-learning model and is <b>not a medical diagnosis</b>. If you have chest pain, breathlessness or fainting, call your emergency number immediately.</div>')
