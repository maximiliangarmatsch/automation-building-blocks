def get_user_profile(unique_id, conn):
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT * 
        FROM User_Profile 
        WHERE unique_id = ?
        """,
        (unique_id,),
    )
    profile = cursor.fetchone()
    if not profile:
        conn.close()
        return None
    cursor.execute(
        """
        SELECT question 
        FROM User_profile_general_questions
        WHERE user_id = ?
        ORDER BY id ASC
        """,
        (unique_id,),
    )
    questions = cursor.fetchall()
    column_names = [column[0] for column in cursor.description]
    profile_data = dict(zip(column_names, profile))
    profile_data["user_general_questions"] = [question[0] for question in questions]
    return profile_data
