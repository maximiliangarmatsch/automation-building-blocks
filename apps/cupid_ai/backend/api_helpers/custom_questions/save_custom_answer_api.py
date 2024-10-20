from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from helper import get_db_connection, validate_required_fields
from api_helpers.custom_questions.save_custom_answer import save_customize_answer

save_custom_answer = Blueprint("save_custom_answer", __name__)


@save_custom_answer.route("/save_custom_answer", methods=["PUT"])
@cross_origin()
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
    response, status = save_customize_answer(
        to_user_id, from_user_id, question_id, answer, conn
    )
    return jsonify(response), status
