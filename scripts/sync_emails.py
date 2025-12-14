#!/usr/bin/env python3
"""
Sync script to populate the email cache from a batch read.
Parses email data and inserts into SQLite cache.
"""

import sqlite3
import re
import sys
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "email_cache.db"

# Configure your internal domain to filter external senders
# Example: "company.com" or "myorg.org"
INTERNAL_DOMAIN = "company.com"


def init_db():
    """Initialize the SQLite database with required tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emails (
            id TEXT PRIMARY KEY,
            subject TEXT,
            sender TEXT,
            date TEXT,
            folder TEXT DEFAULT 'Inbox',
            snippet TEXT,
            synced_at TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sync_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            synced_at TEXT,
            emails_added INTEGER,
            emails_removed INTEGER
        )
    """)

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_sender ON emails(sender)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_subject ON emails(subject)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_date ON emails(date)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_folder ON emails(folder)")

    conn.commit()
    conn.close()


def add_email(email_id, subject, sender, date, folder='Inbox'):
    """Add a single email to the cache."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now = datetime.now().isoformat()

    try:
        cursor.execute("""
            INSERT OR REPLACE INTO emails (id, subject, sender, date, folder, synced_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (email_id, subject, sender, date, folder, now))
        conn.commit()
    except Exception as e:
        print(f"Error adding email {email_id}: {e}")
    finally:
        conn.close()


def search(term, limit=50):
    """Search emails in local cache."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    pattern = f"%{term}%"
    cursor.execute("""
        SELECT id, subject, sender, date, folder
        FROM emails
        WHERE (sender LIKE ? OR subject LIKE ?) AND folder = 'Inbox'
        ORDER BY date DESC
        LIMIT ?
    """, (pattern, pattern, limit))

    results = cursor.fetchall()
    conn.close()
    return results


def search_sender(sender_pattern, limit=100):
    """Search emails by sender domain/pattern."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    pattern = f"%{sender_pattern}%"
    cursor.execute("""
        SELECT id, subject, sender, date
        FROM emails
        WHERE sender LIKE ? AND folder = 'Inbox'
        ORDER BY date DESC
        LIMIT ?
    """, (pattern, limit))

    results = cursor.fetchall()
    conn.close()
    return results


def get_top_senders(limit=30):
    """Get top senders by email count in inbox."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT sender, COUNT(*) as cnt
        FROM emails
        WHERE folder = 'Inbox'
        GROUP BY sender
        ORDER BY cnt DESC
        LIMIT ?
    """, (limit,))

    results = cursor.fetchall()
    conn.close()
    return results


def get_external_senders(limit=50):
    """Get senders from outside your internal domain (configure INTERNAL_DOMAIN)."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT sender, COUNT(*) as cnt
        FROM emails
        WHERE folder = 'Inbox' AND sender NOT LIKE '%@{INTERNAL_DOMAIN}'
        GROUP BY sender
        ORDER BY cnt DESC
        LIMIT ?
    """, (limit,))

    results = cursor.fetchall()
    conn.close()
    return results


def search_by_date(month_pattern, year_pattern=None, limit=100):
    """Search emails by date pattern (e.g., 'October', 'November 2025')."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if year_pattern:
        pattern = f"%{month_pattern}%{year_pattern}%"
    else:
        pattern = f"%{month_pattern}%"

    cursor.execute("""
        SELECT id, subject, sender, date
        FROM emails
        WHERE date LIKE ? AND folder = 'Inbox'
        ORDER BY date DESC
        LIMIT ?
    """, (pattern, limit))

    results = cursor.fetchall()
    conn.close()
    return results


def search_date_range(start_month, end_month, limit=200):
    """Search emails between two months (inclusive)."""
    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Build OR conditions for each month in range
    try:
        start_idx = months.index(start_month)
        end_idx = months.index(end_month)
    except ValueError:
        print(f"Invalid month name. Use full names like 'October', 'November'")
        return []

    if start_idx > end_idx:
        start_idx, end_idx = end_idx, start_idx

    conditions = []
    params = []
    for i in range(start_idx, end_idx + 1):
        conditions.append("date LIKE ?")
        params.append(f"%{months[i]}%")

    params.append(limit)
    query = f"""
        SELECT id, subject, sender, date
        FROM emails
        WHERE ({' OR '.join(conditions)}) AND folder = 'Inbox'
        ORDER BY date DESC
        LIMIT ?
    """
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results


def mark_moved(email_id, new_folder='Archived'):
    """Mark an email as moved out of inbox."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE emails SET folder = ? WHERE id = ?", (new_folder, email_id))
    conn.commit()
    conn.close()


def stats():
    """Get cache statistics."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM emails WHERE folder = 'Inbox'")
    inbox = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM emails")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT sender) FROM emails WHERE folder = 'Inbox'")
    senders = cursor.fetchone()[0]

    conn.close()
    return {"inbox": inbox, "total": total, "unique_senders": senders}


if __name__ == "__main__":
    init_db()

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python sync_emails.py stats")
        print("  python sync_emails.py search <term>")
        print("  python sync_emails.py sender <pattern>")
        print("  python sync_emails.py top")
        print("  python sync_emails.py external")
        print("  python sync_emails.py date <month> [year]     # e.g., 'October' or 'October 2025'")
        print("  python sync_emails.py range <start> <end>    # e.g., 'October' 'December'")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "stats":
        s = stats()
        print(f"Inbox: {s['inbox']} | Total cached: {s['total']} | Unique senders: {s['unique_senders']}")

    elif cmd == "search" and len(sys.argv) > 2:
        term = sys.argv[2]
        results = search(term)
        print(f"Found {len(results)} emails matching '{term}':")
        for r in results:
            print(f"  ID:{r[0]} | {r[3][:16]} | {r[2][:35]} | {r[1][:50]}")

    elif cmd == "sender" and len(sys.argv) > 2:
        pattern = sys.argv[2]
        results = search_sender(pattern)
        print(f"Found {len(results)} emails from '{pattern}':")
        for r in results:
            print(f"  ID:{r[0]} | {r[3][:16]} | {r[1][:60]}")

    elif cmd == "top":
        results = get_top_senders()
        print("Top senders in inbox:")
        for sender, count in results:
            print(f"  {count:3d} | {sender}")

    elif cmd == "external":
        results = get_external_senders()
        print(f"Top external senders (non {INTERNAL_DOMAIN}):")
        for sender, count in results:
            print(f"  {count:3d} | {sender}")

    elif cmd == "date" and len(sys.argv) > 2:
        month = sys.argv[2]
        year = sys.argv[3] if len(sys.argv) > 3 else None
        results = search_by_date(month, year)
        label = f"{month} {year}" if year else month
        print(f"Found {len(results)} emails from '{label}':")
        for r in results:
            print(f"  ID:{r[0]} | {r[3][:30]} | {r[2][:30]} | {r[1][:45]}")

    elif cmd == "range" and len(sys.argv) > 3:
        start = sys.argv[2]
        end = sys.argv[3]
        results = search_date_range(start, end)
        print(f"Found {len(results)} emails from {start} to {end}:")
        for r in results:
            print(f"  ID:{r[0]} | {r[3][:30]} | {r[2][:30]} | {r[1][:45]}")

    else:
        print("Unknown command. Run without arguments for help.")
