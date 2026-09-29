from datetime import date

PRIORITY_POINTS = {"High": 40, "Medium": 25, "Low": 10}


def score_task(row, today=None):
    """Rule-based ranking that combines the ML-predicted priority with other factors."""
    today = today or date.today()
    score = PRIORITY_POINTS.get(row["predicted_priority"], 10)
    reasons = [f"{row['predicted_priority']} predicted priority"]
    if row["deadline"]:
        days = (date.fromisoformat(row["deadline"]) - today).days
        if days < 0:
            score += 40; reasons.append("it is overdue")
        elif days == 0:
            score += 35; reasons.append("deadline is today")
        elif days == 1:
            score += 30; reasons.append("deadline is tomorrow")
        elif days <= 3:
            score += 20; reasons.append(f"deadline is in {days} days")
        elif days <= 7:
            score += 10; reasons.append("deadline is this week")
    score += row["importance"] * 5
    if row["importance"] == 3:
        reasons.append("importance is high")
    if row["estimated_duration"] <= 30:
        score += 5; reasons.append("it is a quick task")
    return score, reasons


def recommend_next(pending_df):
    if pending_df.empty:
        return None, None
    scored = [(score_task(r), r) for _, r in pending_df.iterrows()]
    (best_score, reasons), best_row = max(scored, key=lambda x: x[0][0])
    return best_row, "Reason: " + ", ".join(reasons) + f". (Rule-based score: {best_score})"
