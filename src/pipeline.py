import os
import logging
import time
import io
import bq_query
from google.colab import drive
from google.colab import auth
from google.cloud import bigquery
from line_profiler import LineProfiler
from functions import (
    authenticate_google_drive, mount_google_drive, create_bucket_if_not_exists, 
    download_file_from_drive, upload_drive_file_to_cloud_storage, extract_zip_file_conditionally, 
    authenticate_bigquery, create_dataset, create_table, load_data_from_storage, 
    q1_time, q2_time, q3_time, process_bigquery_results,
    q1_memory, q2_memory, q3_memory
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

# Montaje de Google Drive
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

# Clonar o actualizar el repositorio
if os.path.exists(os.path.join(target_dir, ".git")):
    print("Repositorio ya existe. Haciendo pull de los últimos cambios...")
    os.system("git checkout develop")
    os.system("git pull origin develop")
else:
    repo_url = "https://github.com/leoengufmg/latam-challenge.git"
    print("Clonando el repositorio...")
    os.system(f"git clone {repo_url} .")
    os.system("git checkout develop")

# Autenticación y creación de bucket en GCP
auth.authenticate_user()
new_bucket = create_bucket_if_not_exists(bucket_name, project_id)

# Descarga de archivo de Google Drive y carga en Google Cloud Storage
downloaded = download_file_from_drive(file_id)
if downloaded.getbuffer().nbytes != 0:
    upload_drive_file_to_cloud_storage(bucket_name, folder_name, downloaded, zip_file_name)
    json_file_name = extract_zip_file_conditionally(bucket_name, folder_name, zip_file_name)
    logging.info("File transfer successful!")
else:
    logging.info("Skipping upload as the file is empty.")

downloaded.close()

# Autenticación en BigQuery y creación de dataset y tabla
bigquery_client = authenticate_bigquery(project_id)
create_dataset(bigquery_client, dataset, mode='overwrite')
create_table(bigquery_client, dataset, table, mode='overwrite')

# Carga de datos desde Cloud Storage a BigQuery
load_data_from_storage(bigquery_client, gcloud_url, dataset, table, json_file_name)

# Consultas y perfilado de tiempo con LineProfiler
profiler = LineProfiler()

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
