"""
Main module of flask API.
"""
import os
from typing import Any
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS, cross_origin
from asgiref.wsgi import WsgiToAsgi
import google.generativeai as genai
from dotenv import load_dotenv

from helper import (generate_unique_id, analyze_image_video, 
                        hash_password, get_db_connection,
                        save_uploaded_file, get_attractiveness_score)
from user_profile_helper import (extract_profile_data, check_mandatory_fields)
# Module
app = Flask(__name__)
cors = CORS(app)
asgi_app = WsgiToAsgi(app)
api_cors = {
  "origins": ["*"],
  "methods": ["OPTIONS", "GET", "POST"],
  "allow_headers": ["Content-Type"]
}
MEDIA_FOLDER = 'uploads'
def __init__():
    if not os.path.exists(MEDIA_FOLDER):
        os.makedirs(MEDIA_FOLDER)
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key = api_key)

@app.route('/auth', methods=['POST'])
@cross_origin()
def authenticate():
    data = request.json
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Missing email or password'}), 422
    email = data['email']
    password = data['password']
    if not email or not password:
        return make_response(jsonify({"message": "Email and password are required"}), 400)
    hashed_password = hash_password(password)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM User WHERE email = ?', (email,))
    user = cursor.fetchone()
    if user:
        if user[2] == hashed_password:
            conn.close()
            return make_response(jsonify({"message": "Authentication successful!", "unique_id": user[3]}), 200)
        else:
            conn.close()
            return make_response(jsonify({"message": "Invalid password!"}), 401)
    else:
        cursor.execute('INSERT INTO User (email, password) VALUES (?, ?)', (email, hashed_password))
        user_id = cursor.lastrowid
        unique_id = generate_unique_id(user_id)
        cursor.execute('UPDATE User SET unique_id = ? WHERE id = ?', (unique_id, user_id))
        conn.commit()
        conn.close()

        return make_response(jsonify({"message": "User created successfully!", "unique_id": unique_id}), 201)
    
@app.route('/extract_features', methods=['POST'])
def extract_features():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    uploaded_file = request.files['file']
    if uploaded_file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if uploaded_file:
        file_path = save_uploaded_file(uploaded_file, MEDIA_FOLDER)
        analysis_insights = analyze_image_video(file_path)
        if os.path.exists(file_path):
            os.remove(file_path)
        return jsonify(analysis_insights), 200
    return jsonify({"error": "File processing failed."}), 500

@app.route('//attractiveness', methods=['POST'])
def atractiveness():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    uploaded_file = request.files['file']
    if uploaded_file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if uploaded_file:
        file_path = save_uploaded_file(uploaded_file, MEDIA_FOLDER)
        analysis_insights = get_attractiveness_score(file_path)
        if os.path.exists(file_path):
            os.remove(file_path)
        return jsonify(analysis_insights), 200
    return jsonify({"error": "File processing failed."}), 500

@app.route('/get_profile', methods=['GET'])
@cross_origin()
def get_profile():
    data = request.json
    if not data or 'unique_id' not in data:
        return jsonify({'error': 'Missing unique_id'}), 422 
    unique_id = data['unique_id']
    if not unique_id:
        return make_response(jsonify({"message": "unique_id is required"}), 400)  
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM User_Profile WHERE unique_id = ?', (unique_id,))
    profile = cursor.fetchone()
    print("Fetched profile:", profile)
    if not profile:
        conn.close()
        return jsonify({'error': 'Profile not found for the provided unique_id'}), 404
    column_names = [column[0] for column in cursor.description]
    profile_data = dict(zip(column_names, profile)) 
    conn.close()
    return jsonify(profile_data), 200

