from flask import jsonify
from api_helpers.create_profile.create_profile import insert_user_profile
from api_helpers.create_profile.update_profile import update_user_profile
from api_helpers.create_profile.insert_general_questions import (
    insert_user_general_questions,
)


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
    cursor.execute(
        """SELECT * 
        FROM User_profile 
        WHERE unique_id = ?""",
        (unique_id,),
    )
    return cursor.fetchone()


def calculate_bmi(weight, height):
    height_meters = height / 100
    bmi = weight / (height_meters**2)
    return int(round(bmi))


def handle_update_profile(conn, profile_data, bmi):
    cursor = conn.cursor()
    update_user_profile(cursor, profile_data, bmi)
    conn.commit()
    conn.close()
    return (
        jsonify(
            {
                "message": "User profile updated successfully",
                "profile_id": profile_data["unique_id"],
            }
        ),
        200,
    )


def handle_create_profile(conn, profile_data, bmi):
    cursor = conn.cursor()
    insert_user_profile(cursor, profile_data, bmi)
    insert_user_general_questions(cursor, profile_data)
    conn.commit()
    conn.close()
    return (
        jsonify(
            {
                "message": "User profile created successfully",
                "profile_id": profile_data["unique_id"],
            }
        ),
        200,
    )
