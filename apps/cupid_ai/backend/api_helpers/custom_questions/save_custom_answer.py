def save_customize_answer(to_user_id, from_user_id, question_id, answer, conn):
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE User_Match_Questions
            SET answer = ?
            WHERE question_id = ? AND to_user_id = ? AND from_user_id = ?
            """,
            (answer, question_id, to_user_id, from_user_id),
        )
        if cursor.rowcount == 0:
            return {"error": "No matching question found."}, 404
        conn.commit()
        conn.close()
        return {"message": "Answer submitted successfully!"}, 200
    except Exception as e:
        return {"error": str(e)}, 500
