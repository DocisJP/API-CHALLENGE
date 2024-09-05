from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, MetaData
from etl.config import DB_PARAMS
from etl.utils import create_db_engine
from etl.logger import logger
from etl.config import NULL_DATE_PLACEHOLDER

def create_tables(engine):
    logger.info("Creating tables")
    metadata = MetaData()

    departments = Table('departments', metadata,
        Column('id', Integer, primary_key=True),
        Column('department', String(100), nullable=False)
    )

    jobs = Table('jobs', metadata,
        Column('id', Integer, primary_key=True),
        Column('job', String(100), nullable=False)
    )

    hired_employees = Table('hired_employees', metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String(100), nullable=False),
        Column('datetime', DateTime, nullable=False, default=NULL_DATE_PLACEHOLDER),
        Column('department_id', Integer, ForeignKey('departments.id')),
        Column('job_id', Integer, ForeignKey('jobs.id'))
    )

    metadata.create_all(engine)
    logger.info("Tables created successfully")

def drop_tables(engine):
    logger.info("Dropping all existing tables")
    metadata = MetaData()
    metadata.reflect(bind=engine)
    metadata.drop_all(engine)
    logger.info("All tables dropped successfully")

def load_process():
    logger.info("Starting load process")
    engine = create_db_engine(DB_PARAMS)
    try:
        drop_tables(engine)
        create_tables(engine)
        logger.info("Load process completed successfully")
    except Exception as e:
        logger.error(f"Load process failed: {str(e)}", exc_info=True)
        raise