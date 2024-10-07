def get_user_and_profile_data(your_unique_id, match_unique_id, conn):
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT * FROM User_profile WHERE unique_id = ?;
            """,
            (match_unique_id,),
        )
        match_profile_data = cursor.fetchone()

        if not match_profile_data:
            return {"success": False, "message": "Match user data not found."}
        cursor.execute(
            """
            SELECT g_q1, g_q2, g_q3, g_q4, g_q5, g_q6, g_q7, g_q8, g_q9, g_q10
            FROM User_profile_general_questions WHERE user_id = ?;
            """,
            (match_unique_id,),
        )
        match_general_questions = cursor.fetchone()
        cursor.execute(
            """
            SELECT g_q1, g_q2, g_q3, g_q4, g_q5, g_q6, g_q7, g_q8, g_q9, g_q10
            FROM User_profile_general_questions WHERE user_id = ?;
            """,
            (your_unique_id,),
        )
        your_general_questions = cursor.fetchone()

        if not your_general_questions:
            return {
                "success": False,
                "message": "Your general questions data not found.",
            }
        result = {
            "match_profile_data": match_profile_data,
            "match_general_questions": {
                "g_q1": match_general_questions[0],
                "g_q2": match_general_questions[1],
                "g_q3": match_general_questions[2],
                "g_q4": match_general_questions[3],
                "g_q5": match_general_questions[4],
                "g_q6": match_general_questions[5],
                "g_q7": match_general_questions[6],
                "g_q8": match_general_questions[7],
                "g_q9": match_general_questions[8],
                "g_q10": match_general_questions[9],
            },
            "your_general_questions": {
                "g_q1": your_general_questions[0],
                "g_q2": your_general_questions[1],
                "g_q3": your_general_questions[2],
                "g_q4": your_general_questions[3],
                "g_q5": your_general_questions[4],
                "g_q6": your_general_questions[5],
                "g_q7": your_general_questions[6],
                "g_q8": your_general_questions[7],
                "g_q9": your_general_questions[8],
                "g_q10": your_general_questions[9],
            },
        }

    except Exception as e:
        return {"success": False, "message": str(e)}
    finally:
        conn.close()

    return {"success": True, "data": result}
