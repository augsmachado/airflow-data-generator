from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python import PythonOperator
from datetime import datetime
import logging

# Configuração padrão da DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 2, 21),
}

# Função para imprimir mensagens antes e depois
def log_message(message):
    logging.info(message)

with DAG('dual_postgres_dag', default_args=default_args, schedule_interval=None) as dag:

    # Mensagem antes da primeira query
    start_task1 = PythonOperator(
        task_id='start_query_postgres1',
        python_callable=log_message,
        op_args=['Iniciando query no postgres1...']
    )

    # Execução da query no primeiro banco
    task1 = PostgresOperator(
        task_id='query_postgres1',
        postgres_conn_id='postgres1_conn',
        sql="SELECT NOW();"
    )

    # Mensagem após a primeira query
    end_task1 = PythonOperator(
        task_id='end_query_postgres1',
        python_callable=log_message,
        op_args=['Finalizando query no postgres1...']
    )

    # Mensagem antes da segunda query
    start_task2 = PythonOperator(
        task_id='start_query_postgres2',
        python_callable=log_message,
        op_args=['Iniciando query no postgres2...']
    )

    # Execução da query no segundo banco
    task2 = PostgresOperator(
        task_id='query_postgres2',
        postgres_conn_id='postgres2_conn',
        sql="SELECT NOW();"
    )

    # Mensagem após a segunda query
    end_task2 = PythonOperator(
        task_id='end_query_postgres2',
        python_callable=log_message,
        op_args=['Finalizando query no postgres2...']
    )

    # Definição da ordem de execução
    start_task1 >> task1 >> end_task1 >> start_task2 >> task2 >> end_task2
