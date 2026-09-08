import cv2
import easyocr
from ultralytics import YOLO
from database import init_db, log_vehicle_to_db

# Initialize SQLite database on startup
init_db()

# 1. Load YOLOv8 model & EasyOCR reader (English)
print("[INFO] Loading YOLOv8 and EasyOCR models...")
model = YOLO("yolov8n.pt")
reader = easyocr.Reader(["en"], gpu=False)  # Set gpu=True if you have CUDA setup

# COCO IDs mapping: 2=car, 3=motorcycle, 5=bus, 7=truck
CLASS_NAMES = {2: "Car", 3: "Motorcycle", 5: "Bus", 7: "Truck"}
VEHICLE_CLASSES = list(CLASS_NAMES.keys())
VIDEO_PATH = "data/traffic.mp4"

cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    print(f"[ERROR] Could not open video file at {VIDEO_PATH}")
    exit()

unique_vehicle_ids = set()
logged_vehicle_ids = set()  # Set to track vehicles logged to DB
processed_ocr_ids = set()   # Tracks vehicles we've already run OCR on to avoid lag

print("[INFO] Starting pipeline. Press 'q' or close window to exit.")

# Skip frames to optimize OCR speed
frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("[INFO] End of video stream.")
        break

    frame_count += 1

    # Track vehicles frame-by-frame
    results = model.track(frame, persist=True, classes=VEHICLE_CLASSES, verbose=False)

    active_in_frame = 0

    if results[0].boxes is not None and results[0].boxes.id is not None:
        boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
        track_ids = results[0].boxes.id.cpu().numpy().astype(int)
        class_ids = results[0].boxes.cls.cpu().numpy().astype(int)
        active_in_frame = len(track_ids)

        for box, track_id, class_id in zip(boxes, track_ids, class_ids):
            unique_vehicle_ids.add(track_id)
            x1, y1, x2, y2 = box
            vehicle_type = CLASS_NAMES.get(class_id, "Vehicle")
            detected_text = "N/A"

            # Run OCR once per vehicle ID every 10 frames to keep playback smooth
            if track_id not in processed_ocr_ids and frame_count % 10 == 0:
                # Crop vehicle region from image matrix
                vehicle_crop = frame[y1:y2, x1:x2]

                if vehicle_crop.size > 0:
                    # Run EasyOCR on cropped region
                    ocr_results = reader.readtext(vehicle_crop, detail=0)

                    if ocr_results:
                        text_candidate = " ".join(ocr_results).strip()
                        if len(text_candidate) >= 3:  # Filter out noise
                            detected_text = text_candidate
                            print(f"[OCR DETECTED] Vehicle ID #{track_id} -> Text: {detected_text}")
                            processed_ocr_ids.add(track_id)

            # LOGGING LOGIC: Properly indented inside the vehicle loop
            if track_id not in logged_vehicle_ids:
                log_vehicle_to_db(vehicle_id=track_id, vehicle_class=vehicle_type, plate_text=detected_text)
                logged_vehicle_ids.add(track_id)

    # Render bounding boxes and overlay on screen
    annotated_frame = results[0].plot()

    # Draw Analytics Dashboard
    cv2.rectangle(annotated_frame, (10, 10), (330, 85), (0, 0, 0), -1)
    cv2.putText(
        annotated_frame,
        f"Active Vehicles: {active_in_frame}",
        (20, 38),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (0, 255, 255),
        2,
    )
    cv2.putText(
        annotated_frame,
        f"Total Unique Vehicles: {len(unique_vehicle_ids)}",
        (20, 68),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (0, 255, 0),
        2,
    )

    cv2.imshow("AI Traffic Analytics Engine - Milestone 1", annotated_frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q") or cv2.getWindowProperty("AI Traffic Analytics Engine - Milestone 1", cv2.WND_PROP_VISIBLE) < 1:
        break

cap.release()
cv2.destroyAllWindows()
print(f"[SUMMARY] Total Unique Vehicles Processed: {len(unique_vehicle_ids)}")