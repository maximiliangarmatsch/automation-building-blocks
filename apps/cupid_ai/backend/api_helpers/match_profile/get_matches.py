from flask import jsonify


def fetch_general_questions(unique_id, conn):
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT question 
        FROM User_profile_general_questions
        WHERE user_id = ?
        ORDER BY id ASC
        """,
        (unique_id,),
    )
    user_questions = cursor.fetchall()
    return user_questions


def get_matches(unique_id, conn):
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT DISTINCT match_unique_id 
        FROM match_profile
        WHERE your_unique_id = ?;
        """,
        (unique_id,),
    )
    match_ids = cursor.fetchall()

    # Extract match IDs from the result set
    match_unique_ids = [match_id[0] for match_id in match_ids]

    user_general_questions = fetch_general_questions(unique_id, conn)

    # Proceed only if there are matches and user questions
    if match_unique_ids and user_general_questions:
        placeholders = ", ".join(["?"] * len(match_unique_ids))
        cursor.execute(
            f"""
            SELECT * 
            FROM User_profile
            WHERE unique_id IN ({placeholders});
            """,
            match_unique_ids,
        )

        matched_profiles = cursor.fetchall()

        # If matched profiles are found, format the results
        if matched_profiles:
            columns = [column[0] for column in cursor.description]
            profiles = []
            for row in matched_profiles:
                profile_dict = dict(zip(columns, row))

                # Attach the current user's general questions to the profile
                profile_dict["user_general_questions"] = [
                    question[0] for question in user_general_questions
                ]

                # Fetch and attach the matched user's general questions
                match_general_questions = fetch_general_questions(
                    profile_dict["unique_id"], conn
                )
                profile_dict["match_general_questions"] = [
                    question[0] for question in match_general_questions
                ]

                profiles.append(profile_dict)

            conn.close()
            return jsonify({"profiles": profiles})

    conn.close()
    return jsonify({"profiles": []})
