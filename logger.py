import csv
import os
from datetime import datetime

# Define the log file path
LOG_FILE = "traffic_log.csv"

def init_logger():
    """Creates the CSV file with headers if it does not already exist."""
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Vehicle_ID", "Class", "License_Plate"])

def log_vehicle(vehicle_id, vehicle_class, plate_text="N/A"):
    """Appends a new detection record to the CSV file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, vehicle_id, vehicle_class, plate_text])