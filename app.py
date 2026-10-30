"""
HeartGuard AI  -  multi-page Streamlit app

python -m streamlit run app.py

Run:  python -m streamlit run app.py
"""
import streamlit as st

from utils.config import APP_NAME, PAGES
from utils.ui import enhancer, footer, inject_css, navbar

st.set_page_config(page_title=f"{APP_NAME} · Heart Health Screening", page_icon="❤️",
                   layout="wide", initial_sidebar_state="collapsed")

inject_css()

valid = [k for k, _ in PAGES]
page = st.query_params.get("page", "home")
if isinstance(page, list):
    page = page[0]
if page not in valid:
    page = "home"

navbar(page)
enhancer()

if page == "home":
    from views import home as view
elif page == "predict":
    from views import predict as view
elif page == "tips":
    from views import tips as view
elif page == "insights":
    from views import insights as view
else:
    from views import support as view

view.render()
footer()
