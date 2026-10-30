import csv
import re
from datetime import datetime
from pathlib import Path

import streamlit as st

from utils import content as C
from utils.config import SUPPORT_EMAIL, SUPPORT_HOURS, SUPPORT_PHONE
from utils.ui import md, page_title, section_head

MSG_FILE = Path(__file__).resolve().parent.parent / "data" / "messages.csv"


def _save(name, email, topic, message):
    MSG_FILE.parent.mkdir(exist_ok=True)
    new = not MSG_FILE.exists()
    with open(MSG_FILE, "a", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        if new:
            w.writerow(["time", "name", "email", "topic", "message"])
        w.writerow([datetime.now().isoformat(timespec="seconds"), name, email, topic, message])


def render():
    page_title("Help & Support", "How can we help you?",
               "Find quick answers, contact our team or learn what to do in an emergency.")

    md(f"""<div class="grid g3">
      <div class="card"><div class="ico">📧</div><h3>Email us</h3><p>{SUPPORT_EMAIL}<br>We reply within 24 hours.</p></div>
      <div class="card"><div class="ico green">📞</div><h3>Call us</h3><p>{SUPPORT_PHONE}<br>{SUPPORT_HOURS}</p></div>
      <div class="card" style="background:linear-gradient(160deg,#fff,#ffe9ed)"><div class="ico red">🚑</div><h3>Emergency?</h3><p>Call <b>112</b> (India) · <b>911</b> (US) · <b>999</b> (UK) immediately. Do not use the app.</p></div></div>""")

    section_head("FAQ", "Frequently asked questions")
    for q, a in C.FAQS:
        with st.expander(f"💬 {q}"):
            st.write(a)

    section_head("GET IN TOUCH", "Send us a message", "Questions, feedback or found a bug? We'd love to hear from you.")
    left, right = st.columns([1.3, 1], gap="large")
    with left:
        with st.container(key="card_contact"):
            with st.form("contact_form", clear_on_submit=True):
                a, b = st.columns(2)
                name = a.text_input("Your name *")
                email = b.text_input("Email *")
                topic = st.selectbox("Topic", ["General question", "Report a problem", "Feedback / suggestion", "Medical information", "Partnership"])
                message = st.text_area("Message *", height=140, placeholder="Tell us how we can help…")
                sent = st.form_submit_button("📨 Send message", use_container_width=True)
            if sent:
                if not name.strip() or not email.strip() or not message.strip():
                    st.error("Please fill in your name, email and message.")
                elif not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email.strip()):
                    st.error("Please enter a valid email address.")
                else:
                    _save(name.strip(), email.strip(), topic, message.strip())
                    st.success("✅ Thank you! Your message has been received. We'll get back to you soon.")
                    st.balloons()
    with right:
        md("""<div class="sos"><h3>🚨 Not for emergencies</h3><p style="color:var(--ink);line-height:1.7">This form is not monitored around the clock.
            For chest pain, severe breathlessness, fainting or any life-threatening situation, call your emergency number straight away.</p></div>
            <div class="card" style="margin-top:1rem"><h3>🩺 Useful resources</h3><ul>
            <li>World Health Organization – Cardiovascular diseases</li><li>American Heart Association – Know your risk</li>
            <li>National Health Portal of India</li><li>Your local cardiologist or family doctor</li></ul></div>""")
