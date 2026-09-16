from fastapi import FastAPI
from analytics import get_total_vehicle_count, get_vehicle_breakdown, search_by_license_plate

app = FastAPI(title="VISTA Traffic Analytics API", version="1.0")

@app.get("/")
def read_root():
    return {"message": "Welcome to VISTA Traffic Engine API"}

@app.get("/api/v1/metrics/total")
def read_total_vehicles():
    total = get_total_vehicle_count()
    return {"status": "success", "total_vehicles": total}

@app.get("/api/v1/metrics/breakdown")
def read_vehicle_breakdown():
    raw_breakdown = get_vehicle_breakdown()
    # Convert tuple output to a clean JSON object dictionary
    formatted = {v_type: count for v_type, count in raw_breakdown}
    return {"status": "success", "breakdown": formatted}

@app.get("/api/v1/vehicles/search")
def search_plate(plate: str):
    results = search_by_license_plate(plate)
    formatted = [
        {
            "id": row[0],
            "timestamp": row[1],
            "vehicle_id": row[2],
            "vehicle_class": row[3],
            "license_plate": row[4]
        }
        for row in results
    ]
    return {"status": "success", "query": plate, "matches": formatted}