import sqlite3

conn = sqlite3.connect("recipe_app.db")
cursor = conn.cursor()

# Table 1 - users
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL,
        password TEXT NOT NULL,
        full_name TEXT NOT NULL       
               
    )
""")

# Table 2 - recipes
cursor.execute("""
    CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        ingredients TEXT,
        steps TEXT,
        image_url TEXT,
        video_url TEXT,
        category TEXT,
        user_id INTEGER
    )
""")

# Table 3 - saved_recipes
cursor.execute("""
    CREATE TABLE IF NOT EXISTS saved_recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        recipe_id INTEGER
    )
""")

# Table 4 - ratings
cursor.execute("""
    CREATE TABLE IF NOT EXISTS ratings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        recipe_id INTEGER,
        score INTEGER
    )
""")

# Table 5 - comments
cursor.execute("""
    CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        recipe_id INTEGER,
        text TEXT,
        created_at TEXT
    )
""")

conn.commit()
conn.close()
print("Database created successfully!")