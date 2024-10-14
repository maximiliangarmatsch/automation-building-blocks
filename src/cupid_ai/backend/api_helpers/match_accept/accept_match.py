def check_existing_match(conn, data):
    to_user_id = data.get("to_user_id")
    from_user_id = data.get("from_user_id")
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT 1 FROM Accepted_match 
        WHERE to_user_id = ? AND from_user_id = ?;
        """,
        (to_user_id, from_user_id),
    )
    return cursor.fetchone()


def insert_accepted_match(conn, data):
    cursor = conn.cursor()
    to_user_id = data.get("to_user_id")
    from_user_id = data.get("from_user_id")
    answer = data.get("answer")
    cursor.execute(
        """
        INSERT INTO Accepted_match (to_user_id, from_user_id, answer, status)
        VALUES (?, ?, ?, 'No');
        """,
        (to_user_id, from_user_id, answer),
    )
    conn.commit()
