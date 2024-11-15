from typing import List, Tuple
from google.cloud import bigquery
import memory_profiler
from functions import launch_bigquery


@memory_profiler.profile
def q3_memory(client: bigquery.Client, sql: str) -> List[Tuple[str, int]]:
   try:
       results = launch_bigquery(client, sql)
       formatted_results = [(row[0], int(row[1])) for row in results]

       if len(formatted_results) > 1000:
           print("Warning: Returning a large dataset. Consider using streaming or pagination for memory optimization.")
       return formatted_results
   except ValueError as e:
       print(f"Error converting data to string and integer pairs: {e}")
       return []
