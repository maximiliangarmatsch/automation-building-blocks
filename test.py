import sqlite3

# Path to your SQLite database
DB_PATH = 'db/cupid_ai.db'

def create_users_table():
    # Connect to the SQLite database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # SQL command to create the users table
    cursor.execute('SELECT * FROM Match_profile;')
    unique_ids = cursor.fetchall()  # Fetch all results
    print(unique_ids)
    # cursor.execute('''
    #     CREATE TABLE IF NOT EXISTS User (
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         email TEXT NOT NULL UNIQUE,
    #         password TEXT NOT NULL,
    #         unique_id TEXT UNIQUE
    #     );
    # ''')
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
    # cursor.execute('''
    #     CREATE TABLE IF NOT EXISTS Match_profile (
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         your_unique_id INTEGER,
    #         match_unique_id INTEGER,
    #         FOREIGN KEY (your_unique_id) REFERENCES User(unique_id),
    #         FOREIGN KEY (match_unique_id) REFERENCES User(unique_id)
    #     );
    #     ''')
    conn.commit()
    conn.close()
    print("User_profile table created successfully!")

if __name__ == '__main__':
    create_users_table()
