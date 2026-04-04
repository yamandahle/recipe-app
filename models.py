from pydantic import BaseModel

class RegisterUser(BaseModel):
    email: str
    password: str 
    full_name: str

class LoginUser(BaseModel):
    email: str
    password: str



class RecipeCreate(BaseModel):
    title: str 
    description: str 
    ingredients: str 
    steps: str
    image_url: str
    video_url: str
    category: str      

class RatingCreate(BaseModel):
    score: int  # 1 to 5   

class CommentCreate(BaseModel):
    comment: str     



