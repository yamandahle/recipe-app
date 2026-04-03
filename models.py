from pydantic import BaseModel


class UserAuth(BaseModel):
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



