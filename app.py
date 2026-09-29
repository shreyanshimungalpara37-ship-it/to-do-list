from datetime import date
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from utils import database as db
from utils.ml_model import CATEGORIES, predict_priority
from utils.recommendations import recommend_next
from utils.task_parser import parse_task

st.set_page_config(page_title="AI Smart To-Do List", page_icon="✅", layout="wide")
css = Path(__file__).parent / "assets" / "style.css"
if css.exists():
    st.markdown(f"<style>{css.read_text()}</style>", unsafe_allow_html=True)

IMPORTANCE = {"Low": 1, "Medium": 2, "High": 3}
IMPORTANCE_NAME = {v: k for k, v in IMPORTANCE.items()}
COLORS = {"High": "#d64545", "Medium": "#e8a317", "Low": "#2e9e6b"}

try:
    db.init_db()
except Exception as e:
    st.error(f"Database could not be initialised: {e}")
    st.stop()


def badge(text):
    return f"<span class='badge {text}'>{text}</span>"


def safe_predict(title, category, deadline, duration, importance):
    try:
        return predict_priority(title, category, deadline, duration, importance)
    except FileNotFoundError as e:
        st.error(str(e))
    except Exception as e:
        st.error(f"Prediction failed: {e}")
    return None


def load_df():
    try:
        df = db.get_tasks()
    except Exception as e:
        st.error(f"Could not read tasks: {e}")
        return pd.DataFrame()
    if df.empty:
        return df
    df["deadline_date"] = pd.to_datetime(df["deadline"]).dt.date
    df["overdue"] = (df["status"] == "Pending") & df["deadline_date"].apply(lambda d: pd.notna(d) and d < date.today())
    return df


def save_new_task(title, category, deadline, duration, importance, notes, description=""):
    if not title.strip():
        st.error("Task title cannot be empty.")
        return
    if duration <= 0:
        st.error("Duration must be a positive number of minutes.")
        return
    priority = safe_predict(title, category, deadline, duration, importance)
    if priority is None:
        return
    try:
        db.add_task(title.strip(), description, category, deadline.isoformat() if deadline else None,
                    int(duration), importance, priority, notes)
        st.success("Task saved!")
        st.info(f"🤖 ML predicted priority: **{priority}**")
    except Exception as e:
        st.error(f"Database error: {e}")


st.title("AI Smart To-Do List")
st.caption("Intelligent Task Management using Machine Learning")
page = st.sidebar.radio("Navigation", ["Dashboard", "Add Task", "Task List", "What Next?", "Analytics", "AI Insights"])
df = load_df()
pending = df[df["status"] == "Pending"] if not df.empty else df

if page == "Dashboard":
    total = len(df)
    done = int((df["status"] == "Completed").sum()) if total else 0
    cols = st.columns(6)
    stats = [("Total", total), ("Completed", done), ("Pending", total - done),
             ("Overdue", int(df["overdue"].sum()) if total else 0),
             ("High priority", int((pending["predicted_priority"] == "High").sum()) if total else 0),
             ("Completion %", f"{(done / total * 100) if total else 0:.0f}%")]
    for c, (k, v) in zip(cols, stats):
        c.metric(k, v)
    if total:
        a, b = st.columns(2)
        a.plotly_chart(px.pie(df, names="predicted_priority", title="Priority distribution",
                              color="predicted_priority", color_discrete_map=COLORS), use_container_width=True)
        b.plotly_chart(px.histogram(df, x="category", color="status", title="Tasks by category"), use_container_width=True)
    else:
        st.info("No tasks yet. Add one from the sidebar.")

elif page == "Add Task":
    st.subheader("Quick add (natural language)")
    nl = st.text_input("e.g. Complete DBMS assignment by tomorrow, very important")
    if st.button("Parse and add") and nl.strip():
        p = parse_task(nl)
        st.write(f"Parsed → **{p['title']}** | {p['category']} | due {p['deadline'] or 'none'} | "
                 f"{p['duration']} min | importance {IMPORTANCE_NAME[p['importance']]}")
        save_new_task(p["title"], p["category"], p["deadline"], p["duration"], p["importance"], "")
    st.divider()
    st.subheader("Detailed form")
    with st.form("add_form", clear_on_submit=True):
        title = st.text_input("Task title")
        description = st.text_area("Description", height=70)
        c1, c2, c3 = st.columns(3)
        category = c1.selectbox("Category", CATEGORIES)
        deadline = c2.date_input("Deadline", value=date.today())
        duration = c3.number_input("Estimated duration (minutes)", min_value=1, value=30, step=5)
        importance = IMPORTANCE[st.select_slider("Importance", ["Low", "Medium", "High"], value="Medium")]
        notes = st.text_area("Notes", height=70)
        if st.form_submit_button("Add task"):
            save_new_task(title, category, deadline, int(duration), importance, notes, description)

