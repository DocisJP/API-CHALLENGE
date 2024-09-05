from pathlib import Path
from etl.config import DB_PARAMS, DATA_DIR
from etl.utils import (
    create_db_engine, read_csv, insert_dataframe, validate_foreign_keys,
    handle_null_values, validate_schema
)
from etl.load import load_process
from etl.logger import logger
from etl.config import NULL_DATE_PLACEHOLDER

def process_table(engine, table_name, fk_columns=None):
    logger.info(f"{'='*20} Processing {table_name} table {'='*20}")
    
    csv_file = DATA_DIR / f'{table_name}.csv'
    logger.info(f"Reading CSV file: {csv_file}")
    df = read_csv(csv_file)
    logger.info(f"Read {len(df)} rows from {table_name}.csv")
    logger.info(f"First few rows of {table_name}:\n{df.head().to_string()}")
    
    df = handle_null_values(df, table_name)
    
    logger.info(f"Validating schema for {table_name}")
    df = validate_schema(df, table_name, engine)
    logger.info(f"Schema validated. Final shape: {df.shape}")
    
    if table_name == 'hired_employees':
        placeholder_datetimes = (df['datetime'] == NULL_DATE_PLACEHOLDER).sum()
        if placeholder_datetimes > 0:
            logger.warning(f"Found {placeholder_datetimes} placeholder datetime values in hired_employees after handling nulls.")

    if fk_columns:
        logger.info(f"Validating foreign keys for {table_name}: {fk_columns}")
        df = validate_foreign_keys(df, engine, fk_columns)
        logger.info(f"Foreign keys validated. Rows remaining: {len(df)}")
    
    logger.info(f"Inserting data into {table_name} table")
    insert_dataframe(df, table_name, engine)
    logger.info(f"{'='*20} Completed processing {table_name} table {'='*20}\n")

def etl_process():
    try:
        logger.info("Starting ETL process")
        
        logger.info("Initializing database")
        load_process()
        
        logger.info("Creating database engine")
        engine = create_db_engine(DB_PARAMS)
        logger.info("Database engine created successfully")

        # Process each table in the correct order
        process_table(engine, 'departments')
        process_table(engine, 'jobs')
        process_table(engine, 'hired_employees', 
                      fk_columns={'department_id': 'departments', 'job_id': 'jobs'})

        logger.info("ETL process completed successfully")

    except Exception as e:
        logger.error(f"ETL process failed: {str(e)}", exc_info=True)