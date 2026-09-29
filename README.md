# AI Smart To-Do List
Intelligent Task Management using Machine Learning (MCA Sem-3 mini project).

## Setup
    python -m venv venv
    venv\Scripts\activate          (Windows)   |   source venv/bin/activate   (Linux/macOS)
    pip install -r requirements.txt
    python model/train_model.py    # creates data/training_data.csv and model/priority_model.joblib
    streamlit run app.py

## How the AI works
- **Model:** Logistic Regression in a scikit-learn Pipeline (TF-IDF on title + one-hot category + scaled numeric features: days left, duration, importance, overdue). Chosen because it is simple, fast on small data and easy to explain in a viva.
- **Labels:** the sample dataset (120 rows) is generated with documented logic (importance + urgency + keywords) in `model/train_model.py`.
- **Recommendation:** ML priority + rule-based scoring (deadline, importance, duration).
- **Natural language input:** regex/keyword parser (`utils/task_parser.py`). Handles today, tomorrow, weekdays, "in N days", "5 October", "2 hours", "very important". Limitations: no complex phrases like "next month end"; category is keyword-based.

## Limitations
Small synthetic dataset, so the model is educational, not production-grade. Single user, no reminders.

## Screenshots
(add screenshots here)
