import os
import random
import hashlib
import sqlite3
import time
import json
import google.generativeai as genai

DB_PATH = 'db/cupid_ai.db'

def get_prompt() -> str:
    """Make prompt for generating insights."""
    file_path = "./src/cupid_ai/backend/prompts/feature_extraction.txt"
    with open(file_path, "r", encoding="utf8") as file:
        prompt = file.read()
    return prompt

def generate_unique_id(user_id):
    random_number = random.randint(100000, 999999)  # Random 6-digit number
    return f"#{user_id}{random_number}"

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn

def save_uploaded_file(uploaded_file, media_folder):
    file_path = os.path.join(media_folder, uploaded_file.filename)
    with open(file_path, 'wb') as f:
        f.write(uploaded_file.read())
    return file_path

def analyze_image_video(video_path):
    video_file = genai.upload_file(path=video_path)
    while video_file.state.name == "PROCESSING":
        time.sleep(10)
        video_file = genai.get_file(video_file.name)
    if video_file.state.name == "FAILED":
        return {"error": "Video processing failed."}
    prompt = get_prompt()
    model = genai.GenerativeModel('gemini-1.5-flash-latest')    
    response = model.generate_content([prompt, video_file], request_options={"timeout": 600})
    genai.delete_file(video_file.name)
    json_response = response.text.lstrip('```json').rstrip('```')
    data = json.loads(json_response)
    print(data.get('HairColor'))
    return json_response
