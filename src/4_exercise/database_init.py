import sqlite3
import os
from datetime import datetime
import json
from typing import List, Dict, Any

DB_PATH = "quiz_database.db"


def create_quiz_database(force_create_db: bool, debug: bool):
    """
    Creates simple SQLite database for Question Generator Agent
    Only 2 tables: topics and questions
    """

    if os.path.exists(DB_PATH):
        if debug:
            print(f"Database {DB_PATH} already exists.")
        if force_create_db:
            os.remove(DB_PATH)
        else:
            return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if debug:
        print(f"Creating database: {DB_PATH}")

    cursor.execute("""
        CREATE TABLE topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT
        )
    """)
    if debug:
        print("Table 'topics' created")

    cursor.execute("""
        CREATE TABLE questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic_id INTEGER NOT NULL,
            question_text TEXT NOT NULL,
            FOREIGN KEY (topic_id) REFERENCES topics (id) ON DELETE CASCADE
        )
    """)
    if debug:
        print("Table 'questions' created")

    cursor.execute("CREATE INDEX idx_questions_topic ON questions(topic_id)")

    conn.commit()
    if debug:
        print(f"Database {DB_PATH} successfully created!")

    conn.close()
    return DB_PATH


def execute_query(query: str, params: tuple = ()) -> List[Dict[str, Any]]:
    """Helper function to execute SQL query and return results as list of dicts"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(query, params)

        if query.strip().upper().startswith('SELECT'):
            results = [dict(row) for row in cursor.fetchall()]
        else:
            conn.commit()
            results = [{"affected_rows": cursor.rowcount, "last_id": cursor.lastrowid}]

        conn.close()
        return results
    except Exception as e:
        return [{"error": str(e)}]
