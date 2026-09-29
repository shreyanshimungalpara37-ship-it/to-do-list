import sqlite3
from contextlib import closing
from datetime import datetime
from pathlib import Path
import pandas as pd

DB_PATH = Path(__file__).resolve().parent.parent / "database" / "todo.db"


def _run(sql, params=(), fetch=False):
    DB_PATH.parent.mkdir(exist_ok=True)
    with closing(sqlite3.connect(DB_PATH)) as conn:
        if fetch:
            return pd.read_sql_query(sql, conn, params=params)
        conn.execute(sql, params)
        conn.commit()


def init_db():
    _run("""CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        category TEXT NOT NULL,
        deadline TEXT,
        estimated_duration INTEGER NOT NULL DEFAULT 30,
        importance INTEGER NOT NULL DEFAULT 2,
        predicted_priority TEXT,
        status TEXT NOT NULL DEFAULT 'Pending',
        notes TEXT,
        created_at TEXT NOT NULL,
        completed_at TEXT)""")


def add_task(title, description, category, deadline, duration, importance, priority, notes):
    _run("""INSERT INTO tasks (title, description, category, deadline, estimated_duration,
            importance, predicted_priority, notes, created_at) VALUES (?,?,?,?,?,?,?,?,?)""",
         (title, description, category, deadline, duration, importance, priority, notes,
          datetime.now().isoformat(timespec="seconds")))


def get_tasks():
    return _run("SELECT * FROM tasks", fetch=True)


def update_task(task_id, title, category, deadline, duration, importance, priority, notes):
    _run("""UPDATE tasks SET title=?, category=?, deadline=?, estimated_duration=?,
            importance=?, predicted_priority=?, notes=? WHERE id=?""",
         (title, category, deadline, duration, importance, priority, notes, task_id))


def complete_task(task_id):
    _run("UPDATE tasks SET status='Completed', completed_at=? WHERE id=?",
         (datetime.now().isoformat(timespec="seconds"), task_id))


def delete_task(task_id):
    _run("DELETE FROM tasks WHERE id=?", (task_id,))
