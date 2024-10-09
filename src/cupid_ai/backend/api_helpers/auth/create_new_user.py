from api_helpers.auth.helpers import generate_unique_id


def create_new_user(conn, email, hashed_password):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO User (email, password) VALUES (?, ?)", (email, hashed_password)
    )
    user_id = cursor.lastrowid
    unique_id = generate_unique_id(user_id)
    cursor.execute("UPDATE User SET unique_id = ? WHERE id = ?", (unique_id, user_id))
    conn.commit()
    return unique_id
