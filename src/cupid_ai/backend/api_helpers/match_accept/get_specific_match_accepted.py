import json


def get_specific_match_accepted(from_user_id, to_user_id, conn):
    cursor = conn.cursor()

    # Fetch from_user general questions
    cursor.execute(
        """
        SELECT question_id, question
        FROM User_profile_general_questions
        WHERE user_id = ?
        """,
        (from_user_id,),
    )
    from_user_general_questions = cursor.fetchall()

    # Fetch specific questions between users
    cursor.execute(
        """
        SELECT question_id, question, answer, rating
        FROM User_Match_Questions
        WHERE from_user_id = ? AND to_user_id = ?
        """,
        (from_user_id, to_user_id),
    )
    from_user_specific_questions = cursor.fetchall()

    # Fetch from_user profile
    cursor.execute(
        """
        SELECT *
        FROM User_profile
        WHERE unique_id = ?
        """,
        (from_user_id,),
    )
    from_user_profile = cursor.fetchone()

    # Fetch to_user general questions
    cursor.execute(
        """
        SELECT question_id, question
        FROM User_profile_general_questions
        WHERE user_id = ?
        """,
        (to_user_id,),
    )
    to_user_general_questions = cursor.fetchall()

    # Fetch answers from Accepted_match table
    cursor.execute(
        """
        SELECT answer
        FROM Accepted_match
        WHERE from_user_id = ? AND to_user_id = ?
        """,
        (from_user_id, to_user_id),
    )
    accepted_match_row = cursor.fetchone()

    match_general_answers = {}
    user_general_answers = {}

    if accepted_match_row:
        try:
            accepted_match_data = json.loads(accepted_match_row[0])
            match_general_answers = accepted_match_data.get(
                "match_general_questions_answer", {}
            )
            user_general_answers = accepted_match_data.get(
                "user_general_questions_answer", {}
            )
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
    to_user_questions_with_answers = []
    for question_id, question_text in to_user_general_questions:
        answer = match_general_answers.get(question_id, None)
        to_user_questions_with_answers.append(
            {"question_id": question_id, "question": question_text, "answer": answer}
        )
    result = {
        "from_user": {
            "profile": from_user_profile,
            "general_questions": from_user_general_questions,
            "specific_questions": from_user_specific_questions,
        },
        "to_user": {"general_questions_with_answers": to_user_questions_with_answers},
    }

    return result
