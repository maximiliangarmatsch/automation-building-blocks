import sqlite3

# Path to your SQLite database
DB_PATH = "db/cupid_ai.db"


def create_users_table():
    # Connect to the SQLite database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # SQL command to create the users table
    cursor.execute("SELECT * FROM Match_profile;")
    unique_ids = cursor.fetchall()  # Fetch all results
    print(unique_ids)
    # cursor.execute(
    #     """
    #     CREATE TABLE IF NOT EXISTS User (
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         email TEXT NOT NULL UNIQUE,
    #         password TEXT NOT NULL,
    #         unique_id TEXT UNIQUE
    #     );
    # """
    # )
    # cursor.execute('DROP TABLE IF EXISTS User;')
    # Commit and close connection
    # cursor.execute("""
    #     CREATE TABLE User_profile (
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         unique_id TEXT,
    #         attractiveness TEXT NOT NULL,
    #         relationship_type TEXT NOT NULL,
    #         family_planning TEXT NOT NULL,
    #         living_address TEXT NOT NULL,
    #         apartment_style TEXT NOT NULL,
    #         roommates INTEGER NOT NULL,
    #         working_hours TEXT NOT NULL,
    #         other_commitments TEXT NOT NULL,
    #         dating_availability TEXT NOT NULL,
    #         gender TEXT,
    #         height REAL NOT NULL,
    #         weight REAL NOT NULL,
    #         age INTEGER NOT NULL,
    #         eye_color TEXT,
    #         eye_type TEXT,
    #         hair_color TEXT,
    #         hair_length TEXT,
    #         hair_style TEXT,
    #         nose TEXT,
    #         facial_form TEXT,
    #         cheekbones TEXT,
    #         eyebrows TEXT,
    #         dept TEXT,
    #         assets TEXT,
    #         income_this_year REAL,
    #         income_next_year REAL,
    #         income_over_next_year REAL,
    #         wealth_goals TEXT,
    #         kids TEXT,
    #         pets TEXT,
    #         living TEXT,
    #         wealth_splitting TEXT,
    #         effort_splitting TEXT,
    #         religion TEXT,
    #         politics TEXT,
    #         existing_family_structure TEXT,
    #         retirement TEXT,
    #         q1 TEXT,
    #         q2 TEXT,
    #         q3 TEXT,
    #         q4 TEXT,
    #         q5 TEXT,
    #         q6 TEXT,
    #         q7 TEXT,
    #         q8 TEXT,
    #         q9 TEXT,
    #         q10 TEXT,
    #         FOREIGN KEY (unique_id) REFERENCES User(unique_id)
    #     );
    #     """)
    # cursor.execute(
    #     """
    #     CREATE TABLE IF NOT EXISTS Match_profile (
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         your_unique_id INTEGER,
    #         match_unique_id INTEGER,
    #         FOREIGN KEY (your_unique_id) REFERENCES User(unique_id),
    #         FOREIGN KEY (match_unique_id) REFERENCES User(unique_id)
    #     );
    #     """
    # )
    # cursor.execute(
    #     """
    #     CREATE TABLE IF NOT EXISTS Accepted_match (
    #     id INTEGER PRIMARY KEY AUTOINCREMENT,
    #     to_user_id TEXT NOT NULL,
    #     from_user_id TEXT NOT NULL,
    #     answer JSON NOT NULL,
    #     status TEXT NOT NULL,
    #     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    #     FOREIGN KEY (from_user_id) REFERENCES User(unique_id),
    #     FOREIGN KEY (to_user_id) REFERENCES User(unique_id)
    #     );
    # """
    # )
    # cursor.execute(
    #     """
    #     DELETE FROM User_profile;
    #     """
    # )
    # cursor.execute(
    #     """
    #     CREATE TABLE IF NOT EXISTS User_dates (
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         your_unique_id INTEGER,
    #         partner_unique_id INTEGER,
    #         date_selected DATE NOT NULL,
    #         time_selected TIME NOT NULL,
    #         contact_method TEXT NOT NULL,
    #         type_of_date TEXT NOT NULL,
    #         duration INTEGER NOT NULL CHECK (duration BETWEEN 5 AND 120),
    #         created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    #         FOREIGN KEY (your_unique_id) REFERENCES User(unique_id),
    #         FOREIGN KEY (partner_unique_id) REFERENCES User(unique_id)
    #     );
    # """
    # )
    # cursor.execute(
    #     """
    #     CREATE TABLE User_profile (
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         unique_id TEXT,
    #         attractiveness TEXT NOT NULL,
    #         relationship_type TEXT NOT NULL,
    #         family_planning TEXT NOT NULL,
    #         apartment_style TEXT NOT NULL,
    #         roommates INTEGER,
    #         working_hours TEXT NOT NULL,
    #         other_commitments TEXT NOT NULL,
    #         dating_availability TEXT NOT NULL,
    #         gender TEXT NOT NULL,
    #         height REAL NOT NULL,
    #         weight REAL NOT NULL,
    #         age INTEGER NOT NULL,
    #         city TEXT NOT NULL,
    #         country TEXT NOT NULL,
    #         zipcode TEXT NOT NULL,
    #         occupation TEXT NOT NULL,
    #         languages TEXT,
    #         bmi INTEGER,
    #         eye_color TEXT,
    #         eye_type TEXT,
    #         hair_color TEXT,
    #         hair_length TEXT,
    #         hair_style TEXT,
    #         nose TEXT,
    #         facial_form TEXT,
    #         cheekbones TEXT,
    #         eyebrows TEXT,
    #         dept TEXT,
    #         assets TEXT,
    #         income_this_year REAL,
    #         income_next_year REAL,
    #         income_over_next_year REAL,
    #         wealth_goals TEXT,
    #         kids TEXT,
    #         pets TEXT,
    #         living TEXT,
    #         wealth_splitting TEXT,
    #         effort_splitting TEXT,
    #         religion TEXT,
    #         politics TEXT,
    #         existing_family_structure TEXT,
    #         retirement TEXT,
    #         smoking TEXT,
    #         drinking TEXT,
    #         drugs TEXT,
    #         first_sex TEXT,
    #         virgin TEXT,
    #         bodycount INTEGER,
    #         FOREIGN KEY (unique_id) REFERENCES User(unique_id)
    #     );
    # """
    # )
    # cursor.execute(
    #     """
    #     DROP TABLE IF EXISTS User_Match_Questions;
    #     """
    # )
    # Get all user-created table names, excluding system tables
    # cursor.execute(
    #     "SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence';"
    # )
    # tables = cursor.fetchall()

    # # Drop each table
    # for table in tables:
    #     cursor.execute(f"DROP TABLE IF EXISTS {table[0]};")
    # cursor.execute(
    #     """
    #     CREATE TABLE User_profile_general_questions (
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         user_id TEXT NOT NULL,
    #         question_id TEXT NOT NULL,
    #         question TEXT NOT NULL,
    #         FOREIGN KEY (user_id) REFERENCES User(unique_id)
    #     );
    #     """
    # )
    # cursor.execute(
    #     """
    # DELETE FROM User_profile
    # WHERE unique_id = ?;
    # """,
    #     ("#2100403",),
    # )
    # cursor.execute(
    #     """
    # SELECT city, country, zipcode FROM User_profile WHERE unique_id = ?
    # """,
    #     ("#2100403",),
    # )
    # cursor.execute(
    #     """
    # DELETE FROM User_Match_Questions;
    # """
    # )
    # cursor.execute(
    #     """
    #     CREATE TABLE User_profile (
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         unique_id TEXT,
    #         attractiveness TEXT NOT NULL,
    #         relationship_type TEXT NOT NULL,
    #         family_planning TEXT NOT NULL,
    #         working_hours TEXT NOT NULL,
    #         other_commitments TEXT NOT NULL,
    #         dating_availability TEXT NOT NULL,
    #         gender TEXT NOT NULL,
    #         height REAL NOT NULL,
    #         weight REAL NOT NULL,
    #         age INTEGER NOT NULL,
    #         city TEXT NOT NULL,
    #         country TEXT NOT NULL,
    #         zipcode TEXT NOT NULL,
    #         occupation TEXT NOT NULL,
    #         languages TEXT,
    #         bmi INTEGER,
    #         eye_color TEXT,
    #         eye_type TEXT,
    #         hair_color TEXT,
    #         hair_length TEXT,
    #         hair_style TEXT,
    #         nose TEXT,
    #         facial_form TEXT,
    #         cheekbones TEXT,
    #         eyebrows TEXT,
    #         body_shape TEXT,
    #         sports TEXT,
    #         hobbies TEXT,
    #         overall_health TEXT,
    #         skin_helath TEXT,
    #         kids TEXT,
    #         pets TEXT,
    #         living_space TEXT NOT NULL,
    #         living_mates TEXT,
    #         wealth_splitting TEXT,
    #         effort_splitting TEXT,
    #         religion TEXT,
    #         politics TEXT,
    #         existing_family_structure TEXT,
    #         retirement TEXT,
    #         smoking TEXT,
    #         drinking TEXT,
    #         drugs TEXT,
    #         financial_situation TEXT,
    #         dating_experince TEXT,
    #         taruma TEXT,
    #         legal_status TEXT,
    #         FOREIGN KEY (unique_id) REFERENCES User(unique_id)
    #     );
    # """
    # )
    # query = """
    # CREATE TABLE IF NOT EXISTS User_Match_Questions (
    #     id INTEGER PRIMARY KEY AUTOINCREMENT,
    #     question_id TEXT NOT NULL,
    #     to_user_id TEXT NOT NULL,
    #     from_user_id TEXT NOT NULL,
    #     question TEXT NOT NULL,
    #     answer TEXT NULL,
    #     rating BOOLEAN NULL,
    #     FOREIGN KEY (to_user_id) REFERENCES User(user_id),
    #     FOREIGN KEY (from_user_id) REFERENCES User(user_id)
    # );
    # """
    # cursor.execute(query)
    conn.commit()
    # result = cursor.fetchone()
    conn.close()
    print("User_profile table created successfully!")
    # return result[0], result[1], result[2]


if __name__ == "__main__":
    create_users_table()
