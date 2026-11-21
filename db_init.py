import sqlite3
import os

def init_db():
    os.makedirs("/app/data", exist_ok=True)
    conn = sqlite3.connect("/app/data/tasks.db")
    conn.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, content TEXT)")
    conn.close()

init_db()
