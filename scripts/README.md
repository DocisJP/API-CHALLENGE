# Scripts for Globant Challenge

This directory contains utility scripts for the Globant Challenge project. These scripts handle various tasks such as data upload, configuration management, and database setup.

## Scripts Overview

### 1. s3_upload_initial.py

This script is responsible for the initial upload of CSV files to the raw data S3 bucket.

**Functionality:**
- Loads configuration from `config.yaml` in the project root.
- Connects to AWS S3 using boto3.
- Uploads all CSV files from the `data` folder to the specified S3 bucket.

**Usage:**
``` bash
python s3_upload_initial.py
```

**Notes:**
- Ensure AWS credentials are properly configured.
- The script will upload all CSV files found in the `data` folder.

### 2. s3_upload_watcher.py

This script sets up a file system watcher to automatically upload modified CSV files to S3.

**Functionality:**
- Uses the `watchdog` library to monitor the `data` folder for file modifications.
- When a file is modified, it's automatically uploaded to the specified S3 bucket.

**Usage:**

``` bash
python s3_upload_watcher.py
```
**Notes:**
- This script runs continuously until interrupted.
- It's useful for development when frequently updating data files.

### 3. update_config.py

This script updates the `config.yaml` file with the RDS endpoint information.

**Functionality:**
- Takes the RDS endpoint as a command-line argument.
- Updates the `config.yaml` file with the new RDS host information.

**Usage:**
``` bash
python update_config.py <rds_endpoint>
```
**Notes:**
- This script is typically called by Terraform after creating the RDS instance.
- Ensures that the application configuration stays in sync with the infrastructure.

### 4. setup_db.py

This script sets up the initial database schema for the project.

**Functionality:**
- Connects to the PostgreSQL database using details from `config.yaml`.
- Creates tables for departments, jobs, and hired employees if they don't exist.

**Usage:**
``` bash
python setup_db.py
```
**Notes:**
- This script is typically called by Terraform after the RDS instance is created.
- Ensures that the database schema is properly set up before data processing begins.

## General Notes

- All scripts use the `config.yaml` file located in the project root for configuration.
- Ensure that the necessary Python packages are installed. You can install them using:
``` bash
pip install -r requirements.txt
```
- These scripts are designed to work in conjunction with the Terraform configuration and AWS services set up for this project.

## Error Handling

- All scripts include basic error handling and will print error messages to the console if issues occur.
- For production use, consider enhancing error handling and adding logging mechanisms.

## Security Considerations

- These scripts assume that AWS credentials are properly configured in the environment or through AWS CLI configuration.
- Be cautious with the `config.yaml` file as it may contain sensitive information. Ensure it's properly secured and not committed to version control.

## Maintenance

When modifying these scripts or the project structure:
1. Update the `config.yaml` path if the project structure changes.
2. Adjust S3 bucket names or other configuration parameters in `config.yaml` as needed.
3. Update the database schema in `setup_db.py` if new tables or modifications are required.