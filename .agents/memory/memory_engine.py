# -*- coding: utf-8 -*-
"""
Memory Engine (SQLite FTS5 Kognitiv Tezkor Xotira)
Muallif: MuzaffarZed
Standart: MUTLAQ MUKAMMALLIK (Zero-Beta, Zero-Defect)
"""

import os
import sys
import sqlite3
from datetime import datetime

DB_PATH = os.path.join(r"C:\Users\MuzaffarZed\ai_workspace\.agents\memory", "brain_vault.db")

class MemoryEngine:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT,
                    title TEXT,
                    content TEXT,
                    tags TEXT,
                    created_at TEXT
                )
            """)
            c.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS memory_fts USING fts5(
                    title, content, tags, content='memories', content_rowid='id'
                )
            """)
            conn.commit()

    def add_memory(self, category, title, content, tags=""):
        now = datetime.now().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute(
                "INSERT INTO memories (category, title, content, tags, created_at) VALUES (?, ?, ?, ?, ?)",
                (category, title, content, tags, now)
            )
            row_id = c.lastrowid
            c.execute(
                "INSERT INTO memory_fts (rowid, title, content, tags) VALUES (?, ?, ?, ?)",
                (row_id, title, content, tags)
            )
            conn.commit()
            return row_id

    def search(self, query, limit=5):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            try:
                c.execute("""
                    SELECT m.id, m.category, m.title, m.content, m.tags 
                    FROM memory_fts f
                    JOIN memories m ON f.rowid = m.id
                    WHERE memory_fts MATCH ? 
                    ORDER BY rank LIMIT ?
                """, (query, limit))
                return c.fetchall()
            except sqlite3.OperationalError:
                # Fallback to LIKE
                c.execute("""
                    SELECT id, category, title, content, tags FROM memories
                    WHERE title LIKE ? OR content LIKE ? LIMIT ?
                """, (f"%{query}%", f"%{query}%", limit))
                return c.fetchall()

if __name__ == "__main__":
    engine = MemoryEngine()
    engine.add_memory("architecture", "Zero-Defect Standarti", "Muzaffar doimo 100% tayyor mahsulot talab qiladi.", "zero-defect,arxitektura")
    results = engine.search("Zero-Defect")
    print(f"[MemoryEngine] Test qidiruv natijasi ({len(results)} ta topildi):")
    for r in results:
        print(f"  - [{r[1]}] {r[2]}: {r[3]}")
    print("*Dasturchi: MuzaffarZed*")
