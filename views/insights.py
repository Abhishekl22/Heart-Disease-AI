import streamlit as st

from utils import model as M
from utils.ui import md, page_title, section_head


def render():
    m = M.load_metrics()
    page_title("Model Insights", "How the AI works",
               "Transparent numbers about the machine-learning model behind your Heart Check.")
    if not m:
        st.warning("No metrics found. Run `python train_model.py` first.")
        return

    pct = lambda x: f"{x*100:.1f}%"
    md(f"""<div class="grid g4">
      <div class="metric-big"><b>{pct(m['accuracy'])}</b><span>Accuracy</span></div>
      <div class="metric-big"><b>{pct(m['recall'])}</b><span>Recall (finds sick patients)</span></div>
      <div class="metric-big"><b>{pct(m['precision'])}</b><span>Precision</span></div>
      <div class="metric-big"><b>{m['roc_auc']:.2f}</b><span>ROC-AUC</span></div></div>""")

    cm = m["confusion"]
    left = "".join(f'<div class="row"><span>{M.FEATURE_LABELS[i["feature"]]}</span><div class="t"><i style="width:{i["importance"]/max(m["importance"][0]["importance"],1e-9)*100:.0f}%"></i></div><b>{i["importance"]/max(m["importance"][0]["importance"],1e-9)*100:.0f}</b></div>' for i in m["importance"][:10])
    md(f"""<div class="grid g2" style="margin-top:1.2rem">
      <div class="card bars"><h3>🧠 Most influential factors</h3><p style="margin-bottom:.6rem">Permutation importance measured on unseen test patients.</p>{left}</div>
      <div class="card"><h3>🎯 Confusion matrix (test set)</h3><p style="margin-bottom:.8rem">How predictions compare with the true diagnosis for {m['test_rows']} unseen patients.</p>
        <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:.7rem;text-align:center">
          <div class="metric-big" style="background:#d9f7e8"><b style="color:#0f7d49">{cm['tn']}</b><span>Healthy — correctly cleared</span></div>
          <div class="metric-big" style="background:#fff0d4"><b style="color:#a76a00">{cm['fp']}</b><span>False alarm</span></div>
          <div class="metric-big" style="background:#ffe3e8"><b style="color:#e0264a">{cm['fn']}</b><span>Missed disease</span></div>
          <div class="metric-big" style="background:#d9f7e8"><b style="color:#0f7d49">{cm['tp']}</b><span>Disease — correctly found</span></div></div></div></div>""")

    section_head("MODEL SELECTION", "Three models compared", "5-fold cross-validated ROC-AUC on the training data. The best one is used in the app.")
    mx = max(m["cv_auc"].values())
    rows = "".join(f'<div class="row"><span>{k}{" ⭐" if k == m["best_model"] else ""}</span><div class="t"><i style="width:{v/mx*100:.0f}%"></i></div><b>{v:.3f}</b></div>' for k, v in m["cv_auc"].items())
    md(f'<div class="card bars">{rows}</div>')

    section_head("BEHIND THE SCENES", "The pipeline in 4 steps")
    md(f"""<div class="steps">
      <div class="step"><div class="e">📚</div><h4>Data</h4><p>{m['total_rows']} patient records (UCI Heart Disease) with 13 health features.</p></div>
      <div class="step"><div class="e">🧹</div><h4>Cleaning</h4><p>Impossible zeros removed; missing values filled automatically.</p></div>
      <div class="step"><div class="e">🤖</div><h4>Training</h4><p>{m['best_model']} trained on {m['train_rows']} patients, tested on {m['test_rows']}.</p></div>
      <div class="step"><div class="e">🔬</div><h4>Prediction</h4><p>Outputs the probability of heart disease, shown as your risk score.</p></div></div>""")

    md("""<div class="grid g2" style="margin-top:1.4rem">
      <div class="card"><h3>✅ Strengths</h3><ul><li>Trained on real clinical data</li><li>Handles missing answers gracefully</li><li>Fast, private and runs offline</li></ul></div>
      <div class="card"><h3>⚠️ Limitations</h3><ul><li>Dataset is small and from 4 hospitals (1980s–90s)</li><li>Not tested on every population or age group</li><li>A screening aid only — never a diagnosis</li></ul></div></div>""")
