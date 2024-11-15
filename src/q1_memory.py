import datetime
from typing import List, Tuple
from google.cloud import bigquery
import memory_profiler


@memory_profiler.profile
def q1_memory(client: bigquery.Client, sql: str) -> List[Tuple[datetime.date, str]]:
    return launch_bigquery(client, sql)