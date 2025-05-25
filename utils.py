import logging
import sqlite3
from pathlib import Path

# Logging Setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Database Path
DB_PATH = Path("analytics.db")

# Initialize DB schema (only once)
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS analytics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Log search safely
def log_search(prompt):
    try:
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        c = conn.cursor()
        c.execute("INSERT INTO analytics (prompt) VALUES (?)", (prompt,))
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Error logging search: {e}")
