"""Shared UI helpers: CSS injection, navbar, footer, JS enhancer, embedded components."""
import base64
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from utils.config import APP_NAME, PAGES, SUPPORT_EMAIL, SUPPORT_HOURS, SUPPORT_PHONE, TAGLINE

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"


def html(s: str) -> str:
    """Flatten an HTML snippet so Streamlit's markdown parser never treats indentation as code."""
    return "".join(line.strip() for line in s.strip().splitlines())


def md(s: str) -> None:
    st.markdown(html(s), unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def data_uri(rel_path: str) -> str:
    p = ASSETS / rel_path
    mime = {"svg": "image/svg+xml", "png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg"}[p.suffix[1:]]
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()


@st.cache_data(show_spinner=False)
def _css() -> str:
    css = (ASSETS / "css" / "style.css").read_text(encoding="utf-8")
    return css.replace("__BG__", data_uri("img/bg.svg"))


def inject_css() -> None:
    st.markdown(f"<style>{_css()}</style>", unsafe_allow_html=True)


def embed(file_name: str, height: int, **replace) -> None:
    """Render a self-contained HTML/JS file from assets/js inside an iframe."""
    src = (ASSETS / "js" / file_name).read_text(encoding="utf-8")
    for k, v in replace.items():
        src = src.replace(f"%{k}%", str(v))
    components.html(src, height=height)


def enhancer() -> None:
    """Tiny JS helper: 3D mouse-tilt on cards + scroll-reveal. Silently does nothing if blocked."""
    components.html("""
    <script>
    try{
      const w=window.parent, d=w.document;
      if(!w.__hgEnhance){
        w.__hgEnhance=true; d.body.classList.add('hg-js');
        const sel='.card,.step,.stat,.sec-head,.split,.banner,.factor,.metric-big';
        const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.08});
        const scan=()=>d.querySelectorAll(sel).forEach(el=>{if(!el.__rv){el.__rv=1;el.classList.add('rv');io.observe(el)}});
        scan(); new MutationObserver(scan).observe(d.body,{childList:true,subtree:true});
        d.addEventListener('mousemove',e=>{
          const el=e.target.closest&&e.target.closest('.card,.stat,.step'); 
          if(w.__hgLast&&w.__hgLast!==el){w.__hgLast.style.transform='';}
          if(!el){return} w.__hgLast=el;
          const r=el.getBoundingClientRect(), x=(e.clientX-r.left)/r.width-.5, y=(e.clientY-r.top)/r.height-.5;
          el.style.transform='perspective(800px) rotateX('+(-y*9)+'deg) rotateY('+(x*11)+'deg) translateY(-6px)';
        });
        d.addEventListener('mouseleave',()=>{if(w.__hgLast)w.__hgLast.style.transform=''});
      }
    }catch(e){}
    </script>""", height=0)


def scroll_to(anchor_id: str) -> None:
    components.html(f"""<script>
    try{{setTimeout(()=>{{const el=window.parent.document.getElementById('{anchor_id}');
    if(el)el.scrollIntoView({{behavior:'smooth',block:'start'}});}},150);}}catch(e){{}}
    </script>""", height=0)


def navbar(active: str) -> None:
    logo = data_uri_logo()
    # keep the CTA as the 2nd item
    items = []
    for k, label in PAGES:
        if k == "predict":
            items.append(f'<a class="cta {"active" if active == k else ""}" href="?page=predict" target="_self">❤ {label}</a>')
        else:
            items.append(f'<a class="{"active" if k == active else ""}" href="?page={k}" target="_self">{label}</a>')
    md(f"""
    <div class="topbar"><span>🚑 Emergency? Call <b>112</b> (India) · <b>911</b> (US) · <b>999</b> (UK)</span>
    <span class="hide-m">📧 {SUPPORT_EMAIL}</span></div>
    <div class="nav">
      <a class="brand" href="?page=home" target="_self"><div class="brand-logo"><img src="{logo}" width="22" height="22"/></div>
        <div class="brand-name">{APP_NAME}<small>{TAGLINE.upper()}</small></div></a>
      <div class="links">{''.join(items)}</div>
    </div>""")


def data_uri_logo() -> str:
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="white" d="M12 21s-7.5-4.6-9.6-9.2C.8 8.3 2.7 4.5 6.4 4.5c2.1 0 3.8 1.1 5.6 3.2 1.8-2.1 3.5-3.2 5.6-3.2 3.7 0 5.6 3.8 4 7.3C19.5 16.4 12 21 12 21z"/></svg>')
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()


def footer() -> None:
    logo = data_uri_logo()
    md(f"""
    <div class="footer">
      <div class="cols">
        <div><div class="brand"><div class="brand-logo"><img src="{logo}" width="22" height="22"/></div>
          <div class="brand-name">{APP_NAME}<small style="color:#7fe3f0">{TAGLINE.upper()}</small></div></div>
          <p>An AI-assisted screening tool that turns a few simple health numbers into clear, friendly guidance. Built for learning and awareness — always confirm with a doctor.</p></div>
        <div><h5>Explore</h5><a href="?page=home" target="_self">Home</a><a href="?page=predict" target="_self">Heart Check</a>
          <a href="?page=tips" target="_self">Health Tips</a><a href="?page=insights" target="_self">Model Insights</a></div>
        <div><h5>Help</h5><a href="?page=support" target="_self">Support Centre</a><a href="?page=support" target="_self">FAQs</a>
          <a href="?page=support" target="_self">Contact Us</a><a href="?page=tips" target="_self">Warning Signs</a></div>
        <div><h5>Contact</h5><p style="margin-top:0">📧 {SUPPORT_EMAIL}<br>📞 {SUPPORT_PHONE}<br>🕘 {SUPPORT_HOURS}<br>🚑 Emergency: <b style="color:#fff">112</b></p></div>
      </div>
      <div class="bottom">⚠️ Demonstration ML model — not a medical diagnosis. © 2026 {APP_NAME}. Made with ❤ using Python &amp; Streamlit.</div>
    </div>""")


def section_head(eyebrow: str, title: str, text: str = "") -> None:
    md(f"""<div class="sec-head"><div class="eyebrow">{eyebrow}</div><h2>{title}</h2><p>{text}</p></div>""")


def page_title(eyebrow: str, title: str, text: str) -> None:
    md(f"""<div class="page-title fade"><span class="pill"><i></i>{eyebrow}</span><h1>{title}</h1><p>{text}</p></div>""")


def cols(spec, **kw):
    """st.columns with vertical centring where the Streamlit version supports it."""
    try:
        return st.columns(spec, **kw)
    except TypeError:
        kw.pop("vertical_alignment", None)
        return st.columns(spec, **kw)
