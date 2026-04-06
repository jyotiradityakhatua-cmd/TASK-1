from fastapi import FastAPI
from database import add_user
import sqlite3

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Welcome to the FastAPI application!"}


@app.get("/follow")
def add_following(target_user_id: str, current_user_id: str):
    return add_user(target_user_id, current_user_id)

@app.get("/search_user")
def search_user(username: str):
    return username

@app.post("/posts")
def create_post(post_data: dict):
    return post_data

@app.get("/Feed")
def get_feed(user_id: str):
    return user_id

@app.get("/Like/unlike")
def like_post(post_id: str, user_id: str):
    return {"post_id": post_id, "user_id": user_id}

@app.get("/Comment")
def comment_on_post(post_id: str, user_id: str, comment: str):
    return {"post_id": post_id, "user_id": user_id, "comment": comment}
