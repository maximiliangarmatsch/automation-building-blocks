from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from helper import get_db_connection, validate_required_fields
from api_helpers.custom_questions.save_custom_question import save_customize_question

save_custom_question = Blueprint("save_custom_question", __name__)


@save_custom_question.route("/save_custom_question", methods=["POST"])
@cross_origin()
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
    response, status = save_customize_question(to_user_id, from_user_id, question, conn)
    return jsonify(response), status
