import sqlite3

def init_db():
    conn = sqlite3.connect("circles.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS circles(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT
            )
        """)

    count = conn.execute("SELECT COUNT(*) FROM circles").fetchone()[0]
    if count == 0:
        conn.execute("INSERT INTO circles (name, category) VALUES (?, ?)", ("ロンロック", "音楽"))
        conn.execute("INSERT INTO circles (name, category) VALUES (?, ?)", ("クラッシックギター部", "音楽"))
        conn.execute("INSERT INTO circles (name, category) VALUES (?, ?)", ("サッカー部", "スポーツ"))
                                                     
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect("circles.db")
    conn.row_factory = sqlite3.Row
    return conn