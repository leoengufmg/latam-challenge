from typing import List, Tuple
from google.cloud import bigquery
import memory_profiler
from functions import launch_bigquery


@memory_profiler.profile
def q2_memory(client: bigquery.Client, sql: str) -> List[Tuple[str, int]]:
    try:
        results = launch_bigquery(client, sql)
        return [(row[0], int(row[1])) for row in results]
    except ValueError as e:
        print(f"Error converting data to string and integer pairs: {e}")
        return []