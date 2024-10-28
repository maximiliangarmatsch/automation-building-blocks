import os
from flask import jsonify
import sqlite3
import google.generativeai as genai

# DB_PATH = "apps/cupid_ai/db/cupid_ai.db"
DB_PATH = "cupid_ai.db"

def make_prompt(file_path) -> str:
    file_path = file_path
    with open(file_path, "r", encoding="utf8") as file:
        prompt = file.read()
    return prompt


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn


def save_uploaded_file(uploaded_file, media_folder):
    file_path = os.path.join(media_folder, uploaded_file.filename)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())
    return file_path


def validate_required_fields(data, required_fields):
    for field in required_fields:
        if field not in data or data[field] is None:
            return jsonify({"error": f"'{field}' is required."}), 400
    return None
