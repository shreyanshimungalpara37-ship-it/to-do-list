import re
from datetime import date, timedelta

WEEKDAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august",
          "september", "october", "november", "december"]
CATEGORY_WORDS = {
    "Study": ["study", "assignment", "exam", "dbms", "python", "ai ", "practical", "lecture", "presentation", "project", "research"],
    "Work": ["meeting", "client", "email", "office", "report", "resume", "bug"],
    "Shopping": ["buy", "groceries", "order", "shopping"],
    "Health": ["exercise", "gym", "doctor", "walk", "yoga", "run"],
    "Finance": ["bill", "pay", "fees", "insurance", "rent"],
}


def _find_date(text, today):
    t = text.lower()
    if "tomorrow" in t:
        return today + timedelta(days=1), "tomorrow"
    if "today" in t:
        return today, "today"
    m = re.search(r"in (\d+) days?", t)
    if m:
        return today + timedelta(days=int(m.group(1))), m.group(0)
    m = re.search(r"(\d{1,2})(?:st|nd|rd|th)?\s+(" + "|".join(MONTHS) + r")(?:\s+(\d{4}))?", t)
    if m:
        year = int(m.group(3)) if m.group(3) else today.year
        try:
            d = date(year, MONTHS.index(m.group(2)) + 1, int(m.group(1)))
            if d < today and not m.group(3):
                d = d.replace(year=year + 1)
            return d, m.group(0)
        except ValueError:
            return None, None
    for i, name in enumerate(WEEKDAYS):
        if re.search(r"\b" + name + r"\b", t):
            return today + timedelta(days=(i - today.weekday()) % 7 or 7), name
    return None, None


def parse_task(text, today=None):
    """Rule-based extraction (regex + keywords). No LLM used."""
    today = today or date.today()
    t = text.lower()
    deadline, date_phrase = _find_date(text, today)

    duration = 30
    h = re.search(r"(\d+(?:\.\d+)?)\s*(?:hours?|hrs?|h)\b", t)
    mi = re.search(r"(\d+)\s*(?:minutes?|mins?)\b", t)
    if h:
        duration = int(float(h.group(1)) * 60)
    elif mi:
        duration = int(mi.group(1))

    importance = 2
    if re.search(r"very important|urgent|asap|critical", t):
        importance = 3
    elif re.search(r"low priority|whenever|not important", t):
        importance = 1
    elif "important" in t:
        importance = 3

    category = "Personal"
    for cat, words in CATEGORY_WORDS.items():
        if any(w in t + " " for w in words):
            category = cat
            break

    title = text
    for phrase in [date_phrase, r"very important|urgent|asap|important|low priority",
                   r"for \d+(?:\.\d+)?\s*(?:hours?|hrs?|h|minutes?|mins?)\b"]:
        if phrase:
            title = re.sub(phrase, "", title, flags=re.I)
    title = re.sub(r"\s+", " ", title).strip(" ,.-")
    title = re.sub(r"\b(by|on)\b\s*,?\s*$", "", title, flags=re.I).strip(" ,.-") or text.strip()
    return {"title": title, "deadline": deadline, "category": category,
            "importance": importance, "duration": duration}
