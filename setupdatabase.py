import sqlite3

def setup_database():
    conn = sqlite3.connect('college_info.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        fees TEXT,
        facilities TEXT,
        description TEXT,
        image_url TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS hostels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        fees TEXT,
        facilities TEXT,
        description TEXT,
        image_url TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS general_info (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT,
        info TEXT,
        image_url TEXT
    )
    ''')

    conn.commit()
    conn.close()

setup_database()
