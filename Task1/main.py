from fastapi import FastAPI, HTTPException, Header, Depends
from database import add_user, search_user_by_token, create_post, get_feed, like_and_unlike_post, comment_on_post, delete_comment, delete_post, unfollow_user, register_user, login_user
from jwt import create_access_token, verify_token
from pydantic import BaseModel
from database import login_user, search_user_by_token

app = FastAPI()


class RegisterRequest(BaseModel):
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

def get_current_user(authorization: str = Header(...)):
    try:
        token = authorization.split(" ")[1]
    except IndexError:
        raise HTTPException(status_code=401, detail="Invalid token format")

    payload = verify_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload


@app.post("/register")
def register_the_user(data: RegisterRequest):
    return register_user(data.username, data.password)

@app.post("/login")
def login_the_user(data: LoginRequest):
    user = login_user(data.username, data.password)
    if "token" not in user:
            raise HTTPException(status_code=401, detail="Invalid username or password")
    return user


@app.get("/")
def home():
    return {"message": "Welcome to the Instagram Clone FastAPI application!"}


@app.post("/follow")
def add_following(target_user_id: str, current_user_id: str):
    return add_user(target_user_id, current_user_id)

@app.get("/search_user")
def find_user(token: str):
    return search_user_by_token(token)

@app.post("/posts")
def make_post(post_data: dict):
    return create_post(post_data)

@app.get("/Feed")
def take_feed(user_id: str):
    return get_feed(user_id)

@app.post("/Like/unlike")
def like_the_post_and_unlike(post_id: str, user_id: str):
    return like_and_unlike_post(post_id, user_id)


@app.post("/Comment")
def comment_on_the_post(post_id: str, user_id: str, comment: str):
    return comment_on_post(post_id, user_id, comment)

@app.delete("/Comment/delete")
def delete_the_comment(comment_id: str, user_id: str):
    return delete_comment(comment_id, user_id)

@app.delete("/Post/delete")
def delete_the_post(post_id: str, user_id: str):
    return delete_post(post_id, user_id)

@app.delete("/unfollow")
def unfollow_the_user(target_user_id: str, current_user_id: str):
    return unfollow_user(target_user_id, current_user_id)