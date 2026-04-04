from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import bcrypt #to hash the password 
from models import UserAuth
from models import RecipeCreate
from fastapi import Header
from jose import jwt #to generate a token 
from models import RatingCreate



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


#return one specific recipe 
@app.get("/recipes/{id}")
def get_one_recipe(id: int):

    #connect to the databse 
    conn = sqlite3.connect("recipe_app.db")
    cursor = conn.cursor()
    
    #find the specific recipe
    cursor.execute("SELECT * FROM recipes WHERE id = ?", (id,))
    recipe = cursor.fetchone()
    
    conn.close()

    if recipe is None :
        return{"message": "recipe is not found"}
    else:
        return {
            "id": recipe[0],
            "title": recipe[1],
            "description": recipe[2],
            "ingredients": recipe[3],
            "steps": recipe[4],
            "image_url": recipe[5],
            "video_url": recipe[6],
            "category": recipe[7],
            "user_id": recipe[8]
        }
    

#endpoint for deleting a recipe 
@app.delete("/recipes/{id}")
def delete_recipe(id: int ,token: str = Header()):

    user_id = get_current_user(token)

    #connect to the databse 
    conn = sqlite3.connect("recipe_app.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM recipes WHERE id = ?", (id,))
    recipe = cursor.fetchone()
    
    #if recipe dose not exist 
    if recipe is None:
        return {"message": "Recipe not found"}

    #check if the recipe belong to the user 
    if recipe[8] != user_id:
        return{"message": "you can only delete your own recipes"}
    else :
        cursor.execute("DELETE FROM recipes WHERE id = ?", (id,))
        return{"message": "recipe deleted successfully!"}

    conn.commit()
    conn.close()    


@app.post("/recipes/{id}/save")
def save_favorite_recipe(id: int , token: str = Header()):

    user_id = get_current_user(token)

    #connect to the databse 
    conn = sqlite3.connect("recipe_app.db")
    cursor = conn.cursor()
    
    #find the recipe 
    cursor.execute("SELECT * FROM recipes WHERE id = ?", (id,))
    recipe = cursor.fetchone()
    
    #check if the recipe already saved 
    cursor.execute(
    "SELECT * FROM saved_recipes WHERE user_id = ? AND recipe_id = ?",
    (user_id, id)
    )
    saved = cursor.fetchone()


    #if the recipe does not exist 
    if recipe is None:
        conn.close()
        return {"message": "recipe does not exist "}
    
    #if the recipe is already saved 
    elif saved is not None :
        cursor.execute(
            "DELETE FROM saved_recipes WHERE user_id = ? AND recipe_id = ?",
            (user_id, id)
        )
        conn.commit()
        conn.close()
        return {"message": "Recipe unsaved!"}
    
    #if everything is ok 
    else:
        cursor.execute(
            "INSERT INTO saved_recipes (user_id, recipe_id) VALUES (?, ?)",
            (user_id, id)
        )
        conn.commit()
        conn.close()
        return {"message": "Recipe saved!"}
    
    
@app.post("/recipes/{id}/rate")
def rate(id: int , score: RatingCreate , token: str = Header()):

    user_id = get_current_user(token)

    #connect to the databse 
    conn = sqlite3.connect("recipe_app.db")
    cursor = conn.cursor()
    
    #find the recipe 
    cursor.execute("SELECT * FROM recipes WHERE id = ?", (id,))
    recipe = cursor.fetchone()

    #check if already rated
    cursor.execute("SELECT * FROM ratings WHERE user_id = ? AND recipe_id = ?", (user_id, id))
    previous_rating = cursor.fetchone()

    #if the recipe does not exist 
    if recipe is None:
        conn.close()
        return {"message": "recipe does not exist "}
    
    #if there us a previous rating , update it 
    elif previous_rating is not None:
        cursor.execute("UPDATE ratings SET score = ? WHERE user_id = ? AND recipe_id = ?", (score.score, user_id, id))
        # get average:
        cursor.execute("SELECT AVG(score) FROM ratings WHERE recipe_id = ?", (id,))
        result = cursor.fetchone()
        average = result[0]  
        conn.commit()
        conn.close()
        return {
            "message": "Rating updated!",
            "average_rating": round(average, 1)  
        }        


    #add new rating 
    else:
        cursor.execute("INSERT INTO ratings (user_id, recipe_id, score) VALUES (?, ?, ?)", (user_id, id, score.score))   
        # get average:
        cursor.execute("SELECT AVG(score) FROM ratings WHERE recipe_id = ?", (id,))
        result = cursor.fetchone()
        average = result[0]  
        conn.commit()
        conn.close()
        return {
            "message": "Rating submitted!",
            "average_rating": round(average, 1)  
        }    
    
 


        
        
    












    


         







