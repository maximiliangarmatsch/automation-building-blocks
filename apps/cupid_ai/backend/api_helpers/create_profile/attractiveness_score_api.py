import os
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin

# Extract features module imports
from api_helpers.create_profile.attractivenss_score_helper import (
    get_attractiveness_score,
)
from helper import save_uploaded_file

MEDIA_FOLDER = "uploads"
attractiveness_score = Blueprint("attractiveness_score", __name__)


@attractiveness_score.route("/attractiveness_score", methods=["POST"])
@cross_origin()
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
