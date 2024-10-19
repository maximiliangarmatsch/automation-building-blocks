import os
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from dotenv import load_dotenv
from api_helpers.match_profile.helpers import (
    filter_profiles_by_distance,
    save_matched_profiles,
    fetch_matching_profiles,
    get_user_address,
)
from api_helpers.match_profile.extract_user_preferences import extract_user_preferences
from api_helpers.match_profile.build_match_query import build_match_query
from helper import get_db_connection

load_dotenv()
google_distance_api = os.getenv("GOOGLE_DISTANCE_API")

MEDIA_FOLDER = "uploads"
match_profile = Blueprint("match_profile", __name__)


@match_profile.route("/match_profile", methods=["POST"])
@cross_origin()
def match_profile_method():
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
