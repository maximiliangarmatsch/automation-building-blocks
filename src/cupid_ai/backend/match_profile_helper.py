import sqlite3
from flask import jsonify


def save_match_profile(your_unique_id, match_unique_id, conn):
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO Match_profile (your_unique_id, match_unique_id)
            VALUES (?, ?);
        """,
            (your_unique_id, match_unique_id),
        )
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return jsonify({"success": False, "message": str(e)})
    finally:
        conn.close()
    return jsonify({"success": True, "message": "Match profile saved successfully."})


def get_match_profiles(unique_id, conn):
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT DISTINCT match_unique_id FROM match_profile
        WHERE your_unique_id = ?;
    """,
        (unique_id,),
    )
    match_ids = cursor.fetchall()
    match_unique_ids = [match_id[0] for match_id in match_ids]
    print(match_ids)
    cursor.execute(
        """
        SELECT q1, q2, q3, q4, q5, q6, q7, q8, q9, q10 
        FROM User_profile
        WHERE unique_id = ?;
    """,
        (unique_id,),
    )
    user_questions = cursor.fetchone()
    if match_unique_ids and user_questions:
        placeholders = ", ".join(["?"] * len(match_unique_ids))
        cursor.execute(
            f"""
            SELECT * FROM User_profile
            WHERE unique_id IN ({placeholders});
        """,
            match_unique_ids,
        )
        matched_profiles = cursor.fetchall()
        if matched_profiles:
            columns = [column[0] for column in cursor.description]
            profiles = []
            for row in matched_profiles:
                profile_dict = dict(zip(columns, row))
                for i, q in enumerate(user_questions, 1):
                    profile_dict[f"your_q{i}"] = q
                profiles.append(profile_dict)
            conn.close()
            return jsonify({"profiles": profiles})
    conn.close()
    return jsonify({"profiles": []})


def get_accepted_profiles(unique_id, conn):
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT DISTINCT your_unique_id FROM Accepted_match
        WHERE match_unique_id = ?;
        """,
        (unique_id,),
    )
    match_ids = cursor.fetchall()
    accepted_unique_ids = [match_id[0] for match_id in match_ids]
    if not accepted_unique_ids:
        cursor.execute(
            """
            SELECT DISTINCT match_unique_id FROM Accepted_match
            WHERE your_unique_id = ?;
            """,
            (unique_id,),
        )
        match_ids = cursor.fetchall()
        accepted_unique_ids = [match_id[0] for match_id in match_ids]
    if not accepted_unique_ids:
        return jsonify({"accepted_profiles": []})
    accepted_profiles = []
    for your_unique_id in accepted_unique_ids:
        cursor.execute(
            """
            SELECT attractiveness, relationship_type, family_planning, living_address, apartment_style, roommates, working_hours,
            other_commitments, dating_availability, gender, height, weight, age, eye_color, eye_type, hair_color, hair_length,
            hair_style, nose, facial_form, cheekbones, eyebrows, dept, assets, income_this_year, income_next_year, income_over_next_year,
            wealth_goals, kids, pets, living, wealth_splitting, effort_splitting, religion, politics, existing_family_structure,
            retirement
            FROM User_profile
            WHERE unique_id = ?;
            """,
            (your_unique_id,),
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
            WHERE your_unique_id = ? AND match_unique_id = ?;
            """,
            (your_unique_id, unique_id),
        )
        accepted_match_data = cursor.fetchall()
        if not accepted_match_data:
            cursor.execute(
                """
                SELECT *
                FROM Accepted_match
                WHERE your_unique_id = ? AND match_unique_id = ?;
                """,
                (unique_id, your_unique_id),
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
