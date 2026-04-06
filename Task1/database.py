import sqlite3

def get_connection():
    conn = sqlite3.connect(r"/Users/mobcoderid-225/Desktop/TASK-1/Task1/database.db")
    # conn.row_factory = sqlite3.Row
    # return conn
    # conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS followers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        follower_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (follower_id) REFERENCES users (id)
    )
    """)
    conn.commit()
    conn.close()
    return sqlite3.connect(r"/Users/mobcoderid-225/Desktop/TASK-1/Task1/database.db")



def add_user(target_user_id: str, current_user_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO followers (user_id, follower_id) VALUES (?, ?)", (target_user_id, current_user_id))
    conn.commit()
    return "DONE"
    # conn.close()
    # return sqlite3.connect(r"/Users/mobcoderid-225/Desktop/TASK-1/Task1/database.db")

def search_user(username: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username LIKE ?", ('%' + username + '%',))
    conn.commit()
    users = cursor.fetchall()
    return {"users": users}

def create_post(post_data: dict):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO posts (user_id, content) VALUES (?, ?)", (post_data['user_id'], post_data['content']))
    conn.commit()
    return "Post created successfully"

def get_feed(user_id: str):
    conn= get_connection()
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

def like_post(post_id: str, user_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO likes (post_id, user_id) VALUES (?, ?)", (post_id, user_id))
    conn.commit()
    return "Post liked successfully"

def comment_on_post(post_id: str, user_id: str, comment: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO comments (post_id, user_id, comment) VALUES (?, ?, ?)", (post_id, user_id, comment))
    conn.commit()
    return "Comment added successfully"

def delete_comment(comment_id: str, user_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM comments WHERE id = ? AND user_id = ?", (comment_id, user_id))
    conn.commit()
    return "Comment deleted successfully"

def delete_post(post_id: str, user_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM posts WHERE id = ? AND user_id = ?", (post_id, user_id))
    conn.commit()
    return "Post deleted successfully"

def unfollow_user(target_user_id: str, current_user_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM followers WHERE user_id = ? AND follower_id = ?", (target_user_id, current_user_id))
    conn.commit()
    return "Unfollowed successfully"



