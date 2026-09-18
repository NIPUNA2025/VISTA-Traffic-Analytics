# VISTA: Vision-Based Intelligent Traffic Analytics Engine

A production-ready Data Engineering and Computer Vision pipeline designed to ingest traffic video streams, extract real-time vehicle telemetry and license plates using YOLOv8 and EasyOCR, persist logs into SQLite, and expose microservice REST endpoints via FastAPI.

## Architectural Highlights
- Computer Vision Pipeline: Real-time object detection (YOLOv8) and Optical Character Recognition (EasyOCR).
- Data Persistence: Automated relational schema management in SQLite with index-optimized SQL queries.
- RESTful API Service: FastAPI microservice with OpenAPI/Swagger documentation, query filtering, and HTTP exception handling.
- Asynchronous Processing: Non-blocking background task processing for heavy inference workflows using FastAPI BackgroundTasks.
- Containerized Deployment: Packaged with Docker for consistent multi-platform deployments.

## Tech Stack
- Languages & Frameworks: Python 3.10, FastAPI, Uvicorn
- AI & Computer Vision: Ultralytics YOLOv8, EasyOCR, OpenCV
- Database: SQLite3
- DevOps & Tooling: Docker, Git

## API Quickstart

### 1. Run via Local Virtual Environment
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload

Access the interactive documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

### 2. Run via Docker
docker build -t vista-traffic-engine .
docker run -p 8000:8000 vista-traffic-engine

## Endpoints Summary
- GET /api/v1/metrics/total - Returns aggregate vehicle count.
- GET /api/v1/metrics/breakdown - Returns vehicle classification breakdown.
- GET /api/v1/vehicles/filter?v_class=car - Filters detections strictly by vehicle class.
- GET /api/v1/vehicles/search?plate=XYZ - Searches detections by license plate substring.
- POST /api/v1/pipeline/process-stream - Queues an asynchronous video inference job.