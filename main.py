from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import bcrypt
from models import UserAuth



#open the server
app = FastAPI()  


###register method 
@app.post("/register")
def register(user: UserAuth):

    # hash the password
    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"),bcrypt.gensalt())

    # save to database
    conn = sqlite3.connect("recipe_app.db")
    cursor = conn.cursor()
    

    #add a new user to the users table
    cursor.execute(
        "INSERT INTO users (email, password) VALUES (?, ?)",
        (user.email, hashed_password.decode("utf-8"))
    )

    conn.commit()
    conn.close()

    return {"message": "User registered successfully!"}



###login method
@app.post("/login")
def login(auth: UserAuth):

    conn = sqlite3.connect("recipe_app.db")
    cursor = conn.cursor()
 

    #check if the email exists 
    cursor.execute("SELECT * FROM users WHERE email = ?", (auth.email,))
    user = cursor.fetchone()
    conn.close() 
    
    if user != None:
        #check if the password matches is correct
        check_password = bcrypt.checkpw(auth.password.encode("utf-8"),user[2].encode("utf-8"))

        #if the password is correct send success message 
        if check_password == True:
            return {"message": "Login successful!"}
        #if wrong 
        elif check_password == False:
            return {"message": "Wrong password"}
    #if the email does not exist     
    elif user == None:
        return {"message": "Email does not exist"}

         







