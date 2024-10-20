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


def get_specific_match(from_unique_id, to_unique_id, conn):
    cursor = conn.cursor()
    from_user_general_questions = fetch_general_questions(from_unique_id, conn)
    cursor.execute(
        """
        SELECT unique_id, attractiveness, relationship_type, family_planning, city, country, zipcode, occupation, languages, 
        bmi, working_hours, other_commitments, dating_availability, gender, height, weight, age, eye_color, 
        eye_type, hair_color, hair_length, hair_style, nose, facial_form, cheekbones, eyebrows, 
        sports, hobbies, overall_health, skin_helath, kids, pets, living_space, living_mates, wealth_splitting, 
        effort_splitting, religion, politics, existing_family_structure, retirement, smoking, drinking, drugs,
        financial_situation, dating_experince, taruma, legal_status
        FROM User_profile
        WHERE unique_id = ?
        """,
        (to_unique_id,),
    )
    matched_profile = cursor.fetchall()
    profile_dict = {}
    if matched_profile:
        columns = [column[0] for column in cursor.description]
        for row in matched_profile:
            profile_dict = dict(zip(columns, row))
            profile_dict["user_general_questions"] = [
                question[0] for question in from_user_general_questions
            ]
            match_general_questions = fetch_general_questions(
                profile_dict["unique_id"], conn
            )
            profile_dict["match_general_questions"] = [
                question[0] for question in match_general_questions
            ]
        conn.close()
        return profile_dict
    conn.close()
    return {"profiles": []}  # Return a regular dictionary
