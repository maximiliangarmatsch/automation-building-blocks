from helper import validate_required_fields


def insert_user_date(
    your_unique_id,
    partner_unique_id,
    date_selected,
    time_selected,
    contact_method,
    type_of_date,
    duration,
    conn,
):
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO User_dates (your_unique_id, partner_unique_id, date_selected, time_selected, 
        contact_method, type_of_date, duration)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            your_unique_id,
            partner_unique_id,
            date_selected,
            time_selected,
            contact_method,
            type_of_date,
            duration,
        ),
    )


def date_exists(your_unique_id, partner_unique_id, conn):
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT COUNT(*) FROM User_dates 
        WHERE your_unique_id = ? AND partner_unique_id = ?
        """,
        (your_unique_id, partner_unique_id),
    )
    exists = cursor.fetchone()[0]
    return exists > 0


def handle_date_schedule(data, conn):
    required_fields = [
        "your_unique_id",
        "partner_unique_id",
        "date_selected",
        "time_selected",
        "contact_method",
        "type_of_date",
        "duration",
    ]

    error_response = validate_required_fields(data, required_fields)
    if error_response:
        return error_response

    your_unique_id = data["your_unique_id"]
    partner_unique_id = data["partner_unique_id"]

    if date_exists(your_unique_id, partner_unique_id, conn):
        return {"message": "Date already scheduled."}, 200

    insert_user_date(
        your_unique_id,
        partner_unique_id,
        data["date_selected"],
        data["time_selected"],
        data["contact_method"],
        data["type_of_date"],
        data["duration"],
        conn,
    )
    conn.close()
    return {"message": "Date added successfully!"}, 200
