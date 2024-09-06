from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, BackgroundTasks
from fastapi.openapi.utils import get_openapi
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
import pandas as pd
import io
from typing import List
from .database import get_db
from . import models
from etl.process import etl_process

app = FastAPI(
    title="Globant Data Project API",
    description="API for managing employee data and generating hiring reports",
    version="1.0.0",
)

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url='/docs')

@app.post("/batch_insert/", summary="Batch insert data")
async def batch_insert(request: models.BatchInsertRequest, db: Session = Depends(get_db)):
    """
    Insert multiple rows of data in a single request.

    - **table_name**: Name of the table to insert data into
    - **data**: List of dictionaries, each representing a row of data
    
    Returns a message confirming the number of rows inserted.
    """
    if len(request.data) > 1000:
        raise HTTPException(status_code=400, detail="Maximum 1000 rows allowed per request")
    
    df = pd.DataFrame(request.data)
    
    try:
        df.to_sql(request.table_name, db.bind, if_exists='append', index=False)
        return {"message": f"{len(request.data)} rows inserted successfully into {request.table_name}"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/employees_hired_by_quarter/", response_model=List[models.EmployeeHiredByQuarter], summary="Employees hired by quarter")
async def employees_hired_by_quarter(db: Session = Depends(get_db)):
    """
    Get the number of employees hired for each job and department in 2021, divided by quarter.

    Returns a list of objects containing:
    - **department**: Department name
    - **job**: Job title
    - **Q1**: Number of employees hired in Q1
    - **Q2**: Number of employees hired in Q2
    - **Q3**: Number of employees hired in Q3
    - **Q4**: Number of employees hired in Q4
    """
    query = """
    SELECT 
        d.department,
        j.job,
        COUNT(CASE WHEN EXTRACT(QUARTER FROM he.datetime) = 1 THEN 1 END) as "Q1",
        COUNT(CASE WHEN EXTRACT(QUARTER FROM he.datetime) = 2 THEN 1 END) as "Q2",
        COUNT(CASE WHEN EXTRACT(QUARTER FROM he.datetime) = 3 THEN 1 END) as "Q3",
        COUNT(CASE WHEN EXTRACT(QUARTER FROM he.datetime) = 4 THEN 1 END) as "Q4"
    FROM 
        hired_employees he
    JOIN 
        departments d ON he.department_id = d.id
    JOIN 
        jobs j ON he.job_id = j.id
    WHERE 
        EXTRACT(YEAR FROM he.datetime) = 2021
    GROUP BY 
        d.department, j.job
    ORDER BY 
        d.department, j.job

    """
    
    try:
        result = db.execute(text(query)).mappings()
        return [models.EmployeeHiredByQuarter(**row) for row in result]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/departments_hired_above_mean/", response_model=List[models.DepartmentHiredAboveMean], summary="Departments hired above mean")
async def departments_hired_above_mean(db: Session = Depends(get_db)):
    """
    Get the list of departments that hired more employees than the mean in 2021.

    Returns a list of objects containing:
    - **id**: Department ID
    - **department**: Department name
    - **hired**: Number of employees hired
    
    The list is ordered by the number of employees hired in descending order.
    """
    query = """
    WITH department_hires AS (
        SELECT 
            d.id,
            d.department,
            COUNT(*) as hired
        FROM 
            hired_employees he
        JOIN 
            departments d ON he.department_id = d.id
        WHERE 
            EXTRACT(YEAR FROM he.datetime) = 2021
        GROUP BY 
            d.id, d.department
    ),
    mean_hires AS (
        SELECT AVG(hired) as mean_hired
        FROM department_hires
    )
    SELECT 
        dh.id,
        dh.department,
        dh.hired
    FROM 
        department_hires dh, mean_hires
    WHERE 
        dh.hired > mean_hires.mean_hired
    ORDER BY 
        dh.hired DESC
    """
    
    try:
        result = db.execute(text(query)).mappings()
        return [models.DepartmentHiredAboveMean(**row) for row in result]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

def custom_openapi():
    """
    Customize the OpenAPI schema for the application.

    Returns:
        dict: The custom OpenAPI schema
    """
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Globant Data Project API",
        version="1.0.0",
        description="API for managing employee data and generating hiring reports",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.post("/run_etl/", summary="Run ETL process")
async def run_etl(background_tasks: BackgroundTasks):
    """
    Trigger the ETL process to run in the background.

    Returns a message confirming that the ETL process has been started.
    """
    background_tasks.add_task(etl_process)
    return {"message": "ETL process started in the background"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)