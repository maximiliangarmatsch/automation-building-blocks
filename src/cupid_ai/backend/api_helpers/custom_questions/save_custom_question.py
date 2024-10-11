from helpers import get_next_question_id


def save_custom_question(to_user_id, from_user_id, question, conn):
    question_id = get_next_question_id(to_user_id, from_user_id, conn)
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO User_Match_Questions (question_id, to_user_id, from_user_id, question, answer)
            VALUES (?, ?, ?, ?, ?)
            """,
            (question_id, to_user_id, from_user_id, question, ""),
        )
        conn.commit()
        conn.close()
        return {
            "message": "Question added successfully!",
            "question_id": question_id,
        }, 200
    except Exception as e:
        return {"error": str(e)}, 500
