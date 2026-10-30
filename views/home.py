import streamlit as st

from utils.config import APP_NAME
from utils.model import load_metrics
from utils.ui import cols, data_uri, embed, md, section_head


def render():
    m = load_metrics()
    acc = f"{m.get('accuracy', 0.85) * 100:.0f}%"
    auc = f"{m.get('roc_auc', 0.91):.2f}"
    rows = f"{m.get('total_rows', 920):,}"

    left, right = cols([1.08, 0.92], gap="large", vertical_alignment="center")
    with left:
        md(f"""
        <div class="fade"><span class="pill"><i></i>AI-powered heart screening · free &amp; private</span></div>
        <div class="hero" style="display:block;padding:0">
        <h1 class="fade d1">Know your heart.<br><span class="grad">Protect your life.</span></h1>
        <p class="lead fade d2">{APP_NAME} turns a few simple health numbers into a clear, friendly heart-risk report in under a minute —
        with personal tips to keep your heart strong.</p>
        <div class="btn-row fade d3">
          <a class="btn primary" href="?page=predict" target="_self">❤ Start Heart Check</a>
          <a class="btn ghost" href="?page=tips" target="_self">🥗 Health Tips</a></div></div>""")
    with right:
        embed("hero3d.html", 430)

    md(f"""
    <div class="stats">
      <div class="stat fade d1"><b>{acc}</b><span>Model accuracy</span></div>
      <div class="stat fade d2"><b>{auc}</b><span>ROC-AUC score</span></div>
      <div class="stat fade d3"><b>{rows}</b><span>Patient records learned from</span></div>
      <div class="stat fade d4"><b>&lt; 1 min</b><span>To get your report</span></div>
    </div>""")

    section_head("WHAT YOU GET", "Everything for a healthier heart",
                 "More than a number — understand <i>why</i> and know exactly <i>what to do next</i>.")
    md("""
    <div class="grid g3">
      <div class="card"><div class="ico red">🫀</div><h3>Instant risk score</h3><p>A friendly 0–100% gauge with Low, Moderate or High status computed by a trained machine-learning model.</p><span class="tag red">AI-powered</span></div>
      <div class="card"><div class="ico">🔍</div><h3>Reading-by-reading insight</h3><p>Every value — BP, cholesterol, heart rate, ECG — is explained in plain language with a green / amber / red status.</p><span class="tag">Easy to understand</span></div>
      <div class="card"><div class="ico green">🥗</div><h3>Personal action plan</h3><p>Diet, exercise and lifestyle suggestions chosen from <i>your</i> results, not generic advice.</p><span class="tag green">Personalised</span></div>
      <div class="card"><div class="ico amber">📄</div><h3>Downloadable report</h3><p>Save a clean printable report to show your doctor, plus a session history you can export as CSV.</p><span class="tag amber">Share with doctor</span></div>
      <div class="card"><div class="ico violet">🧰</div><h3>Handy health tools</h3><p>BMI calculator, target heart-rate zones, blood-pressure guide and a new health tip every day.</p><span class="tag">Free tools</span></div>
      <div class="card"><div class="ico">🔒</div><h3>Private by design</h3><p>No sign-up. Your numbers stay in your browser session and are never sold or shared.</p><span class="tag">100% private</span></div>
    </div>""")

    section_head("SIMPLE PROCESS", "How it works", "Four easy steps — no medical degree required.")
    md("""
    <div class="steps">
      <div class="step"><div class="e">📝</div><h4>Enter details</h4><p>Fill in age, BP, cholesterol and a few more values. Not sure? Choose “Don't know”.</p></div>
      <div class="step"><div class="e">🧠</div><h4>AI analyses</h4><p>The model compares your profile with hundreds of real patient records.</p></div>
      <div class="step"><div class="e">📊</div><h4>See your result</h4><p>Get a risk gauge, colour-coded factors and clear explanations.</p></div>
      <div class="step"><div class="e">💪</div><h4>Take action</h4><p>Follow your personal plan and download the report for your doctor.</p></div>
    </div>""")

    md(f"""
    <div class="split">
      <div><img src="{data_uri('img/hospital.svg')}" alt="Modern hospital illustration"/></div>
      <div><span class="pill">Why it matters</span>
        <h2>Heart disease is the world's #1 killer — but largely preventable</h2>
        <p style="color:var(--muted);line-height:1.7">Cardiovascular disease causes nearly 18 million deaths every year according to the WHO. The good news: most cases are linked to risk factors you can control.</p>
        <ul class="check" style="margin:0;padding:0">
          <li>High blood pressure and cholesterol are usually <b>silent</b></li>
          <li>Early screening can detect problems <b>years</b> before symptoms</li>
          <li>Healthy eating, exercise and no tobacco can prevent up to <b>80%</b> of premature heart disease</li>
        </ul></div>
    </div>""")

    section_head("DID YOU KNOW?", "Quick heart facts")
    md("""
    <div class="grid g4">
      <div class="card" style="text-align:center"><div style="font-size:2.2rem">💓</div><h3>100,000</h3><p>times a day your heart beats — about 2.5 billion in a lifetime.</p></div>
      <div class="card" style="text-align:center"><div style="font-size:2.2rem">🩸</div><h3>7,500 L</h3><p>of blood pumped through your body every single day.</p></div>
      <div class="card" style="text-align:center"><div style="font-size:2.2rem">🚶</div><h3>30 minutes</h3><p>of brisk walking daily lowers heart-disease risk by ~30%.</p></div>
      <div class="card" style="text-align:center"><div style="font-size:2.2rem">🧂</div><h3>&lt; 5 grams</h3><p>of salt a day is the WHO-recommended limit for healthy blood pressure.</p></div>
    </div>""")

    md("""
    <div class="banner"><h2>Ready to check your heart?</h2>
      <p>It takes less than a minute, it's free and your data stays private.</p>
      <a class="btn primary" href="?page=predict" target="_self">❤ Start Heart Check Now</a></div>""")
