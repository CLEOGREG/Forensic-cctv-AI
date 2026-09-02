import sqlite3
from pathlib import Path


# =========================================
# DATABASE PATH
# =========================================

BASE_DIR = Path(__file__).resolve().parent

DATABASE_DIR = BASE_DIR / "database"

DATABASE_FILE = DATABASE_DIR / "forensiciq.db"


# =========================================
# DATABASE CONNECTION
# =========================================

def get_connection():

    DATABASE_DIR.mkdir(exist_ok=True)

    connection = sqlite3.connect(
        DATABASE_FILE
    )

    connection.row_factory = sqlite3.Row

    return connection


# =========================================
# DATABASE INITIALIZATION
# =========================================

def init_database():

    connection = get_connection()

    cursor = connection.cursor()


    # =====================================
    # USERS
    # =====================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT NOT NULL UNIQUE,

            password_hash TEXT NOT NULL,

            role TEXT DEFAULT 'VIEWER',

            created_at DATETIME
                DEFAULT CURRENT_TIMESTAMP
        )
    """)


    # =====================================
    # CAMERAS
    # =====================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cameras (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            camera_code TEXT NOT NULL UNIQUE,

            camera_name TEXT NOT NULL,

            ip_address TEXT NOT NULL,

            rtsp_url TEXT,

            location TEXT,

            status TEXT DEFAULT 'OFFLINE',

            resolution TEXT,

            fps INTEGER,

            created_at DATETIME
                DEFAULT CURRENT_TIMESTAMP
        )
    """)


    # =====================================
    # DETECTIONS
    # =====================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS detections (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            subject_id TEXT NOT NULL,

            camera_id INTEGER,

            confidence REAL,

            detection_type TEXT,

            timestamp DATETIME
                DEFAULT CURRENT_TIMESTAMP,

            video_path TEXT,

            FOREIGN KEY (camera_id)
                REFERENCES cameras(id)
        )
    """)


    # =====================================
    # INTERACTIONS
    # =====================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interactions (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            subject_a TEXT NOT NULL,

            subject_b TEXT NOT NULL,

            camera_id INTEGER,

            distance REAL,

            interaction_type TEXT,

            start_time DATETIME,

            end_time DATETIME,

            FOREIGN KEY (camera_id)
                REFERENCES cameras(id)
        )
    """)


    # =====================================
    # SYSTEM NODES
    # =====================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_nodes (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            node_name TEXT NOT NULL,

            node_type TEXT NOT NULL,

            ip_address TEXT,

            status TEXT DEFAULT 'OFFLINE',

            last_seen DATETIME,

            created_at DATETIME
                DEFAULT CURRENT_TIMESTAMP
        )
    """)


    connection.commit()

    connection.close()


# =========================================
# RUN DIRECTLY
# =========================================

if __name__ == "__main__":

    init_database()

    print("ForensicIQ database initialized.")

    print(f"Database: {DATABASE_FILE}")