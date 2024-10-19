import os
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin

# Extract features module imports
from api_helpers.create_profile.image_analysis_helper import analyze_image_video
from helper import save_uploaded_file

MEDIA_FOLDER = "uploads"
extract_features = Blueprint("extract_features", __name__)


@extract_features.route("/extract_features", methods=["POST"])
@cross_origin()
def extract_feature():
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
