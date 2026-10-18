import sqlite3
from pathlib import Path

DB_PATH=Path(__file__).parent/'expenses.db'

def create_database(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    conn.execute("""CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, amount REAL NOT NULL, category TEXT NOT NULL, date TEXT NOT NULL)""")
    conn.commit()
    conn.close()
if __name__=='__main__':
    create_database()
    print('Database ready: ', DB_PATH)
