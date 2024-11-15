import datetime
from typing import List, Tuple
from google.cloud import bigquery
import line_profiler


@line_profiler.profile
def q1_time(client: bigquery.Client, sql: str) -> List[Tuple[datetime.date, str]]:
    client: bigquery.Client, sql: str