@app.route('/create_profile', methods=['POST'])
@cross_origin()
def create_or_update_user_profile():
    data = request.json
    mandatory_fields = [
        'unique_id', 'attractiveness', 'relationship_type', 'family_planning',
        'living_address', 'apartment_style', 'roommates', 'working_hours',
        'other_commitments', 'dating_availability', 'height', 'weight', 'age'
    ]
    are_fields_present, missing_fields = check_mandatory_fields(data, mandatory_fields)
    if not are_fields_present:
        return jsonify({'error': f'Missing mandatory fields: {", ".join(missing_fields)}'}), 400
    profile_data = extract_profile_data(data)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM User WHERE unique_id = ?', (profile_data['unique_id'],))
    unique_id = cursor.fetchone()
    if not unique_id:
        conn.close()
        return jsonify({'error': 'unique_id does not exist in User table'}), 400
    cursor.execute('SELECT * FROM User_profile WHERE unique_id = ?', (profile_data['unique_id'],))
    user_profile = cursor.fetchone()
    if user_profile:
        cursor.execute('''UPDATE User_profile SET
            attractiveness = ?,
            relationship_type = ?,
            family_planning = ?,
            living_address = ?,
            apartment_style = ?,
            roommates = ?,
            working_hours = ?,
            other_commitments = ?,
            dating_availability = ?,
            height = ?,
            weight = ?,
            age = ?,
            gender = ?,
            eye_color = ?,
            eye_type = ?,
            hair_color = ?,
            hair_length = ?,
            hair_style = ?,
            nose = ?,
            facial_form = ?,
            cheekbones = ?,
            eyebrows = ?,
            dept = ?,
            assets = ?,
            income_this_year = ?,
            income_next_year = ?,
            income_over_next_year = ?,
            wealth_goals = ?,
            kids = ?,
            pets = ?,
            living = ?,
            wealth_splitting = ?,
            effort_splitting = ?,
            religion = ?,
            politics = ?,
            existing_family_structure = ?,
            retirement = ?,
            q1 = ?,
            q2 = ?,
            q3 = ?,
            q4 = ?,
            q5 = ?,
            q6 = ?,
            q7 = ?,
            q8 = ?,
            q9 = ?,
            q10 = ?
            WHERE unique_id = ?''', (
                profile_data['attractiveness'],
                profile_data['relationship_type'],
                profile_data['family_planning'],
                profile_data['living_address'],
                profile_data['apartment_style'],
                profile_data['roommates'],
                profile_data['working_hours'],
                profile_data['other_commitments'],
                profile_data['dating_availability'],
                profile_data['height'],
                profile_data['weight'],
                profile_data['age'],
                profile_data['gender'],
                profile_data['eye_color'],
                profile_data['eye_type'],
                profile_data['hair_color'],
                profile_data['hair_length'],
                profile_data['hair_style'],
                profile_data['nose'],
                profile_data['facial_form'],
                profile_data['cheekbones'],
                profile_data['eyebrows'],
                profile_data['dept'],
                profile_data['assets'],
                profile_data['income_this_year'],
                profile_data['income_next_year'],
                profile_data['income_over_next_year'],
                profile_data['wealth_goals'],
                profile_data['kids'],
                profile_data['pets'],
                profile_data['living'],
                profile_data['wealth_splitting'],
                profile_data['effort_splitting'],
                profile_data['religion'],
                profile_data['politics'],
                profile_data['existing_family_structure'],
                profile_data['retirement'],
                profile_data['q1'],
                profile_data['q2'],
                profile_data['q3'],
                profile_data['q4'],
                profile_data['q5'],
                profile_data['q6'],
                profile_data['q7'],
                profile_data['q8'],
                profile_data['q9'],
                profile_data['q10'],
                profile_data['unique_id']
            ))
        conn.commit()
        conn.close()
        return jsonify({'message': 'User profile updated successfully', 'profile_id': profile_data['unique_id']}), 200
    else:
        cursor.execute('''INSERT INTO User_profile (unique_id, attractiveness, relationship_type, 
            family_planning, living_address, apartment_style, roommates, working_hours, 
            other_commitments, dating_availability, height, weight, age, gender, eye_color, 
            eye_type, hair_color, hair_length, hair_style, nose, facial_form, cheekbones, 
            eyebrows, dept, assets, income_this_year, income_next_year, income_over_next_year, 
            wealth_goals, kids, pets, living, wealth_splitting, effort_splitting, religion, 
            politics, existing_family_structure, retirement, q1, q2, q3, q4, q5, q6, q7, q8, 
            q9, q10) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
            profile_data['unique_id'],
            profile_data['attractiveness'],
            profile_data['relationship_type'],
            profile_data['family_planning'],
            profile_data['living_address'],
            profile_data['apartment_style'],
            profile_data['roommates'],
            profile_data['working_hours'],
            profile_data['other_commitments'],
            profile_data['dating_availability'],
            profile_data['height'],
            profile_data['weight'],
            profile_data['age'],
            profile_data['gender'],
            profile_data['eye_color'],
            profile_data['eye_type'],
            profile_data['hair_color'],
            profile_data['hair_length'],
            profile_data['hair_style'],
            profile_data['nose'],
            profile_data['facial_form'],
            profile_data['cheekbones'],
            profile_data['eyebrows'],
            profile_data['dept'],
            profile_data['assets'],
            profile_data['income_this_year'],
            profile_data['income_next_year'],
            profile_data['income_over_next_year'],
            profile_data['wealth_goals'],
            profile_data['kids'],
            profile_data['pets'],
            profile_data['living'],
            profile_data['wealth_splitting'],
            profile_data['effort_splitting'],
            profile_data['religion'],
            profile_data['politics'],
            profile_data['existing_family_structure'],
            profile_data['retirement'],
            profile_data['q1'],
            profile_data['q2'],
            profile_data['q3'],
            profile_data['q4'],
            profile_data['q5'],
            profile_data['q6'],
            profile_data['q7'],
            profile_data['q8'],
            profile_data['q9'],
            profile_data['q10']
        ))

        conn.commit()
        conn.close()
        return jsonify({'message': 'User profile created successfully', 'profile_id': profile_data['unique_id']}), 201

@app.route('/delete_user', methods=['DELETE'])
@cross_origin()
def delete_user():
    data = request.json
    if not data or 'email' not in data:
        return jsonify({'error': 'Missing email'}), 422 
    email = data['email']
    if not email:
        return make_response(jsonify({"message": "Email is required"}), 400)    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT unique_id FROM User WHERE email = ?', (email,))
    user = cursor.fetchone()

    if user:
        unique_id = user[0]
        cursor.execute('DELETE FROM User_profile WHERE unique_id = ?', (unique_id,))
        cursor.execute('DELETE FROM User WHERE email = ?', (email,))
        conn.commit()
        conn.close()
        return make_response(jsonify({"message": f"User with email {email} deleted successfully!"}), 200)
    else:
        conn.close()
        return make_response(jsonify({"message": "User not found!"}), 404)
    
    
if __name__ == '__main__':
    __init__()
    app.run(host="0.0.0.0", port=8000)


