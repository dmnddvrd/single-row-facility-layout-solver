from datetime import timedelta
from airflow.utils.dates import days_ago
from airflow import DAG
import srflp.utils.config as config
from airflow.operators.python_operator import PythonOperator
import MySQLdb
import csv, os, time
from datetime import date
import pandas as pd


DB_HOST = config.get("DB_HOST")
DB_USER = config.get("DB_USER")
DB_PASS = config.get("DB_PASSWORD")
DB_SCHEMA = config.get("DB_SCHEMA")

DATA = []


def get_problems():
    db = MySQLdb.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, db=DB_SCHEMA)
    curs = db.cursor()
    curs.execute('SELECT * FROM srflp_problems where status = "Finished";')
    for row in curs.fetchall():
        print(row)
        DATA.append(row)
    db.close()


def process_data():
    print("PROCESS")


def export_data():
    print("EXPORT")


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email": ["edi.dimand@gmail.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=20),
    "execution_timeout": timedelta(seconds=18000),
}

dag = DAG(
    "Statistics",
    default_args=default_args,
    description="An srlfp solver dag using permutations",
    schedule_interval=timedelta(hours=1),
    start_date=days_ago(1),
    tags=["srflp-statistics"],
)

collect_data = PythonOperator(
    task_id="collect_data",
    python_callable=get_problems,
    dag=dag,
)

process_problems = PythonOperator(
    task_id="solve_problems",
    python_callable=process_data,
    dag=dag,
)

export_csv = PythonOperator(
    task_id="export_csv",
    python_callable=export_data,
    dag=dag,
)

collect_data >> process_problems >> export_csv
