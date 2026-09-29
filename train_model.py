import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from utils.ml_model import FEATURE_COLS, MODEL_PATH

DATA_PATH = ROOT / "data" / "training_data.csv"

# (title, category, importance 1-3, duration in minutes)
BASE_TASKS = [
    ("Submit AI assignment", "Study", 3, 180), ("Complete DBMS practical", "Study", 3, 120),
    ("Study Python for exam", "Study", 3, 120), ("Prepare MCA presentation", "Study", 3, 150),
    ("Submit project report", "Study", 3, 240), ("Read research paper", "Study", 2, 90),
    ("Revise operating system notes", "Study", 2, 60), ("Watch machine learning lecture", "Study", 1, 60),
    ("Attend project meeting", "Work", 2, 60), ("Prepare resume", "Work", 2, 90),
    ("Reply to client emails", "Work", 2, 30), ("Fix bug in website", "Work", 3, 120),
    ("Send weekly status report", "Work", 2, 30), ("Organise desk files", "Work", 1, 30),
    ("Buy groceries", "Shopping", 1, 45), ("Buy birthday gift", "Shopping", 2, 60),
    ("Order printer ink", "Shopping", 1, 15), ("Exercise for 30 minutes", "Health", 2, 30),
    ("Doctor appointment", "Health", 3, 60), ("Go for evening walk", "Health", 1, 30),
    ("Pay electricity bill", "Finance", 3, 15), ("Pay college fees", "Finance", 3, 30),
    ("Track monthly expenses", "Finance", 1, 30), ("Renew insurance policy", "Finance", 2, 30),
    ("Clean the room", "Personal", 1, 60), ("Call parents", "Personal", 2, 20),
    ("Plan weekend trip", "Personal", 1, 45), ("Wash clothes", "Personal", 1, 40),
    ("Book train tickets", "Personal", 2, 20), ("Learn guitar basics", "Personal", 1, 60),
]
DEADLINES = [-1, 0, 1, 3, 7, 14]


def label_priority(text, days_left, importance):
    """Labelling logic: importance + urgency + a small bonus for 'serious' keywords."""
    urgency = 3 if days_left <= 1 else 2 if days_left <= 3 else 1 if days_left <= 7 else 0
    keyword = any(k in text.lower() for k in ["submit", "exam", "bill", "fees", "doctor", "assignment", "report"])
    score = importance * 2 + urgency + int(keyword)
    return "High" if score >= 8 else "Medium" if score >= 5 else "Low"


def create_sample_data():
    random.seed(42)
    rows = []
    for title, cat, imp, dur in BASE_TASKS:
        for days in random.sample(DEADLINES, 4):
            rows.append({"text": title, "category": cat, "days_left": days, "duration_min": dur,
                         "importance": imp, "overdue": int(days < 0),
                         "priority": label_priority(title, days, imp)})
    DATA_PATH.parent.mkdir(exist_ok=True)
    pd.DataFrame(rows).to_csv(DATA_PATH, index=False)
    print(f"Created {len(rows)} training rows at {DATA_PATH}")


def main():
    if not DATA_PATH.exists():
        create_sample_data()
    df = pd.read_csv(DATA_PATH)
    X, y = df[FEATURE_COLS], df["priority"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    prep = ColumnTransformer([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2)), "text"),
        ("cat", OneHotEncoder(handle_unknown="ignore"), ["category"]),
        ("num", StandardScaler(), ["days_left", "duration_min", "importance", "overdue"]),
    ])
    model = Pipeline([("prep", prep), ("clf", LogisticRegression(max_iter=1000))])
    model.fit(X_train, y_train)

    pred = model.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, pred):.2%}")
    print(classification_report(y_test, pred, zero_division=0))
    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")
    print("Note: small demo dataset - educational model, not production-grade.")


if __name__ == "__main__":
    main()
