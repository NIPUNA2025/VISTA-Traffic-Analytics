import time
from fastapi import FastAPI, HTTPException, Query, BackgroundTasks
from analytics import (
    get_total_vehicle_count,
    get_vehicle_breakdown,
    search_by_license_plate,
    get_vehicles_by_class
)

app = FastAPI(
    title="VISTA Traffic Analytics API",
    description="Backend AI & Data Pipeline Engine for Traffic Telemetry",
    version="1.2"
)

VALID_CLASSES = ["car", "truck", "bus", "motorcycle"]

# Simulated background worker (simulating frame processing pipeline)
def process_video_stream_task(video_path: str):
    print(f"[BACKGROUND TASK STARTED] Processing video feed: {video_path}")
    time.sleep(5)  # Simulates active video processing duration
    print(f"[BACKGROUND TASK COMPLETED] Finished analyzing: {video_path}")

@app.get("/")
def read_root():
    return {"message": "VISTA Engine Active", "version": "1.2"}

@app.get("/api/v1/metrics/total")
def read_total_vehicles():
    total = get_total_vehicle_count()
    return {"status": "success", "total_vehicles": total}

@app.get("/api/v1/metrics/breakdown")
def read_vehicle_breakdown():
    raw_breakdown = get_vehicle_breakdown()
    formatted = {v_type: count for v_type, count in raw_breakdown}
    return {"status": "success", "breakdown": formatted}

@app.get("/api/v1/vehicles/filter")
def filter_by_class(v_class: str = Query(..., description="Vehicle type: Car, Truck, Bus, Motorcycle")):
    if v_class.lower() not in VALID_CLASSES:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid vehicle class '{v_class}'. Allowed values: {VALID_CLASSES}"
        )
    
    results = get_vehicles_by_class(v_class)
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
    return {"status": "success", "class": v_class, "count": len(formatted), "data": formatted}

@app.get("/api/v1/vehicles/search")
def search_plate(plate: str = Query(..., min_length=1, description="License plate query")):
    results = search_by_license_plate(plate)
    if not results:
        raise HTTPException(status_code=404, detail=f"No vehicle records found matching plate '{plate}'")
        
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

@app.post("/api/v1/pipeline/process-stream")
def trigger_pipeline(background_tasks: BackgroundTasks, video_name: str = "traffic.mp4"):
    """Triggers non-blocking background video processing."""
    background_tasks.add_task(process_video_stream_task, f"data/{video_name}")
    return {
        "status": "queued",
        "message": f"Inference job for '{video_name}' queued in background.",
        "target": f"data/{video_name}"
    }