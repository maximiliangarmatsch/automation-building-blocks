import requests
def get_distance(api_key, origin, destination):
    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": origin,
        "destinations": destination,
        "key": api_key,
        "mode": "driving"  # You can use other modes like walking, bicycling, or transit
    }
    response = requests.get(url, params=params)
    data = response.json()
    print(data)
    if response.status_code == 200 and data['status'] == "OK":
        distance = data['rows'][0]['elements'][0]['distance']['text']
        duration = data['rows'][0]['elements'][0]['duration']['text']
        return distance
    else:
        raise Exception(f"Error in response: {data}")
    
def get_user_address(unique_id, conn):
    cursor = conn.cursor()
    query = "SELECT living_address FROM User_profile WHERE unique_id = ?"
    cursor.execute(query, (unique_id,))
    result = cursor.fetchone()
    return result[0]