elif page == "Task List":
    if df.empty:
        st.info("No tasks yet.")
    else:
        c1, c2, c3, c4, c5 = st.columns(5)
        q = c1.text_input("Search")
        cat = c2.selectbox("Category", ["All"] + CATEGORIES)
        pri = c3.selectbox("Priority", ["All", "High", "Medium", "Low"])
        stat = c4.selectbox("Status", ["All", "Pending", "Completed", "Overdue"])
        sort = c5.selectbox("Sort by", ["Deadline", "Priority"])
        view = df.copy()
        if q:
            mask = view["title"].str.contains(q, case=False, na=False) | view["description"].fillna("").str.contains(q, case=False)
            view = view[mask]
        if cat != "All": view = view[view["category"] == cat]
        if pri != "All": view = view[view["predicted_priority"] == pri]
        if stat == "Overdue": view = view[view["overdue"]]
        elif stat != "All": view = view[view["status"] == stat]
        if sort == "Deadline":
            view = view.sort_values("deadline_date", na_position="last")
        else:
            view = view.assign(_o=view["predicted_priority"].map({"High": 0, "Medium": 1, "Low": 2})).sort_values("_o")
        for _, r in view.iterrows():
            with st.container(border=True):
                a, b, c, d = st.columns([6, 1, 1, 1])
                tags = badge(r["predicted_priority"]) + (badge("Completed") if r["status"] == "Completed" else "") + (badge("Overdue") if r["overdue"] else "")
                a.markdown(f"**{r['title']}** {tags}<br><small>{r['category']} · due {r['deadline'] or '—'} · {r['estimated_duration']} min</small>", unsafe_allow_html=True)
                if r["status"] == "Pending" and b.button("✔", key=f"d{r['id']}", help="Mark completed"):
                    db.complete_task(int(r["id"])); st.rerun()
                if d.button("🗑", key=f"x{r['id']}", help="Delete"):
                    db.delete_task(int(r["id"])); st.rerun()
                with c.expander("Edit"):
                    with st.form(f"e{r['id']}"):
                        t = st.text_input("Title", r["title"])
                        ct = st.selectbox("Category", CATEGORIES, index=CATEGORIES.index(r["category"]) if r["category"] in CATEGORIES else 0)
                        dl = st.date_input("Deadline", value=r["deadline_date"] if pd.notna(r["deadline_date"]) else date.today())
                        du = st.number_input("Duration (min)", min_value=1, value=int(r["estimated_duration"]))
                        im = IMPORTANCE[st.select_slider("Importance", ["Low", "Medium", "High"], value=IMPORTANCE_NAME[int(r["importance"])])]
                        nt = st.text_area("Notes", r["notes"] or "")
                        if st.form_submit_button("Save"):
                            if not t.strip():
                                st.error("Title cannot be empty.")
                            else:
                                p = safe_predict(t, ct, dl, int(du), im)
                                if p:
                                    db.update_task(int(r["id"]), t.strip(), ct, dl.isoformat(), int(du), im, p, nt)
                                    st.rerun()

elif page == "What Next?":
    row, reason = recommend_next(pending)
    if row is None:
        st.success("No pending tasks. 🎉")
    else:
        st.markdown(f"<div class='card'><h3>Recommended next: {row['title']}</h3><p>{reason}</p></div>", unsafe_allow_html=True)
        st.caption("This combines the ML-predicted priority with rule-based ranking (deadline, importance, duration). It is not advanced AI.")

elif page == "Analytics":
    if df.empty:
        st.info("No data yet.")
    else:
        done_df = df[df["status"] == "Completed"].copy()
        if not done_df.empty:
            done_df["day"] = pd.to_datetime(done_df["completed_at"]).dt.date
            a, b = st.columns(2)
            a.plotly_chart(px.bar(done_df.groupby("day").size().reset_index(name="completed"), x="day", y="completed", title="Completed per day"), use_container_width=True)
            b.plotly_chart(px.bar(done_df.groupby("category").size().reset_index(name="completed"), x="category", y="completed", title="Completed per category"), use_container_width=True)
        else:
            st.info("Complete a task to see completion charts.")
        a, b = st.columns(2)
        a.plotly_chart(px.pie(df, names="predicted_priority", title="Priority distribution", color="predicted_priority", color_discrete_map=COLORS), use_container_width=True)
        b.plotly_chart(px.pie(df, names="status", title="Pending vs completed"), use_container_width=True)
        week_ago = pd.Timestamp.now() - pd.Timedelta(days=7)
        created = int((pd.to_datetime(df["created_at"]) >= week_ago).sum())
        finished = int((pd.to_datetime(df["completed_at"]) >= week_ago).sum())
        st.info(f"Last 7 days: {created} tasks created, {finished} completed. Overall completion: {len(done_df) / len(df) * 100:.0f}%.")

elif page == "AI Insights":
    st.caption("These insights use ordinary Python logic, not ML.")
    if df.empty:
        st.info("Add tasks to see insights.")
    else:
        high = int((pending["predicted_priority"] == "High").sum())
        st.write(f"• You have {high} high-priority task(s) pending.")
        st.write(f"• You have {int(df['overdue'].sum())} overdue task(s).")
        st.write(f"• Most of your tasks belong to the **{df['category'].mode()[0]}** category.")
        week_ago = pd.Timestamp.now() - pd.Timedelta(days=7)
        week = df[pd.to_datetime(df["created_at"]) >= week_ago]
        if len(week):
            rate = (week["status"] == "Completed").mean() * 100
            st.write(f"• Your completion rate for tasks created this week is {rate:.0f}%.")
