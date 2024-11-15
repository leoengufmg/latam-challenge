import io
import importlib.util
import logging
import os
import sys
import subprocess
import sys
import time
from typing import Any


from google.api_core.exceptions import Conflict
from google.api_core.exceptions import NotFound
from google.cloud import storage
from google.cloud import bigquery
from google.colab import auth
from google.colab import drive
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload


## Requirements
def install_requirements(requirements_path: str = "./requirements.txt") -> bool:
    try:
        with open(requirements_path, 'r') as file:
            requirements = [line.strip() for line in file if line.strip()]

        for requirement in requirements:
            print(f"Installing {requirement}...")
            subprocess.run([sys.executable, "-m", "pip", "install", requirement], check=True)
            print(f"{requirement} installed successfully.")

        print("All required libraries were installed successfully.")
        return True

    except subprocess.CalledProcessError as e:
        print(f"Error installing libraries: {e}")
        return False
    except FileNotFoundError:
        print(f"Requirements file not found at: {requirements_path}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False
    

## Google 
### bucket
def create_bucket_if_not_exists(bucket_name: str, project_id: str, location: str = "US") -> storage.Bucket:
    # Initialize the Google Cloud Storage client
    storage_client = storage.Client(project=project_id)

    # Check if the bucket already exists
    try:
        bucket = storage_client.get_bucket(bucket_name)
        print(f"Bucket {bucket_name} already exists.")
        return bucket
    except Exception:
        print(f"Bucket {bucket_name} does not exist, attempting to create it.")

    # Create the bucket if it does not exist
    try:
        bucket = storage_client.create_bucket(bucket_name, location=location)
        print(f"Bucket {bucket.name} created in {location}.")
        return bucket
    except Conflict:
        print(f"Bucket {bucket_name} already exists (Conflict error).")
        return storage_client.get_bucket(bucket_name)
    except Exception as e:
        print(f"Error creating bucket: {e}")
        raise

### drive
def authenticate_google_drive() -> None:
    """Authenticate the user with Google Drive."""
    auth.authenticate_user()

def mount_google_drive(mount_point: str = '/content/drive') -> None:
    """Mounts Google Drive to a specified mount point."""
    drive.mount(mount_point, force_remount=True)

def download_file_from_drive(drive_service: Any, file_id: str) -> io.BytesIO:
    """Downloads a file from Google Drive and returns it as a BytesIO object."""
    downloaded = io.BytesIO()
    try:
        request = drive_service.files().get_media(fileId=file_id)
        downloader = MediaIoBaseDownload(downloaded, request)
        
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f'Downloading {int(status.progress() * 100)}%')
        
        downloaded.seek(0)
        return downloaded
    except Exception as e:
        logging.error(f"Error downloading file: {e}")
        raise

def upload_drive_file_to_cloud_storage(bucket: storage.Bucket, folder_name: str, file_data: io.BytesIO, file_name: str) -> storage.Blob:
    """Uploads a file to Google Cloud Storage."""
    blob = bucket.blob(f"{folder_name}/{file_name}")
    file_data.seek(0)  # Resetea el puntero del archivo
    blob.upload_from_file(file_data)
    return blob


def extract_zip_file_conditionally(bucket: storage.Bucket, folder_name: str, zip_file_name: str) -> str:
    json_file_name = ''
    blob_name = ''
    try:
        zip_blob = bucket.blob(f'{folder_name}/{zip_file_name}')
        if not zip_blob.exists():
            print(f"ZIP file '{zip_file_name}' does not exist in bucket '{bucket.name}'.")
            return False
        with zipfile.ZipFile(io.BytesIO(zip_blob.download_as_string()), 'r') as z:
            for file_info in z.infolist():
                blob_name = f'{folder_name}/{file_info.filename}'
                json_file_name = file_info.filename
                json_blob = bucket.blob(blob_name)
                if json_blob.exists():
                    existing_blob_data: str = json_blob.download_as_string()
                    existing_blob_size: int = len(existing_blob_data)
                if json_blob.exists() and existing_blob_size == file_info.file_size:
                    print(f"File '{json_file_name}' already exists on cloud storage with exact matching size, skipping extraction.")
                else:
                    with z.open(file_info) as file:
                        json_blob.upload_from_file(file)
                    print(f'ZIP File extracted to gs://{bucket.name}/{blob_name}')
    except zipfile.BadZipFile:
        logging.warning(f'Invalid ZIP file: gs://{bucket.name}/{folder_name}/{zip_file_name}')
    except Exception as e:
        logging.error(f'Error extracting ZIP file: {e}')
    finally:
        return json_file_name
    
