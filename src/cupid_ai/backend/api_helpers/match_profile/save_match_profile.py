import sqlite3
from flask import jsonify


def save_match_profile(your_unique_id, match_unique_id, conn):
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT 1 
            FROM Match_profile
            WHERE (your_unique_id = ? AND match_unique_id = ?);
            """,
            (your_unique_id, match_unique_id),
        )
        result = cursor.fetchone()
        if result:
            return jsonify(
                {"success": False, "message": "This match profile already exists."}
            )
        cursor.execute(
            """
            INSERT INTO Match_profile (your_unique_id, match_unique_id)
            VALUES (?, ?);
            """,
            (your_unique_id, match_unique_id),
        )
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return jsonify({"success": False, "message": str(e)})
    return jsonify({"success": True, "message": "Match profile saved successfully."})
