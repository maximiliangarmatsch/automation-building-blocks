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

# Create Profile module imports
from api_helpers.create_profile.extract_profile_data import extract_profile_data
from api_helpers.create_profile.create_profile import insert_user_profile
from api_helpers.create_profile.update_profile import update_user_profile
from view_match_profile import get_user_and_profile_data
from api_helpers.create_profile.insert_general_questions import (
    insert_user_general_questions,
)
from api_helpers.create_profile.helpers import (
    check_mandatory_fields,
    user_profile_exists,
)

from helper import (
    generate_unique_id,
    analyze_image_video,
    hash_password,
    get_db_connection,
    save_uploaded_file,
    get_attractiveness_score,
)
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

if not os.path.exists(MEDIA_FOLDER):
    os.makedirs(MEDIA_FOLDER)
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


@app.route("/get_profile", methods=["POST"])
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


@app.route("/view_match_profile", methods=["POST"])
def view_match_profile():
    conn = get_db_connection()
    data = request.get_json()
    your_unique_id = data.get("your_unique_id")
    match_unique_id = data.get("match_unique_id")
    if not your_unique_id or not match_unique_id:
        return (
            jsonify({"error": "Both your_unique_id and match_unique_id are required"}),
            400,
        )
    # profiles = get_match_profiles(unique_id, conn=conn)

    return jsonify(
        get_user_and_profile_data(your_unique_id, match_unique_id, conn), 200
    )


@app.route("/update_question", methods=["PUT"])
def update_question():
    user_unique_id = request.json["user_unique_id"]
    question_number = request.json["question_number"]
    new_question_text = request.json["new_question_text"]
    query = f"UPDATE User_profile_general_questions SET g_q{question_number} = ? WHERE user_id = (SELECT unique_id FROM User WHERE unique_id = ?)"
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, (new_question_text, user_unique_id))
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": "Question updated successfully"})


@app.route("/delete_question", methods=["DELETE"])
def delete_question():
    user_unique_id = request.json["user_unique_id"]
    question_number = request.json["question_number"]
    query = f"UPDATE User_profile_general_questions SET g_q{question_number} = NULL WHERE user_id = (SELECT unique_id FROM User WHERE unique_id = ?)"
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, (user_unique_id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": "Question deleted successfully"})


@app.route("/reject_profile", methods=["DELETE"])
def reject_profile():
    data = request.json
    your_unique_id = data.get("your_unique_id")
    match_unique_id = data.get("match_unique_id")
    if not your_unique_id or not match_unique_id:
        return (
            jsonify({"error": "Both your_unique_id and match_unique_id are required"}),
            400,
        )
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            DELETE FROM Match_profile 
            WHERE your_unique_id = ? AND match_unique_id = ?
        """,
            (your_unique_id, match_unique_id),
        )
        conn.commit()
        conn.close()
        if cursor.rowcount == 0:
            return jsonify({"message": "No matching profile found"}), 404
        else:
            return jsonify({"message": "Profile rejected successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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
            city = profile_dict["city"]
            country = profile_dict["country"]
            zipcode = profile_dict["zipcode"]
            profile_address = f"{city}, {country}, {zipcode}"
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
        "apartment_style",
        "roommates",
        "working_hours",
        "other_commitments",
        "dating_availability",
        "gender",
        "height",
        "weight",
        "age",
        "city",
        "country",
        "zipcode",
        "occupation",
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
    if user_profile_exists(cursor, profile_data["unique_id"]):
        update_user_profile(cursor, profile_data)
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
        insert_user_profile(cursor, profile_data)
        insert_user_general_questions(cursor, profile_data)
        conn.commit()
        conn.close()
        return (
            jsonify(
                {
                    "message": "User profile created successfully",
                    "profile_id": profile_data["unique_id"],
                }
            ),
            200,
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
        SELECT 1 FROM Accepted_match 
        WHERE your_unique_id = ? AND match_unique_id = ?
        """,
        (your_unique_id, match_partner_unique_id),
    )
    existing_match = cursor.fetchone()

    if existing_match:
        conn.close()
        return jsonify({"message": "already exists"}), 200
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


@app.route("/schedule_date", methods=["POST"])
def add_user_date():
    data = request.get_json()
    required_fields = [
        "your_unique_id",
        "partner_unique_id",
        "date_selected",
        "time_selected",
        "contact_method",
        "type_of_date",
        "duration",
    ]
    for field in required_fields:
        if field not in data or data[field] is None:
            return jsonify({"error": f"'{field}' is required."}), 400

    your_unique_id = data["your_unique_id"]
    partner_unique_id = data["partner_unique_id"]
    date_selected = data["date_selected"]
    time_selected = data["time_selected"]
    contact_method = data["contact_method"]
    type_of_date = data["type_of_date"]
    duration = data["duration"]
    try:
        if not (5 <= int(duration) <= 120):
            return (
                jsonify({"error": "Duration must be between 5 and 120 minutes."}),
                400,
            )
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT COUNT(*) FROM User_dates 
            WHERE your_unique_id = ? AND partner_unique_id = ?
            """,
            (your_unique_id, partner_unique_id),
        )
        exists = cursor.fetchone()[0]
        if exists > 0:
            return jsonify({"message": "Date already scheduled."}), 200
        cursor.execute(
            """
            INSERT INTO User_dates (your_unique_id, partner_unique_id, date_selected, time_selected, contact_method, type_of_date, duration)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                your_unique_id,
                partner_unique_id,
                date_selected,
                time_selected,
                contact_method,
                type_of_date,
                duration,
            ),
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "Date added successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/get_schedule_date", methods=["POST"])
def get_schedule_date():
    data = request.get_json()
    unique_id = data.get("unique_id")
    if not unique_id:
        return jsonify({"error": "'unique_id' is required."}), 400
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT partner_unique_id, date_selected, time_selected, contact_method, type_of_date, duration
            FROM User_dates
            WHERE your_unique_id = ?
            """,
            (unique_id,),
        )
        schedules = cursor.fetchall()
        if not schedules:
            cursor.execute(
                """
                SELECT your_unique_id, date_selected, time_selected, contact_method, type_of_date, duration
                FROM User_dates
                WHERE partner_unique_id = ?
                """,
                (unique_id,),
            )
            schedules = cursor.fetchall()
        if not schedules:
            return (
                jsonify(
                    {"message": "No scheduling data found for the provided unique ID."}
                ),
                404,
            )
        schedule_list = []
        for schedule in schedules:
            schedule_list.append(
                {
                    "partner_unique_id": schedule[0],
                    "date_selected": schedule[1],
                    "time_selected": schedule[2],
                    "contact_method": schedule[3],
                    "type_of_date": schedule[4],
                    "duration": schedule[5],
                }
            )
        conn.close()
        return jsonify(schedule_list), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


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
    app.run(host="0.0.0.0", port=8000)