### bigquery
def authenticate_bigquery(project_id: str) -> bigquery.Client:
    """
    Authenticates to BigQuery and returns the client object.
    """
    try:
        client = bigquery.Client(project=project_id)
        logging.info(f"Authenticated to BigQuery using project ID '{project_id}'.")
        return client
    except Exception as e:
        logging.error(f"Authentication to BigQuery failed: {e}")
        raise


def create_dataset(client: bigquery.Client, dataset_id: str, mode: str = "create") -> None:
    """
    Creates a BigQuery dataset, with options for existence checks and overwriting.
    """
    dataset_ref = client.dataset(dataset_id)
    try:
        client.get_dataset(dataset_ref)
        if mode == "overwrite":
            logging.info(f"Overwriting dataset '{dataset_id}'...")
            client.delete_dataset(dataset_ref, delete_contents=True)
            client.create_dataset(dataset_ref)
            logging.info(f"Dataset '{dataset_id}' overwritten.")
        else:
            logging.info(f"Dataset '{dataset_id}' already exists. Skipping creation.")
    except NotFound:
        logging.info(f"Dataset '{dataset_id}' not found, creating...")
        client.create_dataset(dataset_ref)
        logging.info(f"Dataset '{dataset_id}' created.")
    except Exception as e:
        logging.error(f"Error managing dataset '{dataset_id}': {e}")
        raise


def create_table(client: bigquery.Client, dataset_id: str, table_name: str, mode: str = "create") -> None:
    """
    Creates a BigQuery table, with options for existence checks and overwriting.
    """
    table_ref = client.dataset(dataset_id).table(table_name)
    try:
        client.get_table(table_ref)
        if mode == "overwrite":
            logging.info(f"Overwriting table '{table_name}'...")
            client.delete_table(table_ref)
            client.create_table(bigquery.Table(table_ref))
            logging.info(f"Table '{table_name}' overwritten.")
        else:
            logging.info(f"Table '{table_name}' already exists. Skipping creation.")
    except NotFound:
        logging.info(f"Table '{table_name}' not found, creating...")
        client.create_table(bigquery.Table(table_ref))
        logging.info(f"Table '{table_name}' created.")
    except Exception as e:
        logging.error(f"Error managing table '{table_name}': {e}")
        raise


def load_data_from_storage(client: bigquery.Client, source_uri: str, dataset_name: str, table_name: str, json_file_name: str) -> None:
    full_source_uri = source_uri + json_file_name
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        autodetect=True,
        ignore_unknown_values=True
    )
    load_job = client.load_table_from_uri(
        full_source_uri,
        client.dataset(dataset_name).table(table_name), 
        job_config=job_config
    )
    try:
        load_job.result()
        logging.info(f"Data loaded from '{full_source_uri}' to table '{dataset_name}.{table_name}'.")
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        raise


def process_bigquery_results(client: bigquery.Client, query: str) -> List[Tuple[Any, Any]]:
    data_extracted : List[Tuple[Any, Any]] = []

    try:
        query_job = client.query(query)
        results = query_job.result()

        if results.total_rows == 0:
            raise NotFound("No results found for the query.")

        data_extracted  = [(row[0], row[1]) for row in results]

    except BadRequest as e:
        print(f"BigQuery BadRequest error: {e}")
        raise
    except NotFound as e:
        print(f"Query returned no results: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise

    return data_extracted 