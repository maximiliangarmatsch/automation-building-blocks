def extract_user_preferences(data):
    user_preferences = data.get("user_preferences", {})
    return {
        "attractiveness_min": user_preferences.get("attractiveness_min"),
        "attractiveness_max": user_preferences.get("attractiveness_max"),
        "relationship_type": user_preferences.get("relationship_type"),
        "family_planning": user_preferences.get("family_planning"),
        "gender": user_preferences.get("gender"),
        "country": user_preferences.get("country"),
        "age_min": user_preferences.get("age_min"),
        "age_max": user_preferences.get("age_max"),
        "hair_length": user_preferences.get("hair_length"),
        "max_distance": user_preferences.get("max_distance"),
        "unique_id": user_preferences.get("unique_id"),
    }
