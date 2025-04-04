import json

from datetime import datetime
from venv import create
from faker import Faker

from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

fake = Faker()

def generate_fake_payments(num_payments, **context):
    pass


with DAG(
    "payments_table",
    start_date=datetime(2025, 4, 4),
    schedule_interval="* * * * *",
    catchup=False,
    tags=["payments", "crud-table"]
) as dag:
    create_table = SQLExecuteQueryOperator(
        task_id="create_table",
        conn_id="postgres1_conn",
        sql="sql/create_payments.sql",
    )
    
    fetch_records = SQLExecuteQueryOperator(
        task_id="fetch_records",
        conn_id="postgres1_conn",
        sql="SELECT * FROM payments LIMIT 1;",
    )
    
    # Define the task dependencies
    create_table >> fetch_records