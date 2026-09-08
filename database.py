import sqlite3
from datetime import datetime

DB_NAME = "traffic_analytics.db"

def init_db():
    """Creates the SQLite database and the logs table if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Create structured logs table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS traffic_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            vehicle_id INTEGER NOT NULL,
            vehicle_class TEXT NOT NULL,
            license_plate TEXT DEFAULT 'N/A'
        )
    """)
    
    conn.commit()
    conn.close()

def log_vehicle_to_db(vehicle_id, vehicle_class, plate_text="N/A"):
    """Inserts a single vehicle detection record into the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute("""
        INSERT INTO traffic_logs (timestamp, vehicle_id, vehicle_class, license_plate)
        VALUES (?, ?, ?, ?)
    """, (timestamp, vehicle_id, vehicle_class, plate_text))
    
    conn.commit()
    conn.close()