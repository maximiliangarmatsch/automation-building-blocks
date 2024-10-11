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
from api_helpers.create_profile.attractivenss_score_helper import (
    get_attractiveness_score,
)
from api_helpers.create_profile.image_analysis_helper import analyze_image_video
from view_match_profile import get_user_and_profile_data
from api_helpers.create_profile.insert_general_questions import (
    insert_user_general_questions,
)
from api_helpers.create_profile.helpers import (
    check_mandatory_fields,
    user_profile_exists,
    calculate_bmi,
)

# Create Match Profile module imports
from api_helpers.match_profile.helpers import (
    filter_profiles_by_distance,
    save_matched_profiles,
    fetch_matching_profiles,
    get_distance,
    get_user_address,
)
from api_helpers.match_profile.extract_user_preferences import extract_user_preferences
from api_helpers.match_profile.build_match_query import build_match_query

# Create auth module imports
from api_helpers.auth.helpers import (
    extract_user_login_data,
    fetch_user_by_email,
    hash_user_password,
    authenticate_user,
)
from api_helpers.auth.create_new_user import create_new_user

# get profile module imports
from api_helpers.get_profile.profile_data import get_user_profile
from match_profile_helper import (
    get_match_profiles,
    get_accepted_profiles,
)

# custom question module imports
from api_helpers.custom_questions.save_custom_question import save_custom_question
from api_helpers.custom_questions.save_custom_answer import save_custom_answer

from helper import get_db_connection, save_uploaded_file, validate_required_fields

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
    user_data, error_message, error_code = extract_user_login_data(data)
    if error_message:
        return jsonify({"error": error_message}), error_code
    email = user_data["email"]
    password = user_data["password"]
    hashed_password = hash_user_password(password)
    conn = get_db_connection()
    user = fetch_user_by_email(conn, email)
    if user:
        auth_response, auth_code = authenticate_user(user, hashed_password)
        conn.close()
        return make_response(jsonify(auth_response), auth_code)
    else:
        unique_id = create_new_user(conn, email, hashed_password)
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
    conn = get_db_connection()
    data = request.json
    if not data or "unique_id" not in data:
        return jsonify({"error": "Missing unique_id"}), 422
    unique_id = data["unique_id"]
    if not unique_id:
        return make_response(jsonify({"message": "unique_id is required"}), 400)
    profile_data = get_user_profile(unique_id, conn)
    if not profile_data:
        return jsonify({"error": "Profile not found for the provided unique_id"}), 404
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
    return jsonify(
        get_user_and_profile_data(your_unique_id, match_unique_id, conn), 200
    )


@app.route("/update_question", methods=["PUT"])
def update_question():
    user_unique_id = request.json["user_unique_id"]
    question_number = request.json["question_number"]
    new_question_text = request.json["new_question_text"]
    question_id = f"{user_unique_id}_gq{question_number}"
    query = """
        UPDATE User_profile_general_questions
        SET question = ?
        WHERE question_id = ? AND user_id = ?
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, (new_question_text, question_id, user_unique_id))
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": "Question updated successfully"})


@app.route("/delete_question", methods=["DELETE"])
def delete_question():
    user_unique_id = request.json["user_unique_id"]
    question_number = request.json["question_number"]
    question_id = f"{user_unique_id}_gq{question_number}"
    query = """
        DELETE FROM User_profile_general_questions
        WHERE question_id = ? AND user_id = ?
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, (question_id, user_unique_id))
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": "Question deleted successfully"})


@app.route("/save_custom_question", methods=["POST"])
def save_specific_question():
    conn = get_db_connection()
    data = request.get_json()
    required_fields = ["to_user_id", "from_user_id", "question"]
    error_response = validate_required_fields(data, required_fields)
    if error_response:
        return error_response
    to_user_id = data["to_user_id"]
    from_user_id = data["from_user_id"]
    question = data["question"]
    response, status = save_custom_question(to_user_id, from_user_id, question, conn)
    return jsonify(response), status


