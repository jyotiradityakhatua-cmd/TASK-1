import sqlite3
import uuid
import hashlib
from jwt import create_access_token,verify_token
from jose import jwt


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def get_connection():
    conn = sqlite3.connect(r"/Users/mobcoderid-225/Desktop/TASK-1/Task1/database.db")
    cursor = conn.cursor()
    # cursor.execute("PRAGMA table_info(users)")
    # columns = cursor.fetchall()
    # print(columns)
    


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS followers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        follower_id TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS posts (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        content TEXT NOT NULL
    )
    """)


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS likes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id TEXT NOT NULL,
        user_id TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id TEXT NOT NULL,
        user_id TEXT NOT NULL,
        comment TEXT NOT NULL
    )
    """)

    conn.commit()
    return conn


def register_user(username: str, password: str):
    conn = get_connection()
    cursor = conn.cursor()

    user_id = str(uuid.uuid4())
    hash_pass = str(hash_password(password))
    print(type(user_id))
    print(type(password))
    print(type(hash_pass))

    try:
        print("im here")
        cursor.execute(
            "INSERT INTO users (id, username, password, role) VALUES (?, ?, ?, ?)",
            (user_id, username, hash_pass, "user")
        )
        print("im here 2")
        conn.commit()
        print("im here 3")
        return {"message": "User registered successfully", "user_id": user_id}

    except Exception as e:
        return {f"message: Username already exists: {e}"}

    finally:
            conn.close()


def login_user(username: str, password: str):
    conn = get_connection()
    cursor = conn.cursor()

    hash_pass = hash_password(password)

    cursor.execute(
        "SELECT id, username FROM users WHERE username = ? AND password = ?",
        (username, hash_pass)
    )
    user = cursor.fetchone()

    if not user:
        return {"message": "Invalid username or password"}

    token = create_access_token({
        "user_id": user[0],
        "username": user[1]
    })

    conn.close()
    return {"token": token}


def add_user(target_user_id: str, current_user_id: str):
    conn = get_connection()
    cursor = conn.cursor()

    if target_user_id == current_user_id:
        return "You cannot follow yourself."

    cursor.execute(
        "SELECT * FROM followers WHERE user_id = ? AND follower_id = ?",
        (target_user_id, current_user_id)
    )

    if cursor.fetchone():
        return "Already following"

    cursor.execute(
        "INSERT INTO followers (user_id, follower_id) VALUES (?, ?)",
        (target_user_id, current_user_id)
    )

    conn.commit()
    conn.close()
    return "Followed successfully"


def unfollow_user(target_user_id: str, current_user_id: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM followers WHERE user_id = ? AND follower_id = ?",
        (target_user_id, current_user_id)
    )

    conn.commit()
    conn.close()
    return "Unfollowed successfully"



SECRET_KEY = "my_secret_key"   

def search_user_by_token(token: str):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")

        cursor.execute(
            "SELECT * FROM users WHERE id = ?",
            (user_id,)
        )

        user = cursor.fetchone()
        return {"user": user}

    except Exception as e:
        return {"error": f"Invalid token: {e}"}

    finally:
        conn.close()

    # users = cursor.fetchall()
    # conn.close()

    return {"users": users}


def create_post(post_data: dict):
    conn = get_connection()
    cursor = conn.cursor()

    post_id = str(uuid.uuid4())

    cursor.execute(
        "INSERT INTO posts (id, user_id, content) VALUES (?, ?, ?)",
        "ALTER COLUMN column_name token;"
        (post_id, post_data['user_id'], post_data['content'])
    )

    conn.commit()
    conn.close()
    return "Post created"


def get_feed(user_id: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT posts.content
    FROM posts
    JOIN followers ON posts.user_id = followers.user_id
    WHERE followers.follower_id = ?
    """, (user_id,))

    feed = cursor.fetchall()
    conn.close()
    return {"feed": feed}

def like_and_unlike_post(post_id: str, user_id: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM likes WHERE post_id = ? AND user_id = ?",
        (post_id, user_id)
    )

    if cursor.fetchone():
        cursor.execute(
            "DELETE FROM likes WHERE post_id = ? AND user_id = ?",
            (post_id, user_id)
        )
        conn.commit()
        conn.close()
        return "Unliked"

    cursor.execute(
        "INSERT INTO likes (post_id, user_id) VALUES (?, ?)",
        (post_id, user_id)
    )

    conn.commit()
    conn.close()
    return "Liked"


def comment_on_post(post_id: str, user_id: str, comment: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO comments (post_id, user_id, comment) VALUES (?, ?, ?)",
        (post_id, user_id, comment)
    )

    conn.commit()
    conn.close()
    return "Comment added"


def delete_comment(comment_id: str, user_id: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM comments WHERE id = ? AND user_id = ?",
        (comment_id, user_id)
    )

    conn.commit()
    conn.close()
    return "Comment deleted"


def delete_post(post_id: str, user_id: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM posts WHERE id = ? AND user_id = ?",
        (post_id, user_id)
    )

    conn.commit()
    conn.close()
    return "Post deleted"



