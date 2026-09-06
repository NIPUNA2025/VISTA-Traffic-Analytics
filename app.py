import cv2
import easyocr
from ultralytics import YOLO

# 1. Load YOLOv8 model & EasyOCR reader (English)
print("[INFO] Loading YOLOv8 and EasyOCR models...")
model = YOLO("yolov8n.pt")
reader = easyocr.Reader(["en"], gpu=False)  # Set gpu=True if you have CUDA setup

VEHICLE_CLASSES = [2, 3, 5, 7]  # COCO IDs for cars, bikes, buses, trucks
VIDEO_PATH = "data/traffic.mp4"

cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    print(f"[ERROR] Could not open video file at {VIDEO_PATH}")
    exit()

unique_vehicle_ids = set()
processed_ocr_ids = set()  # Tracks vehicles we've already run OCR on to avoid lag

print("[INFO] Starting pipeline. Press 'q' or close window to exit.")

# Skip frames to optimize OCR speed (OCR on every single frame is slow)
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
        active_in_frame = len(track_ids)

        for box, track_id in zip(boxes, track_ids):
            unique_vehicle_ids.add(track_id)
            x1, y1, x2, y2 = box

            # Run OCR once per vehicle ID every 10 frames to keep playback smooth
            if track_id not in processed_ocr_ids and frame_count % 10 == 0:
                # Crop vehicle region from image matrix
                vehicle_crop = frame[y1:y2, x1:x2]

                if vehicle_crop.size > 0:
                    # Run EasyOCR on cropped region
                    ocr_results = reader.readtext(vehicle_crop, detail=0)

                    if ocr_results:
                        detected_text = " ".join(ocr_results).strip()
                        if len(detected_text) >= 3:  # Filter out noise
                            print(f"[OCR DETECTED] Vehicle ID #{track_id} -> Text: {detected_text}")
                            processed_ocr_ids.add(track_id)

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