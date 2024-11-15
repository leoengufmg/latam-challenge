from typing import List, Tuple
from google.cloud import bigquery
import line_profiler
from functions import launch_bigquery


@line_profiler.profile
def q3_time(client: bigquery.Client, sql: str) -> List[Tuple[str, int]]:
    return launch_bigquery(client, sql)
