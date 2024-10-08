def insert_user_general_questions(cursor, profile_data):
    cursor.execute(
        """
        INSERT INTO User_profile_general_questions(
            user_id, g_q1, g_q2, g_q3, g_q4, g_q5, g_q6, g_q7, g_q8, g_q9, g_q10
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            profile_data["unique_id"],
            profile_data["g_q1"],
            profile_data["g_q2"],
            profile_data["g_q3"],
            profile_data["g_q4"],
            profile_data["g_q5"],
            profile_data["g_q6"],
            profile_data["g_q7"],
            profile_data["g_q8"],
            profile_data["g_q9"],
            profile_data["g_q10"],
        ),
    )
