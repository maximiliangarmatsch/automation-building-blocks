import os
import sqlite3
import google.generativeai as genai

DB_PATH = "db/cupid_ai.db"


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
