import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

DB_PATH = Path("data/events.db")

def connect_db():
    conn = sqlite3.connect(DB_PATH)
    return conn

def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            event_type TEXT NOT NULL,
            url TEXT NOT NULL,
            link TEXT,
            sale_type TEXT NOT NULL,
            open_date TEXT,
            open_time TEXT,
            close_date TEXT,
            full_text TEXT,
            last_updated TEXT,
            UNIQUE(name)
        );
    """)

    conn.commit()
    conn.close()

def insert_or_update_event(name, event_type, url, link, sale_type, open_date, open_time, close_date, full_text):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO events (name, event_type, url, link, sale_type, open_date, open_time, close_date, full_text, last_updated)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(name) DO UPDATE SET
            event_type = excluded.event_type,
            url = excluded.url,
            link = excluded.link,
            sale_type = excluded.sale_type,
            open_date = excluded.open_date,
            open_time = excluded.open_time,
            close_date = excluded.close_date,
            full_text = excluded.full_text,
            last_updated = excluded.last_updated
    """, (name, event_type, url, link, sale_type, open_date, open_time, close_date, full_text, datetime.now().isoformat()))
    
    conn.commit()
    conn.close()

def fetch_all_events():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_all_events():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events")
    rows = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]
    events = [dict(zip(col_names, row)) for row in rows]
    conn.close()
    return events

def get_upcoming_opening_events(days_ahead=30):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events")
    rows = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]
    events = [dict(zip(col_names, row)) for row in rows]
    conn.close()

    today = datetime.now().date()
    upcoming = []

    for event in events:
        try:
            event_date = datetime.strptime(event["open_date"], "%Y-%m-%d").date()
            if 0 <= (event_date - today).days <= days_ahead:
                upcoming.append(event)
        except (ValueError, TypeError):
            continue

    return upcoming

def get_upcoming_closing_events(days_ahead=30):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events")
    rows = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]
    events = [dict(zip(col_names, row)) for row in rows]
    conn.close()

    today = datetime.now().date()
    upcoming = []

    for event in events:
        try:
            event_date = datetime.strptime(event["close_date"], "%Y-%m-%d").date()
            if 0 <= (event_date - today).days <= days_ahead:
                upcoming.append(event)
        except (ValueError, TypeError):
            continue

    return upcoming



if __name__ == "__main__":
    create_table()
    insert_or_update_event(
        "Berlin Marathon",
        "Marathon",
        "https://www.bmw-berlin-marathon.com/en/",
        "https://www.bmw-berlin-marathon.com/en/entry/",
        "Ballot",
        "2025-09-25",
        "09:00",
        "2025-11-6",
        "Berlin Marathon 2025 ballot opens soon!"
    )

    upcoming = get_upcoming_opening_events()
    for e in upcoming:
        print(f"📅 The {e['name']} opens soon — {e['open_date']}")

    upcoming = get_upcoming_closing_events()
    for e in upcoming:
        print(f"📅 The {e['name']} closes soon — {e['close_date']}")