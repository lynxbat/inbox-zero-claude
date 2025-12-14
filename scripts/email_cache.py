#!/usr/bin/env python3
"""
Email Cache - SQLite-based email metadata cache for faster inbox triage.

This module provides local caching of email metadata to speed up searches
and reduce API calls to Outlook. Only new emails since last sync are fetched.

Usage:
    python email_cache.py sync       # Sync new emails from inbox
    python email_cache.py search <term>  # Search cached emails
    python email_cache.py stats      # Show cache statistics
"""

import sqlite3
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "email_cache.db"


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

    # Create indexes for fast searching
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_sender ON emails(sender)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_subject ON emails(subject)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_date ON emails(date)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_folder ON emails(folder)")

    conn.commit()
    conn.close()
    print(f"Database initialized at {DB_PATH}")


def get_last_sync():
    """Get the timestamp of the last sync."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT synced_at FROM sync_log ORDER BY id DESC LIMIT 1")
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


def search_local(term: str, field: str = None, limit: int = 50):
    """Search emails in local cache."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    term_pattern = f"%{term}%"

    if field == "sender":
        cursor.execute("""
            SELECT id, subject, sender, date, folder
            FROM emails
            WHERE sender LIKE ? AND folder = 'Inbox'
            ORDER BY date DESC
            LIMIT ?
        """, (term_pattern, limit))
    elif field == "subject":
        cursor.execute("""
            SELECT id, subject, sender, date, folder
            FROM emails
            WHERE subject LIKE ? AND folder = 'Inbox'
            ORDER BY date DESC
            LIMIT ?
        """, (term_pattern, limit))
    else:
        cursor.execute("""
            SELECT id, subject, sender, date, folder
            FROM emails
            WHERE (sender LIKE ? OR subject LIKE ? OR snippet LIKE ?) AND folder = 'Inbox'
            ORDER BY date DESC
            LIMIT ?
        """, (term_pattern, term_pattern, term_pattern, limit))

    results = cursor.fetchall()
    conn.close()
    return results


def add_emails(emails: list):
    """Add emails to the cache."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    now = datetime.now().isoformat()
    added = 0

    for email in emails:
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO emails (id, subject, sender, date, folder, snippet, synced_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                email.get('id'),
                email.get('subject', ''),
                email.get('sender', ''),
                email.get('date', ''),
                email.get('folder', 'Inbox'),
                email.get('snippet', ''),
                now
            ))
            added += 1
        except Exception as e:
            print(f"Error adding email {email.get('id')}: {e}")

    conn.commit()
    conn.close()
    return added


def update_folder(email_id: str, new_folder: str):
    """Update the folder for an email (when moved)."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE emails SET folder = ? WHERE id = ?", (new_folder, email_id))
    conn.commit()
    conn.close()


def remove_from_inbox(email_id: str):
    """Mark email as no longer in inbox."""
    update_folder(email_id, "Archived")


def get_stats():
    """Get cache statistics."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM emails WHERE folder = 'Inbox'")
    inbox_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM emails")
    total_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT sender) FROM emails")
    unique_senders = cursor.fetchone()[0]

    last_sync = get_last_sync()

    conn.close()

    return {
        "inbox_count": inbox_count,
        "total_cached": total_count,
        "unique_senders": unique_senders,
        "last_sync": last_sync
    }


def get_sender_counts(limit: int = 20):
    """Get top senders by email count."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT sender, COUNT(*) as count
        FROM emails
        WHERE folder = 'Inbox'
        GROUP BY sender
        ORDER BY count DESC
        LIMIT ?
    """, (limit,))

    results = cursor.fetchall()
    conn.close()
    return results


def get_emails_by_sender(sender_pattern: str):
    """Get all emails from a sender pattern."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, subject, sender, date
        FROM emails
        WHERE sender LIKE ? AND folder = 'Inbox'
        ORDER BY date DESC
    """, (f"%{sender_pattern}%",))

    results = cursor.fetchall()
    conn.close()
    return results


def log_sync(emails_added: int, emails_removed: int = 0):
    """Log a sync operation."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO sync_log (synced_at, emails_added, emails_removed)
        VALUES (?, ?, ?)
    """, (datetime.now().isoformat(), emails_added, emails_removed))
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()

    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "stats":
        stats = get_stats()
        print(f"Cache Statistics:")
        print(f"  Inbox emails: {stats['inbox_count']}")
        print(f"  Total cached: {stats['total_cached']}")
        print(f"  Unique senders: {stats['unique_senders']}")
        print(f"  Last sync: {stats['last_sync'] or 'Never'}")

    elif cmd == "search" and len(sys.argv) > 2:
        term = sys.argv[2]
        results = search_local(term)
        print(f"Found {len(results)} emails matching '{term}':")
        for r in results:
            print(f"  [{r[0]}] {r[3][:10]} - {r[2][:30]} - {r[1][:50]}")

    elif cmd == "senders":
        senders = get_sender_counts(30)
        print("Top senders in inbox:")
        for sender, count in senders:
            print(f"  {count:4d} - {sender}")

    elif cmd == "init":
        print("Database initialized.")

    else:
        print(__doc__)
