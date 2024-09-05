import psycopg2
import yaml
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
config_path = os.path.join(project_root, 'config.yaml')

print(f"Looking for config file at: {config_path}")

with open(config_path, 'r') as config_file:
    config = yaml.safe_load(config_file)


db_params = {
    'dbname': config['rds']['db_name'],
    'user': config['rds']['username'],
    'password': config['rds']['password'],
    'host': config['rds']['host'],
    'port': config['rds']['port']
}

create_tables = [
    """
    CREATE TABLE IF NOT EXISTS departments (
        id INTEGER PRIMARY KEY,
        department VARCHAR(100) NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY,
        job VARCHAR(100) NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS hired_employees (
        id INTEGER PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        datetime TIMESTAMP NOT NULL,
        department_id INTEGER,
        job_id INTEGER,
        FOREIGN KEY (department_id) REFERENCES departments (id),
        FOREIGN KEY (job_id) REFERENCES jobs (id)
    )
    """
]

def setup_database():
    conn = None
    try:
        print("Connecting to the database...")
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        for create_table_sql in create_tables:
            print(f"Executing: {create_table_sql}")
            cur.execute(create_table_sql)

        conn.commit()
        print("Database schema created successfully.")

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        if conn is not None:
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    setup_database()