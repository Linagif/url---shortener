import sqlite3

DB_PATH = "urls.db"


def get_connection():
    """Open a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # lets us read columns by name
    return conn


def init_db():
    """Create the urls table if it doesn't exist yet."""
    conn = get_connection()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS urls (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                original_url TEXT    NOT NULL,
                short_code   TEXT    NOT NULL UNIQUE,
                created_at   TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP,
                clicks       INTEGER NOT NULL DEFAULT 0
            )
        """)
        conn.commit()
    finally:
        conn.close()


def save_url(original_url, short_code):
    """Store a new short code and its original URL."""
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO urls (original_url, short_code) VALUES (?, ?)",
            (original_url, short_code),
        )
        conn.commit()
    finally:
        conn.close()


def get_url_by_code(short_code):
    """Return the row for a short code as a dict, or None if not found."""
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM urls WHERE short_code = ?", (short_code,)
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def increment_clicks(short_code):
    """Add 1 to the click counter for a short code."""
    conn = get_connection()
    try:
        conn.execute(
            "UPDATE urls SET clicks = clicks + 1 WHERE short_code = ?",
            (short_code,),
        )
        conn.commit()
    finally:
        conn.close()