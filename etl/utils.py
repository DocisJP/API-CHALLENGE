import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine, Integer, String, DateTime, inspect
from sqlalchemy.exc import SQLAlchemyError
import logging
from etl.logger import logger
from etl.null_handling import handle_null_values
from etl.config import NULL_DATE_PLACEHOLDER


def create_db_engine(db_params):
    try:
        engine = create_engine(f"postgresql://{db_params['user']}:{db_params['password']}@{db_params['host']}:{db_params['port']}/{db_params['dbname']}")
        return engine
    except Exception as e:
        logger.error(f"Error creating database engine: {str(e)}")
        raise

def read_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        if len(df.columns) == 1:
            logger.warning(f"CSV file {file_path} appears to have no header. Reading without header.")
            df = pd.read_csv(file_path, header=None)
            if file_path.stem == 'departments':
                df.columns = ['id', 'department']
            elif file_path.stem == 'jobs':
                df.columns = ['id', 'job']
            elif file_path.stem == 'hired_employees':
                df.columns = ['id', 'name', 'datetime', 'department_id', 'job_id']
        logger.info(f"Columns in {file_path.stem} CSV: {', '.join(df.columns)}")
        return df
    except Exception as e:
        logger.error(f"Error reading CSV file {file_path}: {str(e)}")
        raise

def validate_schema(df, table_name, engine):
    table_schema = get_table_schema(engine, table_name)
    for column, sa_type in table_schema.items():
        if column not in df.columns:
            logger.warning(f"Column {column} not found in {table_name} DataFrame. Adding with null values.")
            df[column] = pd.NA
        
        pandas_type = sqlalchemy_type_to_pandas(sa_type)
        if not pd.api.types.is_dtype_equal(df[column].dtype, pandas_type):
            logger.warning(f"Data type mismatch for {column} in {table_name}. Attempting to convert.")
            try:
                if pandas_type == 'int64':
                    df[column] = df[column].fillna(0).astype(pandas_type)
                elif pandas_type == 'datetime64[ns]':
                    df[column] = pd.to_datetime(df[column], errors='coerce')
                else:
                    df[column] = df[column].astype(pandas_type)
            except ValueError as e:
                logger.error(f"Unable to convert {column} to {pandas_type}. Error: {str(e)}")
                logger.info(f"Column {column} data sample: {df[column].head()}")
                logger.warning(f"Keeping {column} as is. This may cause issues during insertion.")
    
    extra_columns = set(df.columns) - set(table_schema.keys())
    if extra_columns:
        logger.warning(f"Extra columns found in {table_name} DataFrame: {extra_columns}")
        logger.warning("These columns will be dropped.")
        df = df.drop(columns=extra_columns)
    
    return df

def get_table_schema(engine, table_name):
    inspector = inspect(engine)
    return {column['name']: column['type'] for column in inspector.get_columns(table_name)}

def insert_dataframe(df, table_name, engine):
    inserted_count = 0
    error_count = 0
    try:
        for _, row in df.iterrows():
            try:
                # Ensure datetime is not NaT before inserting
                if 'datetime' in row and pd.isna(row['datetime']):
                    row['datetime'] = NULL_DATE_PLACEHOLDER
                row.to_frame().T.to_sql(table_name, engine, if_exists='append', index=False)
                inserted_count += 1
            except SQLAlchemyError as e:
                error_count += 1
                logger.error(f"Error inserting row into {table_name}: {row.to_dict()}")
                logger.error(f"Error message: {str(e)}")
        
        logger.info(f"Successfully inserted {inserted_count} rows into {table_name}")
        if error_count > 0:
            logger.warning(f"Failed to insert {error_count} rows into {table_name}")
    except Exception as e:
        logger.error(f"Error during batch insert into {table_name}: {str(e)}")
        raise

def sqlalchemy_type_to_pandas(sa_type):
    if isinstance(sa_type, Integer):
        return 'int64'
    elif isinstance(sa_type, String):
        return 'object'
    elif isinstance(sa_type, DateTime):
        return 'datetime64[ns]'
    else:
        return 'object'


def get_existing_ids(engine, table_name, id_column='id'):
    query = f"SELECT {id_column} FROM {table_name}"
    return set(pd.read_sql_query(query, engine)[id_column])

def validate_foreign_keys(df, engine, fk_columns):
    for fk_column, ref_table in fk_columns.items():
        existing_ids = get_existing_ids(engine, ref_table)
        invalid_ids = set(df[fk_column].dropna()) - existing_ids
        if invalid_ids:
            logging.warning(f"Invalid {fk_column} found: {invalid_ids}")
            df = df[~df[fk_column].isin(invalid_ids)]
    return df