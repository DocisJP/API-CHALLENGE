import time
import os
import boto3
import yaml
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

config_path = os.path.join(project_root, 'config.yaml')
with open(config_path, 'r') as config_file:
    config = yaml.safe_load(config_file)

s3 = boto3.client('s3', region_name=config['aws']['region'])
bucket_name = config['s3']['raw_bucket']

data_folder_path = os.path.join(project_root, 'data')

class S3UploadHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            file_path = event.src_path
            file_name = os.path.basename(file_path)
            print(f"File {file_name} has been modified. Uploading to S3...")
            s3.upload_file(file_path, bucket_name, file_name)
            print(f"File {file_name} uploaded successfully.")

if __name__ == "__main__":
    event_handler = S3UploadHandler()
    observer = Observer()
    observer.schedule(event_handler, data_folder_path, recursive=False)
    observer.start()
    print(f"Watching for changes in: {data_folder_path}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()