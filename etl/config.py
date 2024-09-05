import yaml
import os
from pathlib import Path
import datetime

NULL_DATE_PLACEHOLDER = datetime.datetime(1900, 1, 1)

def load_config():
    config_path = Path(__file__).parent.parent / "config.yaml"
    with open(config_path, "r") as config_file:
        return yaml.safe_load(config_file)

CONFIG = load_config()

# Database connection parameters
DB_PARAMS = {
    'dbname': CONFIG['local_db']['db_name'],
    'user': CONFIG['local_db']['username'],
    'password': CONFIG['local_db']['password'],
    'host': CONFIG['local_db']['host'],
    'port': CONFIG['local_db']['port']
}

# Data directory
DATA_DIR = Path(CONFIG['paths']['data_dir'])