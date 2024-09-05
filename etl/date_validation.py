import pandas as pd
from datetime import datetime, timezone
from etl.logger import logger
from etl.config import NULL_DATE_PLACEHOLDER

def standardize_datetime(dt_str):
    if pd.isna(dt_str):
        return None
    
    try:
        dt = pd.to_datetime(dt_str, utc=True)
        return dt.tz_localize(None)  # Convert to timezone-naive
    except ValueError:
        try:
            dt = pd.to_datetime(dt_str, utc=False)
            dt = dt.tz_localize(timezone.utc).tz_localize(None)  # Assume UTC, then convert to timezone-naive
            return dt
        except ValueError as e:
            logger.error(f"Unable to parse datetime: {dt_str}. Error: {str(e)}")
            return None

def validate_and_standardize_datetimes(df, datetime_column='datetime'):
    if datetime_column not in df.columns:
        logger.warning(f"Datetime column '{datetime_column}' not found in DataFrame.")
        return df
    
    logger.info(f"Validating and standardizing datetimes in column: {datetime_column}")
    
    df[datetime_column] = pd.to_datetime(df[datetime_column], errors='coerce')
    
    # Replace null values with placeholder
    null_count = df[datetime_column].isnull().sum()
    df[datetime_column] = df[datetime_column].fillna(NULL_DATE_PLACEHOLDER)
    
    logger.info(f"Replaced {null_count} null or invalid datetime values with placeholder date.")
    
    return df