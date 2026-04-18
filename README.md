# 🍳 Recipe App — Backend

A RESTful API built with FastAPI and Python for a recipe sharing community platform.

## What is this project?

A backend API for a food community app where users can share recipes, rate them, comment on them, and save their favorites — like Instagram but for food!

## Tech Stack

- **Python** — programming language
- **FastAPI** — web framework for building APIs
- **SQLite** — lightweight database
- **SQL** — database queries
- **JWT (JSON Web Tokens)** — user authentication
- **bcrypt** — secure password hashing
- **python-multipart** — file upload support

## Features

- User registration and login with JWT authentication
- Add, view and delete recipes
- Upload recipe photos
- Save/unsave favorite recipes
- Rate recipes (1-5 stars)
- Add and delete comments
- User profile with their recipes

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /register | Register a new user |
| POST | /login | Login and get token |
| GET | /recipes | Get all recipes |
| POST | /recipes | Add a new recipe |
| GET | /recipes/{id} | Get one recipe |
| DELETE | /recipes/{id} | Delete a recipe |
| POST | /recipes/{id}/save | Save/unsave a recipe |
| POST | /recipes/{id}/rate | Rate a recipe |
| GET | /recipes/{id}/rating | Get average rating |
| POST | /recipes/{id}/comments | Add a comment |
| GET | /recipes/{id}/comments | Get all comments |
| DELETE | /comments/{id} | Delete a comment |
| POST | /upload | Upload an image |
| GET | /me | Get current user info |
| GET | /me/recipes | Get my recipes |
| GET | /me/saved | Get saved recipes |

## How to Run Locally

**1. Clone the repository:**
```bash
git clone https://github.com/yamandahle/recipe-app.git
cd recipe-app
```

**2. Install dependencies:**
```bash
pip install fastapi uvicorn bcrypt python-jose python-multipart
```

**3. Create the database:**
```bash
python database.py
```

**4. Run the server:**
```bash
python -m uvicorn main:app --reload
```

**5. Open the API docs:**
```
http://127.0.0.1:8000/docs
```

## Project Structure

```
Recipe_App/
├── main.py          → All API endpoints
├── database.py      → Database tables setup
├── models.py        → Pydantic data models
├── uploads/         → Uploaded recipe images
└── recipe_app.db    → SQLite database file
```