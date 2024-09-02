# routes/form.py

from flask import Blueprint, request, jsonify

bp = Blueprint('form', __name__)

@bp.route('/submit_form', methods=['POST'])
def submit_form():
    data = request.get_json()
    # Process the form data here (e.g., save to database)
    return jsonify({'message': 'Form submitted successfully', 'data': data})