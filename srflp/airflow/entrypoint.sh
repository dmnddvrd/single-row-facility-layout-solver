#!/usr/bin/env bash

# pip install -e custom library
cd /usr/local/airflow/srflp-solver
echo 'Removing cached files'
find . -name "*.pyc" -type f -delete
find . -name a -exec ls {} \;
echo 'Finished removing cached files'
pip install -e .
cd /usr/local/airflow
# Initiliase the metastore
airflow initdb
# Run the scheduler in background
airflow scheduler &> /dev/null &
# Run the web server in foreground (for docker logs)
exec airflow webserver
