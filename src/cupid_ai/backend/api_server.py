"""
Main module of flask API.
"""

import os
from typing import Any
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS, cross_origin
from asgiref.wsgi import WsgiToAsgi
import google.generativeai as genai
from dotenv import load_dotenv

from helper import (
    generate_unique_id,
    analyze_image_video,
    hash_password,
    get_db_connection,
    save_uploaded_file,
    get_attractiveness_score,
)
from user_profile_helper import extract_profile_data, check_mandatory_fields
from distance_calculator_helper import get_distance, get_user_address
from match_profile_helper import (
    save_match_profile,
    get_match_profiles,
    get_accepted_profiles,
)

load_dotenv()
app = Flask(__name__)
cors = CORS(app)
asgi_app = WsgiToAsgi(app)
api_cors = {
    "origins": ["*"],
    "methods": ["OPTIONS", "GET", "POST"],
    "allow_headers": ["Content-Type"],
}
MEDIA_FOLDER = "uploads"


def __init__():
    if not os.path.exists(MEDIA_FOLDER):
        os.makedirs(MEDIA_FOLDER)
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=api_key)


google_distance_api = os.getenv("GOOGLE_DISTANCE_API")


@app.route("/auth", methods=["POST"])
@cross_origin()
def authenticate():
    data = request.json
    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Missing email or password"}), 422
    email = data["email"]
    password = data["password"]
    if not email or not password:
        return make_response(
            jsonify({"message": "Email and password are required"}), 400
        )
    hashed_password = hash_password(password)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM User WHERE email = ?", (email,))
    user = cursor.fetchone()
    if user:
        if user[2] == hashed_password:
            conn.close()
            return make_response(
                jsonify(
                    {"message": "Authentication successful!", "unique_id": user[3]}
                ),
                200,
            )
        else:
            conn.close()
            return make_response(jsonify({"message": "Invalid password!"}), 401)
    else:
        cursor.execute(
            "INSERT INTO User (email, password) VALUES (?, ?)", (email, hashed_password)
        )
        user_id = cursor.lastrowid
        unique_id = generate_unique_id(user_id)
        cursor.execute(
            "UPDATE User SET unique_id = ? WHERE id = ?", (unique_id, user_id)
        )
        conn.commit()
        conn.close()

        return make_response(
            jsonify({"message": "User created successfully!", "unique_id": unique_id}),
            201,
        )


@app.route("/extract_features", methods=["POST"])
def extract_features():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    uploaded_file = request.files["file"]
    if uploaded_file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    if uploaded_file:
        file_path = save_uploaded_file(uploaded_file, MEDIA_FOLDER)
        analysis_insights = analyze_image_video(file_path)
        if os.path.exists(file_path):
            os.remove(file_path)
        return jsonify(analysis_insights), 200
    return jsonify({"error": "File processing failed."}), 500


@app.route("/attractiveness", methods=["POST"])
def atractiveness():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    uploaded_file = request.files["file"]
    if uploaded_file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    if uploaded_file:
        file_path = save_uploaded_file(uploaded_file, MEDIA_FOLDER)
        analysis_insights = get_attractiveness_score(file_path)
        if os.path.exists(file_path):
            os.remove(file_path)
        return jsonify(analysis_insights), 200
    return jsonify({"error": "File processing failed."}), 500


@app.route("/get_profile", methods=["GET"])
@cross_origin()
def get_profile():
    data = request.json
    if not data or "unique_id" not in data:
        return jsonify({"error": "Missing unique_id"}), 422
    unique_id = data["unique_id"]
    if not unique_id:
        return make_response(jsonify({"message": "unique_id is required"}), 400)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM User_Profile WHERE unique_id = ?", (unique_id,))
    profile = cursor.fetchone()
    print("Fetched profile:", profile)
    if not profile:
        conn.close()
        return jsonify({"error": "Profile not found for the provided unique_id"}), 404
    column_names = [column[0] for column in cursor.description]
    profile_data = dict(zip(column_names, profile))
    conn.close()
    return jsonify(profile_data), 200


@app.route("/get_match_profiles", methods=["POST"])
def get_profiles():
    conn = get_db_connection()
    data = request.get_json()
    unique_id = data.get("unique_id")
    if unique_id is None:
        return jsonify({"error": "unique_id is required"}), 400
    profiles = get_match_profiles(unique_id, conn=conn)
    return profiles


@app.route("/get_accepted_profiles", methods=["POST"])
def accepted_profiles():
    connection = get_db_connection()
    data = request.get_json()
    unique_id = data.get("unique_id")
    if unique_id is None:
        return jsonify({"error": "unique_id is required"}), 400
    profiles = get_accepted_profiles(unique_id, connection)
    return profiles


