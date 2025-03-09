from airflow import DAG

from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

from datetime import datetime

with DAG('create_table',
    start_date=datetime(2024, 2, 21),
    schedule_interval="@hourly",
    catchup=False
) as dag:
    create_table = SQLExecuteQueryOperator(
        task_id="create_table",
        conn_id="postgres1_conn",
        sql="sql/create_users.sql",
    )
    
    populate_table = SQLExecuteQueryOperator(
        task_id="populate_table",
        conn_id="postgres1_conn",
        sql="sql/insert_users.sql",
    )
    
    fetch_records = SQLExecuteQueryOperator(
        task_id="fetch_records",
        conn_id="postgres1_conn",
        sql="SELECT * FROM users;",
    )
    
    create_table >> populate_table >> fetch_records