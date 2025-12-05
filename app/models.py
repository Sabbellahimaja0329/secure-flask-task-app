import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

DB_CONF = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASS", ""),
    "database": os.getenv("DB_NAME", "task_app_db"),
    "autocommit": True
}

def get_db():
    return mysql.connector.connect(**DB_CONF)

# helper examples
def get_user_by_email(email):
    cnx = get_db()
    cur = cnx.cursor(dictionary=True)
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()
    cnx.close()
    return user

def create_user(name, email, password_hash, role='user'):
    cnx = get_db()
    cur = cnx.cursor()
    cur.execute(
        "INSERT INTO users (name, email, password_hash, role) VALUES (%s,%s,%s,%s)",
        (name, email, password_hash, role)
    )
    cnx.close()