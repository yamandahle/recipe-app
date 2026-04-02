
import sqlite3

conn = sqlite3.connect("recipe_app.db")
cursor = conn.cursor()

# Table 1 (users)
cursor.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT ,
        email TEXT NOT NULL ,
        password  TEXT NOT NULL
    )
""")

# Table 2 (recipes)
cursor.execute
("""
    CREATE TABLE recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT ,
        title TEXT ,
        description TEXT ,
        ingredients TEXT ,
        steps TEXT ,
        image_url TEXT ,
        video_url TEXT ,
        category TEXT ,
        user_id INTEGER 
    )
""")



# Table 3 (saved_recipes)
cursor.execute("""
    CREATE TABLE saved_recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT ,
        user_id INTEGER ,
        recipe_id INTEGER 
    )
""")



# Table 4(rating)
cursor.execute("""
    CREATE TABLE ratings (
        id INTEGER PRIMARY KEY AUTOINCREMENT ,
        user_id INTEGER,
        recipe_id INTEGER ,
        score INTEGER 
    )
""")




# Table 5(comments)
cursor.execute("""
CREATE TABLE comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT ,
    user_id INTEGER  ,
    recipe_id INTEGER
)
""")




conn.commit()
conn.close()
print (" DataBase is created successfully ")