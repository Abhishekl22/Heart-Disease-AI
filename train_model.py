"""
train_model.py  -  trains the heart-disease model and saves it to /model

Run:   python train_model.py

What it does (improvements over the first version)
  * fixes the 'st-t abnormality' spelling bug (the old mapping silently produced NaN)
  * treats impossible zero values (blood pressure / cholesterol = 0) as missing
  * turns the 0-4 target into a clean binary label  (0 = healthy, 1 = heart disease)
  * handles missing values inside a scikit-learn Pipeline (so the app can accept "Don't know")
  * compares 3 models with cross-validation and keeps the best one
  * saves ONE pipeline file + metrics.json (used by the Insights page)
"""
import json
import os

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, confusion_matrix, f1_score,
                             precision_score, recall_score, roc_auc_score)
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

RANDOM_STATE = 42
DATA_PATH = "dataset/heart_disease_uci.csv"
MODEL_PATH = "model/heart_pipeline.pkl"
METRICS_PATH = "model/metrics.json"

NUMERIC = ["age", "trestbps", "chol", "thalch", "oldpeak", "ca"]
CATEGORICAL = ["sex", "cp", "fbs", "restecg", "exang", "slope", "thal"]
FEATURES = NUMERIC + CATEGORICAL


def load_data() -> pd.DataFrame:
    data = pd.read_csv(DATA_PATH)
    data = data.drop(columns=[c for c in ["id", "dataset"] if c in data.columns])

    # tidy text values (lower-case, trimmed) so spelling/case differences cannot create NaN
    for col in ["sex", "cp", "restecg", "slope", "thal"]:
        data[col] = data[col].astype("object").where(data[col].notna(), np.nan)
        data[col] = data[col].map(lambda v: v.strip().lower() if isinstance(v, str) else v)
    for col in ["fbs", "exang"]:
        data[col] = data[col].map({True: "yes", False: "no", "TRUE": "yes", "FALSE": "no"})

    # impossible values -> missing
    data.loc[data["trestbps"] <= 0, "trestbps"] = np.nan
    data.loc[data["chol"] <= 0, "chol"] = np.nan

    # binary target: 0 = no disease, 1..4 = disease
    data["target"] = (data["num"] > 0).astype(int)
    return data.drop(columns=["num"])


def build_preprocessor() -> ColumnTransformer:
    numeric = Pipeline([
        ("impute", SimpleImputer(strategy="median", add_indicator=True)),
        ("scale", StandardScaler()),
    ])
    categorical = Pipeline([
        ("impute", SimpleImputer(strategy="constant", fill_value="unknown")),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ])
    return ColumnTransformer([("num", numeric, NUMERIC), ("cat", categorical, CATEGORICAL)])


def main() -> None:
    data = load_data()
    X, y = data[FEATURES], data["target"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )

    candidates = {
        "Random Forest": RandomForestClassifier(
            n_estimators=400, min_samples_leaf=3, random_state=RANDOM_STATE, n_jobs=-1),
        "Gradient Boosting": GradientBoostingClassifier(
            n_estimators=200, learning_rate=0.05, max_depth=3, random_state=RANDOM_STATE),
        "Logistic Regression": LogisticRegression(max_iter=2000),
    }

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    scores = {}
    for name, clf in candidates.items():
        pipe = Pipeline([("prep", build_preprocessor()), ("clf", clf)])
        auc = cross_val_score(pipe, X_train, y_train, cv=cv, scoring="roc_auc").mean()
        scores[name] = float(auc)
        print(f"  {name:<20} CV ROC-AUC = {auc:.3f}")

    best_name = max(scores, key=scores.get)
    print(f"\n[OK] Best model: {best_name}")
    best = Pipeline([("prep", build_preprocessor()), ("clf", candidates[best_name])])
    best.fit(X_train, y_train)

    proba = best.predict_proba(X_test)[:, 1]
    pred = (proba >= 0.5).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_test, pred).ravel()

    # permutation importance on the ORIGINAL columns (easy to explain to users)
    imp = permutation_importance(best, X_test, y_test, n_repeats=15,
                                 random_state=RANDOM_STATE, scoring="roc_auc")
    importance = sorted(
        ({"feature": f, "importance": float(max(m, 0))} for f, m in zip(FEATURES, imp.importances_mean)),
        key=lambda d: d["importance"], reverse=True)

    metrics = {
        "best_model": best_name,
        "cv_auc": scores,
        "accuracy": float(accuracy_score(y_test, pred)),
        "precision": float(precision_score(y_test, pred)),
        "recall": float(recall_score(y_test, pred)),
        "f1": float(f1_score(y_test, pred)),
        "roc_auc": float(roc_auc_score(y_test, proba)),
        "confusion": {"tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp)},
        "train_rows": int(len(X_train)),
        "test_rows": int(len(X_test)),
        "total_rows": int(len(data)),
        "positive_rate": float(y.mean()),
        "importance": importance,
        "features": FEATURES,
    }

    print(f"Accuracy {metrics['accuracy']*100:.1f}% | Recall {metrics['recall']*100:.1f}% | "
          f"ROC-AUC {metrics['roc_auc']:.3f}")

    os.makedirs("model", exist_ok=True)
    joblib.dump(best, MODEL_PATH)
    with open(METRICS_PATH, "w", encoding="utf-8") as fh:
        json.dump(metrics, fh, indent=2)
    print(f"[SAVED] {MODEL_PATH} and {METRICS_PATH}")


if __name__ == "__main__":
    main()
