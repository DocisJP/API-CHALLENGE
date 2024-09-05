from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class DepartmentBase(BaseModel):
    """Base model for Department data."""
    id: int
    department: str

class Department(DepartmentBase):
    """Pydantic model for Department, used for ORM mode."""
    class Config:
        orm_mode = True

class JobBase(BaseModel):
    """Base model for Job data."""
    id: int
    job: str

class Job(JobBase):
    """Pydantic model for Job, used for ORM mode."""
    class Config:
        orm_mode = True

class HiredEmployeeBase(BaseModel):
    """Base model for HiredEmployee data."""
    id: int
    name: str
    datetime: datetime
    department_id: Optional[int] = None
    job_id: Optional[int] = None

class HiredEmployee(HiredEmployeeBase):
    """Pydantic model for HiredEmployee, used for ORM mode."""
    class Config:
        orm_mode = True

class EmployeeHiredByQuarter(BaseModel):
    """Model for representing employee hiring data by quarter."""
    department: str
    job: str
    Q1: int
    Q2: int
    Q3: int
    Q4: int

class DepartmentHiredAboveMean(BaseModel):
    """Model for representing departments that hired above the mean."""
    id: int
    department: str
    hired: int

class BatchInsertRequest(BaseModel):
    """Model for batch insert request data."""
    table_name: str
    data: list[dict]