import sqlite3


DATABASE = "database.db"


def create_database():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    # ==========================================
    # USERS TABLE
    # ==========================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            email TEXT UNIQUE NOT NULL,

            phone TEXT,

            password TEXT NOT NULL

        )
    """)

    # ==========================================
    # SCANS TABLE
    # ==========================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scans(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            image_name TEXT NOT NULL,

            prediction TEXT NOT NULL,

            confidence REAL NOT NULL,

            raw_prediction REAL NOT NULL,

            risk_level TEXT NOT NULL,

            scan_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id) REFERENCES users(id)

        )
    """)

    conn.commit()

    conn.close()

    print("Database Created Successfully!")


if __name__ == "__main__":

    create_database()