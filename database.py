import sqlite3

DB_NAME = "feedback.db"

def connect_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    return conn, cursor
    
def create_table():
    conn, cursor = connect_db()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            feedback TEXT NOT NULL,
            intent TEXT,
            topic TEXT,
            priority TEXT,
            confidence REAL,
            status TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_feedback(source, feedback, intent, topic, priority, confidence, status):
    conn, cursor = connect_db()
    cursor.execute("""
    INSERT INTO feedback (source, feedback, intent, topic, priority, confidence, status)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (source, feedback, intent, topic, priority, confidence, status))
    conn.commit()
    conn.close()

def get_review_queue():
    conn, cursor = connect_db()
    cursor.execute("""
        SELECT id, source, feedback, intent, topic, priority, confidence, status
        FROM feedback
        WHERE status = 'needs_review'
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    create_table()
    print("Database and table created successfully")