# Function to update an existing user profile
def update_user_profile(cursor, profile_data):
    cursor.execute(
        """
        UPDATE User_profile SET
            attractiveness = ?, relationship_type = ?, family_planning = ?, living_address = ?, apartment_style = ?, roommates = ?,
            working_hours = ?, other_commitments = ?, dating_availability = ?, gender = ?, height = ?, weight = ?, age = ?, city = ?,
            country = ?, zipcode = ?, occupation = ?, languages = ?, bmi = ?, eye_color = ?, eye_type = ?, hair_color = ?, hair_length = ?,
            hair_style = ?, nose = ?, facial_form = ?, cheekbones = ?, eyebrows = ?, dept = ?, assets = ?, income_this_year = ?, income_next_year = ?,
            income_over_next_year = ?, wealth_goals = ?, kids = ?, pets = ?, living = ?, wealth_splitting = ?, effort_splitting = ?, religion = ?,
            politics = ?, existing_family_structure = ?, retirement = ?, smoking = ?, drinking = ?, drugs = ?, first_sex = ?, virgin = ?, bodycount = ?
        WHERE unique_id = ?
        """,
        (
            profile_data["attractiveness"],
            profile_data["relationship_type"],
            profile_data["family_planning"],
            profile_data["living_address"],
            profile_data["apartment_style"],
            profile_data["roommates"],
            profile_data["working_hours"],
            profile_data["other_commitments"],
            profile_data["dating_availability"],
            profile_data["gender"],
            profile_data["height"],
            profile_data["weight"],
            profile_data["age"],
            profile_data["city"],
            profile_data["country"],
            profile_data["zipcode"],
            profile_data["occupation"],
            profile_data["languages"],
            profile_data["bmi"],
            profile_data["eye_color"],
            profile_data["eye_type"],
            profile_data["hair_color"],
            profile_data["hair_length"],
            profile_data["hair_style"],
            profile_data["nose"],
            profile_data["facial_form"],
            profile_data["cheekbones"],
            profile_data["eyebrows"],
            profile_data["dept"],
            profile_data["assets"],
            profile_data["income_this_year"],
            profile_data["income_next_year"],
            profile_data["income_over_next_year"],
            profile_data["wealth_goals"],
            profile_data["kids"],
            profile_data["pets"],
            profile_data["living"],
            profile_data["wealth_splitting"],
            profile_data["effort_splitting"],
            profile_data["religion"],
            profile_data["politics"],
            profile_data["existing_family_structure"],
            profile_data["retirement"],
            profile_data["smoking"],
            profile_data["drinking"],
            profile_data["drugs"],
            profile_data["first_sex"],
            profile_data["virgin"],
            profile_data["bodycount"],
            profile_data["unique_id"],
        ),
    )
