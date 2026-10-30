from datetime import date

import streamlit as st

from utils import content as C
from utils.ui import md, page_title, section_head


def render():
    page_title("Health Tips & Tools", "Live a heart-healthy life",
               "Simple, doctor-style advice on food, exercise, stress and warning signs — plus free calculators.")

    tip = C.DAILY_TIPS[date.today().toordinal() % len(C.DAILY_TIPS)]
    md(f"""<div class="tip-day fade"><span class="pill" style="color:var(--teal-d)">✨ Tip of the day · {date.today():%d %b %Y}</span>
        <h3>{tip[0]}</h3><p>{tip[1]}</p></div>""")

    t1, t2, t3, t4, t5, t6 = st.tabs(["🌿 Lifestyle", "🥗 Diet", "🏃 Exercise", "🧰 Tools", "🚨 Warning signs", "🧠 Myths & facts"])

    with t1:
        section_head("SIX PILLARS", "Habits that protect your heart")
        cards = "".join(
            f'<div class="card"><div class="ico {cls}">{ic}</div><h3>{t}</h3><p>{d}</p><ul>{"".join(f"<li>{i}</li>" for i in items)}</ul></div>'
            for ic, cls, t, d, items in C.CATEGORIES)
        md(f'<div class="grid g3">{cards}</div>')

    with t2:
        section_head("EAT SMART", "Food for a strong heart")
        more = "".join(f"<li>{i}</li>" for i in C.EAT_MORE)
        less = "".join(f"<li>{i}</li>" for i in C.EAT_LESS)
        md(f"""<div class="grid g2">
          <div class="card" style="border-top:5px solid var(--green)"><h3>✅ Eat more</h3><ul class="check" style="margin:0;padding:0">{more}</ul></div>
          <div class="card" style="border-top:5px solid var(--red)"><h3>⛔ Limit or avoid</h3><ul style="margin:.6rem 0 0 1.1rem">{less}</ul></div></div>""")
        section_head("SAMPLE DAY", "A heart-friendly day of eating")
        meals = "".join(f'<div class="factor"><div class="fi">{m.split()[0]}</div><div><b>{m.split(" ",1)[1]}</b><small>{d}</small></div></div>' for m, d in C.MEAL_PLAN)
        md(f'<div class="grid g2">{meals}</div>')

    with t3:
        section_head("MOVE MORE", "Your simple weekly plan", "Always check with your doctor before starting a new exercise routine.")
        days = "".join(f'<div class="card" style="text-align:center;padding:1.1rem"><div class="tag" style="margin:0 0 .5rem">{d}</div><p style="color:var(--ink)">{a}</p></div>' for d, a in C.WEEK_PLAN[:4])
        days2 = "".join(f'<div class="card" style="text-align:center;padding:1.1rem"><div class="tag" style="margin:0 0 .5rem">{d}</div><p style="color:var(--ink)">{a}</p></div>' for d, a in C.WEEK_PLAN[4:])
        md(f'<div class="grid g4">{days}</div><div class="grid g3" style="margin-top:1.2rem">{days2}</div>')
        md('<div class="disclaimer">💬 <b>Talk test:</b> during moderate exercise you should be able to talk but not sing. Stop immediately if you feel chest pain, dizziness or severe breathlessness.</div>')

    with t4:
        section_head("FREE CALCULATORS", "Health tools")
        a, b = st.columns(2, gap="large")
        with a:
            with st.container(key="card_bmi"):
                md('<div class="panel-title"><span>⚖️</span>BMI calculator</div>')
                w = st.number_input("Weight (kg)", 20.0, 250.0, 70.0, 0.5, key="bmi_w")
                h = st.number_input("Height (cm)", 100.0, 230.0, 170.0, 0.5, key="bmi_h")
                bmi = w / ((h / 100) ** 2)
                cat, col = (("Underweight", "#f5a524") if bmi < 18.5 else ("Healthy weight", "#18a864") if bmi < 25
                            else ("Overweight", "#ef6c3d") if bmi < 30 else ("Obese", "#e5384f"))
                md(f'<div class="metric-big"><b style="color:{col}">{bmi:.1f}</b><span>BMI · <b style="color:{col}">{cat}</b></span></div>')
                lo, hi = 18.5 * (h / 100) ** 2, 24.9 * (h / 100) ** 2
                st.caption(f"Healthy weight for your height: {lo:.0f} – {hi:.0f} kg")
        with b:
            with st.container(key="card_hr"):
                md('<div class="panel-title"><span>💓</span>Target heart-rate zones</div>')
                age = st.slider("Your age", 15, 90, 40, key="hr_age")
                mx = 220 - age
                zones = [("Warm-up", .5, .6, "#5bc0de"), ("Fat-burn / light", .6, .7, "#18a864"),
                         ("Cardio / moderate", .7, .85, "#f5a524"), ("Peak / hard", .85, 1.0, "#e5384f")]
                md(f'<p style="color:var(--muted);margin:.2rem 0 .6rem">Estimated maximum: <b style="color:var(--navy)">{mx} bpm</b></p>' +
                   "".join(f'<div class="zone" style="background:{c}"><span>{n}</span><span>{int(mx*lo)}–{int(mx*hi)} bpm</span></div>' for n, lo, hi, c in zones))
        section_head("KNOW YOUR NUMBERS", "Blood-pressure guide")
        rows = "".join(f'<div class="zone" style="background:{c}"><span>{n}</span><span>{r} mmHg</span></div>' for n, r, c in C.BP_TABLE)
        md(f'<div class="card">{rows}</div>')

    with t5:
        section_head("ACT FAST", "Heart-attack warning signs", "Every minute counts. Do not wait for symptoms to go away.")
        sig = "".join(f'<div class="card"><div class="ico red">{ic}</div><h3>{t}</h3><p>{d}</p></div>' for ic, t, d in C.WARNING_SIGNS)
        md(f'<div class="grid g3">{sig}</div>')
        md("""<div class="sos" style="margin-top:1.4rem"><h3>🚑 If you suspect a heart attack</h3>
            <ul style="margin:0 0 0 1.1rem;line-height:1.9;color:var(--ink)"><li>Call emergency services at once — <b>112</b> (India), <b>911</b> (US), <b>999</b> (UK)</li>
            <li>Sit down, stay calm and loosen tight clothing</li><li>Chew one regular 300 mg aspirin <b>only if</b> you are not allergic and a doctor has not told you otherwise</li>
            <li>Do not drive yourself to the hospital</li></ul></div>""")

    with t6:
        section_head("SEPARATE TRUTH FROM FICTION", "Heart myths & facts")
        for q, a in C.MYTHS:
            with st.expander(f"❓ {q}"):
                st.write(a)
