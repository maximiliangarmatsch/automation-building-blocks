def get_schedules_by_id(unique_id, column, conn):
    cursor = conn.cursor()
    cursor.execute(
        f"""
        SELECT partner_unique_id, date_selected, time_selected, contact_method, type_of_date, duration
        FROM User_dates
        WHERE {column} = ?
        """,
        (unique_id,),
    )
    schedules = cursor.fetchall()
    return schedules


def handle_get_schedule_date(unique_id, conn):
    schedules = get_schedules_by_id(unique_id, "your_unique_id", conn)
    if not schedules:
        schedules = get_schedules_by_id(unique_id, "partner_unique_id", conn)
    if not schedules:
        return {"message": "No scheduling data found for the provided unique ID."}, 404

    schedule_list = [
        {
            "partner_unique_id": schedule[0],
            "date_selected": schedule[1],
            "time_selected": schedule[2],
            "contact_method": schedule[3],
            "type_of_date": schedule[4],
            "duration": schedule[5],
        }
        for schedule in schedules
    ]
    conn.close()
    return schedule_list, 200