@app.route("/save_custom_answer", methods=["PUT"])
def submit_specific_question_answer():
    conn = get_db_connection()
    data = request.get_json()
    required_fields = ["to_user_id", "from_user_id", "question_id", "answer"]
    error_response = validate_required_fields(data, required_fields)
    if error_response:
        return error_response
    to_user_id = data["to_user_id"]
    from_user_id = data["from_user_id"]
    question_id = data["question_id"]
    answer = data["answer"]
    response, status = save_custom_answer(
        to_user_id, from_user_id, question_id, answer, conn
    )
    return jsonify(response), status


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
    conn = get_db_connection()
    user_preferences = extract_user_preferences(data)
    query, params = build_match_query(user_preferences)
    rows, columns = fetch_matching_profiles(conn, query, params)
    if not rows:
        return jsonify({"profiles": []})
    final_profiles = []
    if user_preferences["max_distance"]:
        user_address = get_user_address(user_preferences["unique_id"], conn)
        final_profiles = filter_profiles_by_distance(
            rows,
            user_address,
            user_preferences["max_distance"],
            columns,
            google_distance_api,
        )
    else:
        final_profiles = [dict(zip(columns, row)) for row in rows]
    save_matched_profiles(user_preferences["unique_id"], final_profiles, conn)
    conn.close()
    return jsonify({"profiles": final_profiles})


@app.route("/apply_filter", methods=["POST"])
def apply_filter():
    data = request.get_json()
    user_preferences = data.get("user_preferences", {})
    attractiveness_min = user_preferences.get("attractiveness_min")
    attractiveness_max = user_preferences.get("attractiveness_max")
    relationship_type = user_preferences.get("relationship_type")
    family_planning = user_preferences.get("family_planning")
    user_gender = user_preferences.get("gender")
    country = user_preferences.get("country")
    city = user_preferences.get("city")
    age_min = user_preferences.get("age_min")
    age_max = user_preferences.get("age_max")
    hair_length = user_preferences.get("hair_length")
    max_distance = user_preferences.get("max_distance")
    unique_id = user_preferences.get("unique_id")
    query = "SELECT * FROM User_profile WHERE 1=1"  # 1=1 allows for easy addition of filters
    params = []
    if attractiveness_min is not None and attractiveness_max is not None:
        query += " AND CAST(attractiveness AS INTEGER) BETWEEN ? AND ?"
        params.extend([attractiveness_min, attractiveness_max])
    if relationship_type:
        query += " AND relationship_type = ?"
        params.append(relationship_type)
    if family_planning:
        query += " AND family_planning = ?"
        params.append(family_planning)
    if country and city:
        query += " AND country = ? AND state = ? AND city = ?"
        params.extend([country, city])
    if age_min is not None and age_max is not None:
        query += " AND age BETWEEN ? AND ?"
        params.extend([age_min, age_max])
    if user_gender:
        query += " AND gender = ?"
        params.append(user_gender)
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
    if max_distance:
        user_address = get_user_address(unique_id, conn)
        columns = [column[0] for column in cursor.description]
        for row in rows:
            profile_dict = {columns[i]: row[i] for i in range(len(columns))}
            profile_address = f"{profile_dict['city']}, {profile_dict['country']}, {profile_dict['zipcode']}"
            distance = get_distance(google_distance_api, user_address, profile_address)
            distance_value = float(distance.split()[0])
            if distance_value <= float(max_distance):
                final_profiles.append(profile_dict)
    else:
        columns = [column[0] for column in cursor.description]
        final_profiles = [dict(zip(columns, row)) for row in rows]
    conn.close()
    return jsonify({"profiles": final_profiles})


@app.route("/create_profile", methods=["POST"])
@cross_origin()
def create_or_update_user_profile():
    data = request.json
    are_fields_present, missing_fields = check_mandatory_fields(data)
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
    bmi = calculate_bmi(profile_data["weight"], profile_data["height"])
    if user_profile_exists(cursor, profile_data["unique_id"]):
        update_user_profile(cursor, profile_data, bmi)
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
        insert_user_profile(cursor, profile_data, bmi)
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
