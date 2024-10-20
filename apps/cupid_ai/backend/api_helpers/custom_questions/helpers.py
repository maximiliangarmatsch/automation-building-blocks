def get_next_question_id(to_user_id, from_user_id, conn):
    cursor = conn.cursor()
    query = """
    SELECT COUNT(*) as question_count
    FROM User_Match_Questions
    WHERE to_user_id = ? AND from_user_id = ?
    """
    cursor.execute(query, (to_user_id, from_user_id))
    result = cursor.fetchone()
    if result:
        index = result[0] + 1
    else:
        index = 1
    question_id = f"{from_user_id}_{to_user_id}_gq{index}"
    return question_id
