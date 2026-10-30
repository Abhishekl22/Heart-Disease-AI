# ❤ HeartGuard AI – Heart Disease Prediction (multi-page Streamlit app)

## Run
```bash
pip install -r requirements.txt
python train_model.py              # optional – a trained model is already included
python -m streamlit run app.py
```

## Structure
```
heart_disease_app/
├── app.py                  # entry point + page router (?page=home|predict|tips|insights|support)
├── train_model.py          # trains/compares 3 models, saves model/ + metrics.json
├── requirements.txt
├── .streamlit/config.toml  # light theme
├── dataset/heart_disease_uci.csv
├── model/heart_pipeline.pkl, metrics.json
├── assets/
│   ├── css/style.css       # whole hospital-style design system
│   ├── js/hero3d.html      # 3D rotating particle heart (canvas)
│   ├── js/scanner.html     # sci-fi scanning animation shown while predicting
│   └── img/bg.svg, hospital.svg, doctor.svg
├── utils/ config.py (names/contacts), ui.py (navbar, footer, JS), model.py (predict+analysis), content.py (all text)
└── views/ home.py, predict.py, tips.py, insights.py, support.py
```

## What changed vs. your first version
- Fixed bug: `"ST-T abnormality"` didn't match the dataset (`st-t abnormality`) so it became NaN.
- Fixed bug: probability shown was P(class 1) of a 5-class model; now a proper binary model (healthy vs disease).
- Missing values handled in a Pipeline, so users can answer "Don't know".
- Zero BP/cholesterol treated as missing. Logistic Regression won CV (AUC 0.91, ~85% accuracy).

## Customise
Edit `utils/config.py` (name, email, phone) and `utils/content.py` (tips, FAQs).
Support messages are saved in `data/messages.csv`.
Not a medical device – demo only.
