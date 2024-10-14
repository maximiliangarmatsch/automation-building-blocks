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
from api_helpers.create_profile.attractivenss_score_helper import (
    get_attractiveness_score,
)
from api_helpers.create_profile.image_analysis_helper import analyze_image_video
from api_helpers.create_profile.helpers import (
    check_mandatory_fields,
    user_profile_exists,
    calculate_bmi,
    handle_create_profile,
    handle_update_profile,
)

# Create Match Profile module imports
from api_helpers.match_profile.helpers import (
    filter_profiles_by_distance,
    save_matched_profiles,
    fetch_matching_profiles,
    get_user_address,
)
from api_helpers.match_profile.extract_user_preferences import extract_user_preferences
from api_helpers.match_profile.build_match_query import build_match_query
from api_helpers.match_profile.get_match_profile import get_match_profiles
from api_helpers.match_profile.get_specific_match import get_specific_match

# accept match module imports
from api_helpers.match_accept.accept_match import (
    insert_accepted_match,
    check_existing_match,
)
from api_helpers.match_accept.get_match_accepted import get_match_accepted
from api_helpers.match_profile.reject_match import delete_match_from_db
from api_helpers.match_accept.get_specific_match_accepted import (
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

# get profile module imports
from api_helpers.get_profile.profile_data import get_user_profile

# custom question module imports
from api_helpers.custom_questions.save_custom_question import save_custom_question
from api_helpers.custom_questions.save_custom_answer import save_custom_answer

# date scheduling module imports
from api_helpers.date_scheduling.get_schedule_date import handle_get_schedule_date
from api_helpers.date_scheduling.schedule_date import handle_date_schedule
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


@app.route("/reject_match", methods=["DELETE"])
def reject_profile():
    data = request.json
    conn = get_db_connection()
    error_response = validate_required_fields(data, ["from_unique_id", "to_unique_id"])
    if error_response:
        return error_response
    try:
        rows_deleted = delete_match_from_db(data, conn)
        if rows_deleted == 0:
            return (
                jsonify({"status": "success", "message": "No matching profile found"}),
                404,
            )
        return (
            jsonify({"status": "success", "message": "Match rejected succesfully"}),
            200,
        )
    except Exception as e:
        return error_response(str(e), 500)


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
        return handle_update_profile(conn, profile_data, bmi)
    else:
        return handle_create_profile(conn, profile_data, bmi)


@app.route("/accept_match", methods=["POST"])
def add_accepted_match():
    data = request.get_json()
    error_response = validate_required_fields(
        data, ["to_user_id", "from_user_id", "answer"]
    )
    if error_response:
        return error_response
    conn = get_db_connection()
    if check_existing_match(conn, data):
        conn.close()
        return jsonify({"error": "Match already exists"}), 200
    insert_accepted_match(conn, data)
    conn.close()
    return jsonify({"message": "Accepted match added successfully"}), 200


@app.route("/schedule_date", methods=["POST"])
def add_user_date():
    conn = get_db_connection()
    data = request.get_json()
    response, status_code = handle_date_schedule(data, conn)
    return jsonify(response), status_code


@app.route("/get_schedule_date", methods=["POST"])
def get_schedule_date():
    conn = get_db_connection()
    data = request.get_json()
    unique_id = data.get("unique_id")
    if not unique_id:
        return jsonify({"error": "'unique_id' is required."}), 400
    response, status_code = handle_get_schedule_date(unique_id, conn)
    return jsonify(response), status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
