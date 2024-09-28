import sqlite3
from flask import jsonify
def save_match_profile(your_unique_id, match_unique_id, conn):
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO Match_profile (your_unique_id, match_unique_id)
            VALUES (?, ?);
        ''', (your_unique_id, match_unique_id))
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return jsonify({'success': False, 'message': str(e)})
    finally:
        conn.close()
    return jsonify({'success': True, 'message': 'Match profile saved successfully.'})



def get_match_profiles(unique_id, conn):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT match_unique_id FROM match_profile
        WHERE your_unique_id = ?;
    ''', (unique_id,))
    match_ids = cursor.fetchall()
    match_unique_ids = [match_id[0] for match_id in match_ids]
    print(match_ids)
    if match_unique_ids:
        placeholders = ', '.join(['?'] * len(match_unique_ids))  # Create placeholders for the SQL query
        cursor.execute(f'''
            SELECT * FROM User_profile
            WHERE unique_id IN ({placeholders});
        ''', match_unique_ids)
        matched_profiles = cursor.fetchall()
    conn.close()
    if not matched_profiles:
        return jsonify({'profiles': []})
    columns = [column[0] for column in cursor.description]
    profiles = [dict(zip(columns, row)) for row in matched_profiles]
    return jsonify({'profiles': profiles})
