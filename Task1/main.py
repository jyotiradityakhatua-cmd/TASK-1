from fastapi import FastAPI
from database import add_user, search_user, create_post, get_feed, like_post, comment_on_post, delete_comment, delete_post, unfollow_user


app = FastAPI()


@app.get("/")
def home():
    return {"message": "Welcome to the Instagram Clone FastAPI application!"}


@app.get("/follow")
def add_following(target_user_id: str, current_user_id: str):
    return add_user(target_user_id, current_user_id)

@app.get("/search_user")
def find_user(username: str):
    return search_user(username)

@app.post("/posts")
def make_post(post_data: dict):
    return create_post(post_data)

@app.get("/Feed")
def take_feed(user_id: str):
    return get_feed(user_id)

@app.post("/Like/unlike")
def like_the_post(post_id: str, user_id: str):
    return like_post(post_id, user_id)

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