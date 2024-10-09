from api_helpers.match_profile.save_match_profile import save_match_profile
import requests


def get_distance(api_key, origin, destination):
    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": origin,
        "destinations": destination,
        "key": api_key,
        "mode": "driving",  # You can use other modes like walking, bicycling, or transit
    }
    response = requests.get(url, params=params)
    data = response.json()
    if response.status_code == 200 and data["status"] == "OK":
        distance = data["rows"][0]["elements"][0]["distance"]["text"]
        duration = data["rows"][0]["elements"][0]["duration"]["text"]
        return distance
    else:
        raise Exception(f"Error in response: {data}")


def filter_profiles_by_distance(
    profiles, user_address, max_distance, columns, google_distance_api
):
    final_profiles = []
    for row in profiles:
        profile_dict = {columns[i]: row[i] for i in range(len(columns))}
        city = profile_dict["city"]
        country = profile_dict["country"]
        zipcode = profile_dict["zipcode"]
        profile_address = f"{city}, {country}, {zipcode}"
        distance = get_distance(google_distance_api, user_address, profile_address)
        distance_value = float(distance.split()[0])
        if distance_value <= float(max_distance):
            final_profiles.append(profile_dict)
    return final_profiles


def save_matched_profiles(unique_id, profiles, conn):
    for profile in profiles:
        save_match_profile(
            your_unique_id=unique_id,
            match_unique_id=profile["unique_id"],
            conn=conn,
        )


def fetch_matching_profiles(conn, query, params):
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    return rows, columns