@app.route("/match_profile", methods=["POST"])
def match_profile():
    data = request.get_json()
    user_preferences = data.get("user_preferences", {})
    # Mandatory filters
    attractiveness_min = user_preferences.get("attractiveness_min")
    attractiveness_max = user_preferences.get("attractiveness_max")
    relationship_type = user_preferences.get("relationship_type")
    family_planning = user_preferences.get("family_planning")
    user_gender = user_preferences.get("gender")
    age_min = user_preferences.get("age_min")
    age_max = user_preferences.get("age_max")

    # Optional filters
    hair_length = user_preferences.get("hair_length")
    max_distance = user_preferences.get("max_distance")
    unique_id = user_preferences.get("unique_id")
    query = """
        SELECT * FROM User_profile
        WHERE CAST(attractiveness AS INTEGER) BETWEEN ? AND ?
        AND relationship_type = ?
        AND family_planning = ?
        AND age BETWEEN ? AND ?
    """
    params = [
        attractiveness_min,
        attractiveness_max,
        relationship_type,
        family_planning,
        age_min,
        age_max,
    ]
    if user_gender == "male":
        query += " AND gender = ?"
        params.append("female")
    elif user_gender == "female":
        query += " AND gender = ?"
        params.append("male")
    if hair_length:
        query += " AND hair_length = ?"
        params.append(hair_length)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    if not rows:
        return jsonify({"profiles": []})
    final_profiles = []
    print(rows)
    if max_distance:
        conn = get_db_connection()
        user_address = get_user_address(unique_id, conn)
        columns = [column[0] for column in cursor.description]
        for row in rows:
            profile_dict = {columns[i]: row[i] for i in range(len(columns))}
            profile_address = profile_dict["living_address"]
            distance = get_distance(google_distance_api, user_address, profile_address)
            distance_value = float(distance.split()[0])
            if distance_value <= float(max_distance):
                final_profiles.append(profile_dict)
                save_match_profile(
                    your_unique_id=unique_id,
                    match_unique_id=profile_dict["unique_id"],
                    conn=conn,
                )
        conn.close()
    else:
        columns = [column[0] for column in cursor.description]
        final_profiles = [dict(zip(columns, row)) for row in rows]
        for profile in final_profiles:
            save_match_profile(
                your_unique_id=unique_id,
                match_unique_id=profile["unique_id"],
                conn=conn,
            )
        conn.close()
    return jsonify({"profiles": final_profiles})


