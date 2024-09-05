import pandas as pd
from etl.logger import logger
from etl.date_validation import validate_and_standardize_datetimes
from etl.config import NULL_DATE_PLACEHOLDER

def handle_null_values(df, table_name):
    logger.info(f"Handling null values for {table_name}")
    logger.info(f"Columns in {table_name} DataFrame: {', '.join(df.columns)}")
    
    if table_name == 'departments':
        df = handle_departments_nulls(df)
    elif table_name == 'jobs':
        df = handle_jobs_nulls(df)
    elif table_name == 'hired_employees':
        df = handle_hired_employees_nulls(df)
    else:
        logger.error(f"Unexpected table name: {table_name}")
    
    logger.info(f"Null values handled for {table_name}. Shape: {df.shape}")
    return df

def handle_departments_nulls(df):
    if 'id' in df.columns and 'department' in df.columns:
        df['id'] = df['id'].fillna(-1).astype(int)
        df['department'] = df['department'].fillna('Unknown Department')
    elif len(df.columns) == 2:
        df.columns = ['id', 'department']
        df['id'] = df['id'].fillna(-1).astype(int)
        df['department'] = df['department'].fillna('Unknown Department')
    else:
        logger.error(f"Unexpected structure in departments DataFrame")
    return df

def handle_jobs_nulls(df):
    if 'id' in df.columns and 'job' in df.columns:
        df['id'] = df['id'].fillna(-1).astype(int)
        df['job'] = df['job'].fillna('Unknown Job')
    elif len(df.columns) == 2:
        df.columns = ['id', 'job']
        df['id'] = df['id'].fillna(-1).astype(int)
        df['job'] = df['job'].fillna('Unknown Job')
    else:
        logger.error(f"Unexpected structure in jobs DataFrame")
    return df

def handle_hired_employees_nulls(df):
    expected_columns = ['id', 'name', 'datetime', 'department_id', 'job_id']
    if all(col in df.columns for col in expected_columns):
        df['id'] = df['id'].fillna(-1).astype(int)
        df['name'] = df['name'].fillna('Unknown')
        df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
        df['datetime'] = df['datetime'].fillna(NULL_DATE_PLACEHOLDER)
        df['department_id'] = df['department_id'].fillna(-1).astype(int)
        df['job_id'] = df['job_id'].fillna(-1).astype(int)
    elif len(df.columns) == 5:
        df.columns = expected_columns
        df['id'] = df['id'].fillna(-1).astype(int)
        df['name'] = df['name'].fillna('Unknown')
        df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
        df['datetime'] = df['datetime'].fillna(NULL_DATE_PLACEHOLDER)
        df['department_id'] = df['department_id'].fillna(-1).astype(int)
        df['job_id'] = df['job_id'].fillna(-1).astype(int)
    else:
        logger.error(f"Unexpected structure in hired_employees DataFrame")
    
    placeholder_count = (df['datetime'] == NULL_DATE_PLACEHOLDER).sum()
    logger.info(f"Rows with null or invalid datetimes replaced with placeholder: {placeholder_count}")
    return df