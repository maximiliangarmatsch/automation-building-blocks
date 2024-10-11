"""
Main module of flask API.
"""

import os
import json
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
from api_helpers.match_profile.get_match_profile import get_match_profiles
from api_helpers.match_profile.get_match_accepted import get_match_accepted
from api_helpers.match_profile.get_specific_match import get_specific_match
from api_helpers.match_profile.get_specific_match_accepted import (
    get_specific_match_accepted,
)

# Create auth module imports
from api_helpers.auth.helpers import (
    extract_user_login_data,
    fetch_user_by_email,
    hash_user_password,
    authenticate_user,
)
from api_helpers.auth.create_new_user import create_new_user

from helper import (
    get_db_connection,
    save_uploaded_file,
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


@app.route("/get_specific_match", methods=["POST"])
def view_match_profile():
    conn = get_db_connection()
    data = request.get_json()
    from_unique_id = data.get("from_unique_id")
    to_unique_id = data.get("to_unique_id")
    if not from_unique_id or not to_unique_id:
        return (
            jsonify({"error": "Both from_unique_id and to_unique_id are required"}),
            400,
        )
    return jsonify(get_specific_match(from_unique_id, to_unique_id, conn), 200)


@app.route("/get_specific_match_accepted", methods=["POST"])
def specific_match_accepted():
    conn = get_db_connection()
    data = request.get_json()
    from_unique_id = data.get("from_unique_id")
    to_unique_id = data.get("to_unique_id")
    if not from_unique_id or not to_unique_id:
        return (
            jsonify({"error": "Both from_unique_id and to_unique_id are required"}),
            400,
        )
    return jsonify(get_specific_match_accepted(from_unique_id, to_unique_id, conn), 200)


@app.route("/update_question", methods=["PUT"])
def update_question():
    user_unique_id = request.json["unique_id"]
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
    user_unique_id = request.json["unique_id"]
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
    your_unique_id = data.get("from_unique_id")
    match_unique_id = data.get("to_unique_id")
    if not your_unique_id or not match_unique_id:
        return (
            jsonify({"error": "Both from_unique_id and to_unique_id are required"}),
            400,
        )
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            DELETE FROM Match_profile 
            WHERE from_unique_id = ? AND to_unique_id = ?
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


@app.route("/get_match_accepted", methods=["POST"])
def accepted_profiles():
    connection = get_db_connection()
    data = request.get_json()
    unique_id = data.get("unique_id")
    if unique_id is None:
        return jsonify({"error": "unique_id is required"}), 400
    profiles = get_match_accepted(unique_id, connection)
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


@app.route("/accept_match", methods=["POST"])
def add_accepted_match():
    data = request.get_json()
    to_user_id = data.get("to_user_id")
    from_user_id = data.get("from_user_id")
    answer = data.get("answer")
    if not to_user_id or not from_user_id or not answer:
        return jsonify({"error": "Missing required fields"}), 400
    answer_json = json.dumps(answer)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT 1 FROM Accepted_match 
        WHERE to_user_id = ? AND from_user_id = ?;
        """,
        (to_user_id, from_user_id),
    )
    existing_match = cursor.fetchone()
    if existing_match:
        conn.close()
        return jsonify({"error": "Match already exists"}), 200
    cursor.execute(
        """
        INSERT INTO Accepted_match (to_user_id, from_user_id, answer, status)
        VALUES (?, ?, ?, 'No');
        """,
        (to_user_id, from_user_id, answer_json),
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Accepted match added successfully"}), 200


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
            INSERT INTO User_dates (your_unique_id, partner_unique_id, date_selected, time_selected, 
            contact_method, type_of_date, duration)
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
