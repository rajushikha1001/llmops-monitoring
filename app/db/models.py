import sqlite3
import json
from datetime import datetime

DB_PATH = "./llmops.db"

def _conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

# Initialize table
def init_db():
    conn = _conn()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_id TEXT,
            user_id TEXT,
            model TEXT,
            status TEXT,
            duration REAL,
            tokens INTEGER,
            payload TEXT,
            created_at TEXT
        )
        """
    )
    conn.commit()
    conn.close()

def insert_record_sync(record: dict):
    conn = _conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO requests (request_id, user_id, model, status, duration, tokens, payload, created_at) VALUES (?,?,?,?,?,?,?,?)",
        (
            record.get("request_id"),
            record.get("user_id"),
            record.get("model"),
            record.get("status"),
            float(record.get("duration", 0.0)),
            int(record.get("tokens", 0)),
            json.dumps(record),
            datetime.utcnow().isoformat(),
        ),
    )
    conn.commit()
    conn.close()

def query_recent(limit: int = 50):
    conn = _conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT request_id, user_id, model, status, duration, tokens, payload, created_at "
        "FROM requests ORDER BY id DESC LIMIT ?",
        (limit,),
    )
    rows = cur.fetchall()
    conn.close()
    return [
        dict(
            request_id=r[0],
            user_id=r[1],
            model=r[2],
            status=r[3],
            duration=r[4],
            tokens=r[5],
            payload=json.loads(r[6]),
            created_at=r[7],
        )
        for r in rows
    ]

# Ensure DB exists
init_db()
