import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_total_metrics():
    response = client.get("/api/v1/metrics/total")
    assert response.status_code == 200
    assert "total_vehicles" in response.json()

def test_read_metrics_breakdown():
    response = client.get("/api/v1/metrics/breakdown")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_filter_vehicles_valid():
    response = client.get("/api/v1/vehicles/filter?v_class=car")
    assert response.status_code == 200
    res_json = response.json()
    assert isinstance(res_json, dict)
    assert "data" in res_json
    assert isinstance(res_json["data"], list)

def test_search_plate_not_found():
    response = client.get("/api/v1/vehicles/search?plate=XYZ")
    assert response.status_code == 404