import json
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from helper import get_db_connection
from api_helpers.date_scheduling.get_schedule_date import handle_get_schedule_date


update_general_question = Blueprint("update_general_question", __name__)


@update_general_question.route("/update_general_question", methods=["POST"])
@cross_origin()
def update_question():
    user_id = request.json["user_id"]
    question_id = request.json["question_id"]
    new_question_text = request.json["new_question_text"]
    conn = get_db_connection()
    cursor = conn.cursor()
    update_question_query = """
        UPDATE User_profile_general_questions
        SET question = ?
        WHERE question_id = ? AND user_id = ?
    """
    cursor.execute(update_question_query, (new_question_text, question_id, user_id))
    select_match_query = """
        SELECT id, answer FROM Accepted_match
        WHERE from_user_id = ?
    """
    cursor.execute(select_match_query, (user_id,))
    accepted_matches = cursor.fetchall()
    for match in accepted_matches:
        match_id = match[0]
        answers_json = match[1]
        answers_dict = json.loads(answers_json)
        if question_id in answers_dict["match_general_questions_answer"]:
            answers_dict["match_general_questions_answer"][question_id] = ""
        elif question_id in answers_dict["user_general_questions_answer"]:
            answers_dict["user_general_questions_answer"][question_id] = ""
        update_answer_query = """
            UPDATE Accepted_match
            SET answer = ?
            WHERE id = ?
        """
        cursor.execute(update_answer_query, (json.dumps(answers_dict), match_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Question and answer updated successfully."}), 200
