import sqlite3

DB_NAME = "traffic_analytics.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def get_total_vehicle_count():
    """Returns the total number of vehicles logged."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM traffic_logs")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_vehicle_breakdown():
    """Returns total count grouped by vehicle class (Car, Truck, Bus, etc.)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT vehicle_class, COUNT(*) 
        FROM traffic_logs 
        GROUP BY vehicle_class
    """)
    breakdown = cursor.fetchall()
    conn.close()
    return breakdown

def search_by_license_plate(plate_query):
    """Searches for records containing a specific license plate substring."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, timestamp, vehicle_id, vehicle_class, license_plate 
        FROM traffic_logs 
        WHERE license_plate LIKE ?
    """, (f"%{plate_query}%",))
    records = cursor.fetchall()
    conn.close()
    return records

if __name__ == "__main__":
    print("=== VISTA TRAFFIC ANALYTICS REPORT ===")
    print(f"Total Logged Detections: {get_total_vehicle_count()}")
    print("\nVehicle Class Breakdown:")
    for v_type, count in get_vehicle_breakdown():
        print(f" - {v_type}: {count}")