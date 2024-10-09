def insert_user_general_questions(cursor, profile_data):
    user_id = profile_data["unique_id"]
    questions = profile_data["user_general_questions"]
    for index, question in enumerate(questions, start=1):
        question_id = f"{user_id}_gq{index}"

        cursor.execute(
            """
            INSERT INTO User_profile_general_questions (user_id, question_id, question)
            VALUES (?, ?, ?)
            """,
            (user_id, question_id, question),
        )
