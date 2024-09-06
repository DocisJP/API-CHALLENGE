from app.models import Department, Job, HiredEmployee, DepartmentORM, JobORM, HiredEmployeeORM
from datetime import datetime

def test_batch_insert(test_client, test_session):
    response = test_client.post(
        "/batch_insert/",
        json={
            "table_name": "departments",
            "data": [
                {"id": 1000, "department": "Test Department"}
            ]
        }
    )
    assert response.status_code == 200
    assert "rows inserted successfully" in response.json()["message"]

    # Verify the data was inserted
    department = test_session.query(DepartmentORM).filter_by(id=1000).first()
    assert department is not None
    assert department.department == "Test Department"

def test_run_etl(test_client):
    response = test_client.post("/run_etl/")
    assert response.status_code == 200
    assert "ETL process started" in response.json()["message"]