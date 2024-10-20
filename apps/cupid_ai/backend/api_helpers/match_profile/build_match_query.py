def build_match_query(user_preferences):
    query = """
        SELECT * FROM User_profile
        WHERE CAST(attractiveness AS INTEGER) BETWEEN ? AND ?
        AND relationship_type = ?
        AND family_planning = ?
        AND country =?
        AND age BETWEEN ? AND ?
    """
    params = [
        user_preferences["attractiveness_min"],
        user_preferences["attractiveness_max"],
        user_preferences["relationship_type"],
        user_preferences["family_planning"],
        user_preferences["country"],
        user_preferences["age_min"],
        user_preferences["age_max"],
    ]
    if user_preferences["gender"]:
        query += " AND gender = ?"
        params.append(user_preferences["gender"])
    if user_preferences["hair_length"]:
        query += " AND hair_length = ?"
        params.append(user_preferences["hair_length"])
    return query, params
