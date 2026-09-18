# VISTA: Vision-Based Intelligent Traffic Analytics Engine

A production-ready Data Engineering and Computer Vision microservice pipeline designed to ingest traffic video streams, extract real-time vehicle telemetry and license plates using YOLOv8 and EasyOCR, persist logs into SQLite, and expose microservice REST endpoints via FastAPI.

---

## Technical Highlights
- **Computer Vision Pipeline:** Real-time object detection (YOLOv8) and Optical Character Recognition (EasyOCR).
- **Data Engineering & Persistence:** Structured SQLite schema with optimized query filters for classification and license plate lookups.
- **Asynchronous REST API:** FastAPI service with background workers (`BackgroundTasks`) for non-blocking stream processing.
- **Automated Testing Engine:** Integration unit tests built using `pytest` and FastAPI `TestClient`.
- **CI/CD Pipeline:** GitHub Actions workflow executing automated testing pipelines on every `main` push.
- **Container Orchestration:** Containerized environment using `Dockerfile` and `docker-compose`.

---

## Tech Stack
- **Languages & Frameworks:** Python 3.10, FastAPI, Uvicorn
- **AI & Vision:** Ultralytics YOLOv8, EasyOCR, OpenCV
- **Database:** SQLite3
- **DevOps & Testing:** Docker, Docker Compose, GitHub Actions, Pytest, Git

---

## API Quickstart

### 1. Local Setup & Testing
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest test_main.py
uvicorn main:app --reload