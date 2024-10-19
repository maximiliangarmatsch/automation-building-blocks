def delete_match_from_db(data, conn):
    from_unique_id = data.get("from_unique_id")
    to_unique_id = data.get("to_unique_id")
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            DELETE 
            FROM Match_profile 
            WHERE your_unique_id = ? AND match_unique_id = ?
            """,
            (from_unique_id, to_unique_id),
        )
        conn.commit()
        rows_deleted = cursor.rowcount
        conn.close()
        return rows_deleted
    except Exception as e:
        raise e
