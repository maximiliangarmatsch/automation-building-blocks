import random
import hashlib


def generate_unique_id(user_id):
    random_number = random.randint(100000, 999999)  # Random 6-digit number
    return f"#{user_id}{random_number}"


def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def extract_user_login_data(request_data):
    if (
        not request_data
        or "email" not in request_data
        or "password" not in request_data
    ):
        return None, "Missing email or password", 422

    email = request_data["email"]
    password = request_data["password"]

    if not email or not password:
        return None, "Email and password are required", 400

    return {"email": email, "password": password}, None, None


def hash_user_password(password):
    return hash_password(password)


def fetch_user_by_email(conn, email):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM User WHERE email = ?", (email,))
    return cursor.fetchone()


def authenticate_user(user, hashed_password):
    if user and user[2] == hashed_password:
        return {"message": "Authentication successful!", "unique_id": user[3]}, 200
    elif user:
        return {"message": "Invalid password!"}, 401
    return None
