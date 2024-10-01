def check_mandatory_fields(data, mandatory_fields):
    missing_fields = [field for field in mandatory_fields if field not in data]
    return len(missing_fields) == 0, missing_fields


def user_profile_exists(cursor, unique_id):
    cursor.execute("SELECT * FROM User_profile WHERE unique_id = ?", (unique_id,))
    return cursor.fetchone()
