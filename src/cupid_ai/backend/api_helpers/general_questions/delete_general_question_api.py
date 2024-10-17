import json
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from helper import get_db_connection
from api_helpers.date_scheduling.get_schedule_date import handle_get_schedule_date


delete_general_question = Blueprint("delete_general_question", __name__)


@delete_general_question.route("/delete_general_question", methods=["DELETE"])
@cross_origin()
def delete_question():
    user_id = request.json["user_id"]
    question_id = request.json["question_id"]
    conn = get_db_connection()
    cursor = conn.cursor()
    delete_question_query = """
        DELETE FROM User_profile_general_questions
        WHERE question_id = ? AND user_id = ?
    """
    cursor.execute(delete_question_query, (question_id, user_id))
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
            del answers_dict["match_general_questions_answer"][question_id]
        elif question_id in answers_dict["user_general_questions_answer"]:
            del answers_dict["user_general_questions_answer"][question_id]
        update_answer_query = """
            UPDATE Accepted_match
            SET answer = ?
            WHERE id = ?
        """
        cursor.execute(update_answer_query, (json.dumps(answers_dict), match_id))
    conn.commit()
    cursor.close()
    conn.close()
    return (
        jsonify({"message": "Question and related answers deleted successfully."}),
        200,
    )
