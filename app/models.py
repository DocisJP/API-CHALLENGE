from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from pydantic import BaseModel

# SQLAlchemy ORM models
class DepartmentORM(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True)
    department = Column(String, nullable=False)

class JobORM(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True)
    job = Column(String, nullable=False)

class HiredEmployeeORM(Base):
    __tablename__ = 'hired_employees'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    datetime = Column(String, nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id'))
    job_id = Column(Integer, ForeignKey('jobs.id'))

# Pydantic models for API
class DepartmentBase(BaseModel):
    id: int
    department: str

class Department(DepartmentBase):
    class Config:
        from_attributes = True

class JobBase(BaseModel):
    id: int
    job: str

class Job(JobBase):
    class Config:
        from_attributes = True

class HiredEmployeeBase(BaseModel):
    id: int
    name: str
    datetime: str
    department_id: int
    job_id: int

class HiredEmployee(HiredEmployeeBase):
    class Config:
        from_attributes = True

class EmployeeHiredByQuarter(BaseModel):
    department: str
    job: str
    Q1: int
    Q2: int
    Q3: int
    Q4: int

class DepartmentHiredAboveMean(BaseModel):
    id: int
    department: str
    hired: int

class BatchInsertRequest(BaseModel):
    table_name: str
    data: list[dict]