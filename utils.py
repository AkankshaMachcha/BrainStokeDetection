import sqlite3

def create_database():
    conn = sqlite3.connect('data/users_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            email TEXT NOT NULL UNIQUE,
            date TEXT NOT NULL,
            address TEXT NOT NULL,
            mobile TEXT NOT NULL UNIQUE,
            image_path TEXT NOT NULL,
            feedback TEXT DEFAULT NULL
        )
    ''')
    conn.commit()
    conn.close()


from utils import create_database
create_database()
