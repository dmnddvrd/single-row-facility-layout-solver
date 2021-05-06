from datetime import timedelta
from airflow.utils.dates import days_ago
from airflow import DAG

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['edi.dimand@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=20),
    'execution_timeout': timedelta(seconds=1800),
}

dag = DAG(
    'srflp',
    default_args=default_args,
    description='An srlfp solver dag using permutations',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(2),
    tags=['example'],
)