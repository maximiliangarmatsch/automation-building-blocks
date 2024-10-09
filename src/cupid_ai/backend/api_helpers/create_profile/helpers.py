def check_mandatory_fields(data):
    mandatory_fields = [
        "unique_id",
        "attractiveness",
        "relationship_type",
        "family_planning",
        "living_space",
        "working_hours",
        "other_commitments",
        "dating_availability",
        "gender",
        "height",
        "weight",
        "age",
        "city",
        "country",
        "zipcode",
        "occupation",
    ]
    missing_fields = [field for field in mandatory_fields if field not in data]
    return len(missing_fields) == 0, missing_fields


def user_profile_exists(cursor, unique_id):
    cursor.execute("SELECT * FROM User_profile WHERE unique_id = ?", (unique_id,))
    return cursor.fetchone()


def calculate_bmi(weight, height):
    height_meters = height / 100
    bmi = weight / (height_meters**2)
    return int(round(bmi))
