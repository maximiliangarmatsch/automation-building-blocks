from flask import jsonify


def get_match_accepted(unique_id, conn):
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT DISTINCT from_user_id 
        FROM Accepted_match
        WHERE to_user_id = ?;
        """,
        (unique_id,),
    )
    match_ids = cursor.fetchall()
    accepted_unique_ids = [match_id[0] for match_id in match_ids]
    if not accepted_unique_ids:
        cursor.execute(
            """
            SELECT DISTINCT to_user_id 
            FROM Accepted_match
            WHERE from_user_id = ?;
            """,
            (unique_id,),
        )
        match_ids = cursor.fetchall()
        accepted_unique_ids = [match_id[0] for match_id in match_ids]
    if not accepted_unique_ids:
        return jsonify({"accepted_profiles": []})
    accepted_profiles = []
    for from_unique_id in accepted_unique_ids:
        cursor.execute(
            """
            SELECT attractiveness, relationship_type, family_planning, city, country, zipcode, occupation, languages, 
            bmi, working_hours,other_commitments, dating_availability, gender, height, weight, age, eye_color, 
            eye_type, hair_color, hair_length, hair_style, nose, facial_form, cheekbones, eyebrows, 
            sports, hobbies, overall_health, skin_helath, kids, pets, living_space, living_mates, wealth_splitting, 
            effort_splitting, religion, politics, existing_family_structure, retirement, smoking, drinking, drugs,
            financial_situation, dating_experince , taruma, legal_status
            FROM User_profile
            WHERE unique_id = ?;
            """,
            (from_unique_id,),
        )
        user_profile = cursor.fetchone()
        if not user_profile:
            continue
        user_profile_columns = [desc[0] for desc in cursor.description]
        user_profile_data = dict(zip(user_profile_columns, user_profile))
        cursor.execute(
            """
            SELECT *
            FROM Accepted_match
            WHERE from_user_id = ? AND to_user_id = ?;
            """,
            (from_unique_id, unique_id),
        )
        accepted_match_data = cursor.fetchall()
        if not accepted_match_data:
            cursor.execute(
                """
                SELECT *
                FROM Accepted_match
                WHERE from_user_id = ? AND to_user_id = ?;
                """,
                (unique_id, from_unique_id),
            )
            accepted_match_data = cursor.fetchall()
        if accepted_match_data:
            accepted_match_columns = [desc[0] for desc in cursor.description]
            accepted_match_data_dict = {}
            for row in accepted_match_data:
                for index, value in enumerate(row):
                    accepted_match_data_dict[accepted_match_columns[index]] = value
            merged_profile = {**user_profile_data, **accepted_match_data_dict}
            accepted_profiles.append(merged_profile)
    conn.close()
    return jsonify({"accepted_profiles": accepted_profiles})
