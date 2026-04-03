from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import bcrypt #to hash the password 
from models import UserAuth
from models import RecipeCreate
from fastapi import Header
from jose import jwt #to generate a token 



#open the server
app = FastAPI()  

secret_key = "mysecretkey123"#to generate the token 


###register endpoint 
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



###login endpoint
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
            token = jwt.encode({"user_id": user[0]},secret_key,algorithm="HS256")#generate new token
            return {"token": token} 
        
        #if wrong 
        elif check_password == False:
            return {"message": "Wrong password"}
        

    #if the email does not exist     
    elif user == None:
        return {"message": "Email does not exist"}
    

###helper function that return the user id according to the token 
def get_current_user(token: str = Header()):
    data = jwt.decode(token, secret_key, algorithms=["HS256"])
    return data["user_id"]


@app.post("/recipes")
def create_recipe(new_recipe: RecipeCreate ,token: str=Header()):

    user_id = get_current_user(token)#get the user id
    
    #connect to the database
    conn = sqlite3.connect("recipe_app.db")
    cursor = conn.cursor()


    #insert a new recipe into the database and save it 
    cursor.execute("INSERT INTO recipes (title , description , ingredients , steps , image_url , video_url , category , user_id ) VALUES ( ? , ? , ? , ? , ? , ? , ? ,?)" 
                   , ( new_recipe.title ,new_recipe.description , new_recipe.ingredients , new_recipe.steps , new_recipe.image_url , new_recipe.video_url , new_recipe.category ,user_id))
    
    conn.commit()
    conn.close() 
    


    
    return{"message": "Recipe added successfully" }





#return a list of recipes 
@app.get("/recipes")
def get_recipes():

    #connect to the databse 
    conn = sqlite3.connect("recipe_app.db")
    cursor = conn.cursor()

    #find the recipes 
    cursor.execute("SELECT * FROM recipes")
    rows = cursor.fetchall()
    conn.close()

    #order them in list beautifully 
    recipes = []
    for row in rows:
        recipes.append({
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "ingredients": row[3],
            "steps": row[4],
            "image_url": row[5],
            "video_url": row[6],
            "category": row[7],
            "user_id": row[8]
        })
    return {"recipes": recipes}


         







