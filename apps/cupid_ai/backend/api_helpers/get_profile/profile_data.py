def get_user_profile(unique_id, conn):
    try:
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
            return None

        profile_column_names = [column[0] for column in cursor.description]
        profile_data = dict(zip(profile_column_names, profile))

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
        profile_data["user_general_questions"] = [question[0] for question in questions]

        return profile_data

    except Exception as e:
        print(f"Error fetching user profile: {e}")
        return None

    finally:
        cursor.close()