@app.route("/create_profile", methods=["POST"])
@cross_origin()
def create_or_update_user_profile():
    data = request.json
    mandatory_fields = [
        "unique_id",
        "attractiveness",
        "relationship_type",
        "family_planning",
        "living_address",
        "apartment_style",
        "roommates",
        "working_hours",
        "other_commitments",
        "dating_availability",
        "height",
        "weight",
        "age",
    ]
    are_fields_present, missing_fields = check_mandatory_fields(data, mandatory_fields)
    if not are_fields_present:
        return (
            jsonify(
                {"error": f'Missing mandatory fields: {", ".join(missing_fields)}'}
            ),
            400,
        )
    profile_data = extract_profile_data(data)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM User WHERE unique_id = ?", (profile_data["unique_id"],)
    )
    unique_id = cursor.fetchone()
    if not unique_id:
        conn.close()
        return jsonify({"error": "unique_id does not exist in User table"}), 400
    cursor.execute(
        "SELECT * FROM User_profile WHERE unique_id = ?", (profile_data["unique_id"],)
    )
    user_profile = cursor.fetchone()
    if user_profile:
        cursor.execute(
            """UPDATE User_profile SET
            attractiveness = ?,
            relationship_type = ?,
            family_planning = ?,
            living_address = ?,
            apartment_style = ?,
            roommates = ?,
            working_hours = ?,
            other_commitments = ?,
            dating_availability = ?,
            height = ?,
            weight = ?,
            age = ?,
            gender = ?,
            eye_color = ?,
            eye_type = ?,
            hair_color = ?,
            hair_length = ?,
            hair_style = ?,
            nose = ?,
            facial_form = ?,
            cheekbones = ?,
            eyebrows = ?,
            dept = ?,
            assets = ?,
            income_this_year = ?,
            income_next_year = ?,
            income_over_next_year = ?,
            wealth_goals = ?,
            kids = ?,
            pets = ?,
            living = ?,
            wealth_splitting = ?,
            effort_splitting = ?,
            religion = ?,
            politics = ?,
            existing_family_structure = ?,
            retirement = ?,
            q1 = ?,
            q2 = ?,
            q3 = ?,
            q4 = ?,
            q5 = ?,
            q6 = ?,
            q7 = ?,
            q8 = ?,
            q9 = ?,
            q10 = ?
            WHERE unique_id = ?""",
            (
                profile_data["attractiveness"],
                profile_data["relationship_type"],
                profile_data["family_planning"],
                profile_data["living_address"],
                profile_data["apartment_style"],
                profile_data["roommates"],
                profile_data["working_hours"],
                profile_data["other_commitments"],
                profile_data["dating_availability"],
                profile_data["height"],
                profile_data["weight"],
                profile_data["age"],
                profile_data["gender"],
                profile_data["eye_color"],
                profile_data["eye_type"],
                profile_data["hair_color"],
                profile_data["hair_length"],
                profile_data["hair_style"],
                profile_data["nose"],
                profile_data["facial_form"],
                profile_data["cheekbones"],
                profile_data["eyebrows"],
                profile_data["dept"],
                profile_data["assets"],
                profile_data["income_this_year"],
                profile_data["income_next_year"],
                profile_data["income_over_next_year"],
                profile_data["wealth_goals"],
                profile_data["kids"],
                profile_data["pets"],
                profile_data["living"],
                profile_data["wealth_splitting"],
                profile_data["effort_splitting"],
                profile_data["religion"],
                profile_data["politics"],
                profile_data["existing_family_structure"],
                profile_data["retirement"],
                profile_data["q1"],
                profile_data["q2"],
                profile_data["q3"],
                profile_data["q4"],
                profile_data["q5"],
                profile_data["q6"],
                profile_data["q7"],
                profile_data["q8"],
                profile_data["q9"],
                profile_data["q10"],
                profile_data["unique_id"],
            ),
        )
        conn.commit()
        conn.close()
        return (
            jsonify(
                {
                    "message": "User profile updated successfully",
                    "profile_id": profile_data["unique_id"],
                }
            ),
            200,
        )
    else:
        cursor.execute(
            """INSERT INTO User_profile (unique_id, attractiveness, relationship_type, 
            family_planning, living_address, apartment_style, roommates, working_hours, 
            other_commitments, dating_availability, height, weight, age, gender, eye_color, 
            eye_type, hair_color, hair_length, hair_style, nose, facial_form, cheekbones, 
            eyebrows, dept, assets, income_this_year, income_next_year, income_over_next_year, 
            wealth_goals, kids, pets, living, wealth_splitting, effort_splitting, religion, 
            politics, existing_family_structure, retirement, q1, q2, q3, q4, q5, q6, q7, q8, 
            q9, q10) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                profile_data["unique_id"],
                profile_data["attractiveness"],
                profile_data["relationship_type"],
                profile_data["family_planning"],
                profile_data["living_address"],
                profile_data["apartment_style"],
                profile_data["roommates"],
                profile_data["working_hours"],
                profile_data["other_commitments"],
                profile_data["dating_availability"],
                profile_data["height"],
                profile_data["weight"],
                profile_data["age"],
                profile_data["gender"],
                profile_data["eye_color"],
                profile_data["eye_type"],
                profile_data["hair_color"],
                profile_data["hair_length"],
                profile_data["hair_style"],
                profile_data["nose"],
                profile_data["facial_form"],
                profile_data["cheekbones"],
                profile_data["eyebrows"],
                profile_data["dept"],
                profile_data["assets"],
                profile_data["income_this_year"],
                profile_data["income_next_year"],
                profile_data["income_over_next_year"],
                profile_data["wealth_goals"],
                profile_data["kids"],
                profile_data["pets"],
                profile_data["living"],
                profile_data["wealth_splitting"],
                profile_data["effort_splitting"],
                profile_data["religion"],
                profile_data["politics"],
                profile_data["existing_family_structure"],
                profile_data["retirement"],
                profile_data["q1"],
                profile_data["q2"],
                profile_data["q3"],
                profile_data["q4"],
                profile_data["q5"],
                profile_data["q6"],
                profile_data["q7"],
                profile_data["q8"],
                profile_data["q9"],
                profile_data["q10"],
            ),
        )

        conn.commit()
        conn.close()
        return (
            jsonify(
                {
                    "message": "User profile created successfully",
                    "profile_id": profile_data["unique_id"],
                }
            ),
            201,
        )


@app.route("/match_accepted", methods=["POST"])
def match_accepted():
    data = request.json
    your_unique_id = data.get("your_unique_id")
    match_partner_unique_id = data.get("match_partner_unique_id")
    status = data.get("status", "No")
    your_q1 = data.get("your_q1")
    your_a1 = data.get("your_a1")
    your_q2 = data.get("your_q2")
    your_a2 = data.get("your_a2")
    your_q3 = data.get("your_q3")
    your_a3 = data.get("your_a3")
    your_q4 = data.get("your_q4")
    your_a4 = data.get("your_a4")
    your_q5 = data.get("your_q5")
    your_a5 = data.get("your_a5")
    your_q6 = data.get("your_q6")
    your_a6 = data.get("your_a6")
    your_q7 = data.get("your_q7")
    your_a7 = data.get("your_a7")
    your_q8 = data.get("your_q8")
    your_a8 = data.get("your_a8")
    your_q9 = data.get("your_q9")
    your_a9 = data.get("your_a9")
    your_q10 = data.get("your_q10")
    your_a10 = data.get("your_a10")

    # Optional fields for partner's questions and answers
    partner_q1 = data.get("partner_q1")
    partner_a1 = data.get("partner_a1")
    partner_q2 = data.get("partner_q2")
    partner_a2 = data.get("partner_a2")
    partner_q3 = data.get("partner_q3")
    partner_a3 = data.get("partner_a3")
    partner_q4 = data.get("partner_q4")
    partner_a4 = data.get("partner_a4")
    partner_q5 = data.get("partner_q5")
    partner_a5 = data.get("partner_a5")
    partner_q6 = data.get("partner_q6")
    partner_a6 = data.get("partner_a6")
    partner_q7 = data.get("partner_q7")
    partner_a7 = data.get("partner_a7")
    partner_q8 = data.get("partner_q8")
    partner_a8 = data.get("partner_a8")
    partner_q9 = data.get("partner_q9")
    partner_a9 = data.get("partner_a9")
    partner_q10 = data.get("partner_q10")
    partner_a10 = data.get("partner_a10")
    if not your_unique_id or not match_partner_unique_id:
        return (
            jsonify(
                {"error": "your_unique_id and match_partner_unique_id are required"}
            ),
            400,
        )

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO Accepted_match (
            your_unique_id, match_unique_id, status,
            your_q1, your_a1, your_q2, your_a2, your_q3, your_a3, your_q4, your_a4, your_q5, your_a5, 
            your_q6, your_a6, your_q7, your_a7, your_q8, your_a8, your_q9, your_a9, your_q10, your_a10,
            partner_q1, partner_a1, partner_q2, partner_a2, partner_q3, partner_a3, partner_q4, partner_a4, 
            partner_q5, partner_a5, partner_q6, partner_a6, partner_q7, partner_a7, partner_q8, partner_a8, 
            partner_q9, partner_a9, partner_q10, partner_a10
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            your_unique_id,
            match_partner_unique_id,
            status,
            your_q1,
            your_a1,
            your_q2,
            your_a2,
            your_q3,
            your_a3,
            your_q4,
            your_a4,
            your_q5,
            your_a5,
            your_q6,
            your_a6,
            your_q7,
            your_a7,
            your_q8,
            your_a8,
            your_q9,
            your_a9,
            your_q10,
            your_a10,
            partner_q1,
            partner_a1,
            partner_q2,
            partner_a2,
            partner_q3,
            partner_a3,
            partner_q4,
            partner_a4,
            partner_q5,
            partner_a5,
            partner_q6,
            partner_a6,
            partner_q7,
            partner_a7,
            partner_q8,
            partner_a8,
            partner_q9,
            partner_a9,
            partner_q10,
            partner_a10,
        ),
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "success"}), 200


@app.route("/delete_user", methods=["DELETE"])
@cross_origin()
def delete_user():
    data = request.json
    if not data or "email" not in data:
        return jsonify({"error": "Missing email"}), 422
    email = data["email"]
    if not email:
        return make_response(jsonify({"message": "Email is required"}), 400)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT unique_id FROM User WHERE email = ?", (email,))
    user = cursor.fetchone()

    if user:
        unique_id = user[0]
        cursor.execute("DELETE FROM User_profile WHERE unique_id = ?", (unique_id,))
        cursor.execute("DELETE FROM User WHERE email = ?", (email,))
        conn.commit()
        conn.close()
        return make_response(
            jsonify({"message": f"User with email {email} deleted successfully!"}), 200
        )
    else:
        conn.close()
        return make_response(jsonify({"message": "User not found!"}), 404)


if __name__ == "__main__":
    __init__()
    app.run(host="0.0.0.0", port=8000)
