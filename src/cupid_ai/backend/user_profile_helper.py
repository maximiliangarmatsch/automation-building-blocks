def check_mandatory_fields(data, mandatory_fields):
    missing_fields = [field for field in mandatory_fields if field not in data]
    if missing_fields:
        return False, missing_fields
    return True, []


def extract_profile_data(data):
    return {
        'unique_id': data.get('unique_id'),  # Optional for safety, though it should be mandatory
        'attractiveness': data['attractiveness'],
        'relationship_type': data['relationship_type'],
        'family_planning': data['family_planning'],
        'living_address': data['living_address'],
        'apartment_style': data['apartment_style'],
        'roommates': data['roommates'],
        'working_hours': data['working_hours'],
        'other_commitments': data['other_commitments'],
        'dating_availability': data['dating_availability'],
        'height': data['height'],
        'weight': data['weight'],
        'age': data['age'],
        'gender': data.get('gender'),
        'eye_color': data.get('eye_color'),
        'eye_type': data.get('eye_type'),
        'hair_color': data.get('hair_color'),
        'hair_length': data.get('hair_length'),
        'hair_style': data.get('hair_style'),
        'nose': data.get('nose'),
        'facial_form': data.get('facial_form'),
        'cheekbones': data.get('cheekbones'),
        'eyebrows': data.get('eyebrows'),
        'dept': data.get('dept'),
        'assets': data.get('assets'),
        'income_this_year': data.get('income_this_year'),
        'income_next_year': data.get('income_next_year'),
        'income_over_next_year': data.get('income_over_next_year'),
        'wealth_goals': data.get('wealth_goals'),
        'kids': data.get('kids'),
        'pets': data.get('pets'),
        'living': data.get('living'),
        'wealth_splitting': data.get('wealth_splitting'),
        'effort_splitting': data.get('effort_splitting'),
        'religion': data.get('religion'),
        'politics': data.get('politics'),
        'existing_family_structure': data.get('existing_family_structure'),
        'retirement': data.get('retirement'),
        'q1': data.get('q1'),
        'q2': data.get('q2'),
        'q3': data.get('q3'),
        'q4': data.get('q4'),
        'q5': data.get('q5'),
        'q6': data.get('q6'),
        'q7': data.get('q7'),
        'q8': data.get('q8'),
        'q9': data.get('q9'),
        'q10': data.get('q10'),
    }
