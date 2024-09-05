# Globant Data Project API - App Directory

This directory contains the core components of the Globant Data Project API, developed as part of the Globant Data Engineering Coding Challenge.

## Contents

1. [main.py](#mainpy)
2. [database.py](#databasepy)
3. [models.py](#modelspy)
4. [Setup and Running](#setup-and-running)

## main.py

This file is the heart of the FastAPI application. It defines the API endpoints and implements the business logic for data processing and report generation.

Key features:
- CSV file upload endpoint
- Batch data insertion endpoint
- Employees hired by quarter report
- Departments hired above mean report
- Custom OpenAPI schema for improved documentation

## database.py

This file handles the database connection and session management using SQLAlchemy.

Key components:
- Database URL construction from config
- SQLAlchemy engine and session creation
- Database session dependency for FastAPI

## models.py

This file defines the Pydantic models used for data validation and serialization.

Models included:
- Department
- Job
- HiredEmployee
- EmployeeHiredByQuarter (for report output)
- DepartmentHiredAboveMean (for report output)
- BatchInsertRequest (for batch data insertion)

## Setup and Running

To set up and run the application locally on Ubuntu:

1. Ensure you have Python 3.10+ installed:

``` bash
python3 --version
```
2. Install required packages:

``` bash
pip install -r requirements.tx
```
3. Set up your PostgreSQL database and update the `config.yaml` file in the project root with your database credentials.

4. From the project root directory, run:
``` bash
uvicorn app.main:app --reload
```
5. The API will be available at `http://localhost:8000`. You can access the Swagger UI documentation at `http://localhost:8000/docs`.

For more detailed setup instructions, including database setup and Docker deployment, please refer to the main project README.

## Testing

To test the API endpoints, you can use the Swagger UI or tools like `curl` or Postman. Example `curl` commands for each endpoint are provided in the main project README.

For unit testing, we recommend using `pytest`. Test files should be placed in a `tests` directory at the project root level.

## Note

This API is designed to handle CSV file uploads, perform batch insertions, and generate specific reports as per the Globant Data Engineering Coding Challenge requirements. Ensure all data manipulations and report generations align with the specifications provided in the challenge document.