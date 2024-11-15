# -*- coding: utf-8 -*-
"""challenge.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/gist/leoengufmg/634f1023d32b34f3d3033afa8ccb84f8/challenge.ipynb
"""

import sys
import logging
import os
import time
import io

from google.colab import drive

from google.colab import drive
import os
import logging
import subprocess

drive.mount('/content/drive', force_remount=True)

drive_mount_point = '/content/drive/MyDrive'
source_path = 'leonardora/de/latam-challenge/'
target_dir = os.path.join(drive_mount_point, source_path)

if not os.path.exists(target_dir):
    os.makedirs(target_dir)
    print(f"Directorio creado: {target_dir}")
else:
    print(f"Directorio existente: {target_dir}")

os.chdir(target_dir)
print(f"Directorio actual: {os.getcwd()}")

if os.path.exists(os.path.join(target_dir, ".git")):
    print("Repositorio ya existe. Haciendo pull de los últimos cambios...")
    !git checkout hotfix/fix-issue-functions
    !git pull origin hotfix/fix-issue-functions
else:
    repo_url = "https://github.com/leoengufmg/latam-challenge.git"
    print("Clonando el repositorio...")
    !git clone {repo_url} .

    !git checkout hotfix/fix-issue-functions
    !git pull

os.chdir(os.path.join(target_dir, "src"))
!pwd

import os
import logging
import time
import io
import bq_query
from google.colab import drive
from google.colab import auth
from google.cloud import bigquery
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.cloud import storage
from typing import List, Tuple, Any
from functions import (
    authenticate_google_drive, mount_google_drive, create_bucket_if_not_exists,
    download_file_from_drive, upload_drive_file_to_cloud_storage, extract_zip_file_conditionally,
    authenticate_bigquery, create_dataset, create_table, load_data_from_storage, launch_bigquery,
    install_requirements
)


# Configuración inicial
bucket_name = 'gcp_latam_twitter'
folder_name = 'raw'
zip_file_name = 'tweets.json.zip'
file_id = '1ig2ngoXFTxP5Pa8muXo02mDTFexZzsis'
project_id = "latam-challenge-leonardora"
dataset = "latam_tweets_dataset"
table = "tweets"
gcloud_url = f"gs://{bucket_name}/{folder_name}/"
logging_level = str(logging.DEBUG)
logging.basicConfig(level=int(logging_level))

if install_requirements("../requirements.txt"):
  print("Procediendo a descargar datos...")
  # Código para descargar datos u otras acciones adicionales
else:
  print("Error al instalar los requisitos. Abortando acciones adicionales.")

# Autenticación y creación de bucket en GCP
auth.authenticate_user()
new_bucket = create_bucket_if_not_exists(bucket_name, project_id)

try:
    # Autenticación y montaje de Google Drive
    authenticate_google_drive()
    mount_google_drive()
    drive_service: Any = build('drive', 'v3')

    # Acceso a Google Cloud Storage
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    downloaded = download_file_from_drive(drive_service, file_id)

    # Verificar si el archivo tiene contenido
    if downloaded.getbuffer().nbytes == 0:
        logging.info("Skipping upload as the file is empty.")
    else:
        # Cargar el archivo en Google Cloud Storage
        uploaded_blob = upload_drive_file_to_cloud_storage(bucket, folder_name, downloaded, zip_file_name)

        # Descomprimir el archivo si es un ZIP
        json_file_name: str = extract_zip_file_conditionally(bucket, folder_name, zip_file_name)

    logging.info("File transfer successful!")

except Exception as e:
    logging.error(f"An error occurred: {e}")

finally:
    downloaded.close()
    print("File transfer process completed.")

downloaded.close()

# Autenticación en BigQuery y creación de dataset y tabla
bigquery_client = authenticate_bigquery(project_id)
create_dataset(bigquery_client, dataset, mode='overwrite')
create_table(bigquery_client, dataset, table, mode='overwrite')

drive_mount_point = '/content/drive/MyDrive'
source_path = 'leonardora/de/latam-challenge/'

# Set Google Cloud project and dataset info
project_id = "latam-challenge-leonardora"
project_name = "latam-challenge-leonardora"
dataset = "latam_tweets_dataset"
table ="tweets"
json_file_name = "farmers-protest-tweets-2021-2-4.json"
# Carga de datos desde Cloud Storage a BigQuery
load_data_from_storage(bigquery_client, gcloud_url, dataset, table, json_file_name)

# Consultas y perfilado de tiempo con LineProfiler
from line_profiler import LineProfiler

bigquery_client: bigquery.Client = authenticate_bigquery(project_id)

profiler = LineProfiler()

from q1_time import q1_time
from q2_time import q2_time
from q3_time import q3_time

from q1_memory import q1_memory
from q2_memory import q2_memory
from q3_memory import q3_memory

# Consulta de las fechas con más tweets y usuario con más tweets cada día
profiler.add_function(q1_time)
profiler.enable_by_count()
q1_time_tuple = q1_time(bigquery_client, bq_query.top_dates_with_top_users)
profiler.print_stats()
display(q1_time_tuple)

# Consulta de los 10 emojis más usados
profiler.add_function(q2_time)
profiler.enable_by_count()
q2_time_tuple = q2_time(bigquery_client, bq_query.top_emojis)
profiler.print_stats()
display(q2_time_tuple)

# Consulta de los 10 usuarios más influyentes
profiler.add_function(q3_time)
profiler.enable_by_count()
q3_time_tuple = q3_time(bigquery_client, bq_query.top_influential_users)
profiler.print_stats()
display(q3_time_tuple)

# Análisis de memoria para cada consulta
print("Análisis de Memoria - Top 10 Fechas con más Tweets")
q1_memory(bigquery_client, bq_query.top_dates_with_top_users)

print("Análisis de Memoria - Top 10 Emojis más usados")
q2_memory(bigquery_client, bq_query.top_emojis)

print("Análisis de Memoria - Top 10 Usuarios más influyentes")
q3_memory(bigquery_client, bq_query.top_influential_users)

