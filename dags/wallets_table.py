import json

from datetime import datetime

from numpy import insert
from faker import Faker

from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

fake = Faker()

def generate_fake_wallets(num_wallets, **context):
    wallets = []
    for _ in range(num_wallets):
        wallet = {
            "user_id": fake.random_int(min=1, max=1000),
            "is_active": fake.boolean(),
            "additional_info": json.dumps({
                "currency": fake.currency_code(),
                "hash": fake.sha256(),
                "balance": fake.random_number(digits=5),
            })
        }
        wallets.append(wallet)
    # Push the generated wallets to XCom
    context["ti"].xcom_push(key="generated_wallets", value=wallets)

def insert_wallets(**context):
    postgres_hook = PostgresHook(postgres_conn_id="postgres1_conn")
    conn = postgres_hook.get_conn()
    cursor = conn.cursor()

    wallets = context["ti"].xcom_pull(key="generated_wallets", task_ids="generate_fake_wallets")

    wallet_values = [(
        wallet["user_id"],
        wallet["is_active"],
        wallet["additional_info"]
    ) for wallet in wallets]

    try:
        cursor.executemany(
            """
            INSERT INTO wallets (
                user_id,
                is_active,
                additional_info
            ) VALUES (%s, %s, %s)
            """,
            wallet_values
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise Exception(f"Error inserting wallets: {e}")
    finally:
        cursor.close()
        conn.close()

def soft_delete_wallets(**context):
    postgres_hook = PostgresHook(postgres_conn_id="postgres1_conn")
    conn = postgres_hook.get_conn()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            UPDATE wallets
            SET
                is_active = FALSE,
                deleted_at = NOW()
            WHERE
                user_id IN (
                    SELECT user_id
                    FROM users
                    WHERE is_active = FALSE
                )
                OR is_active = FALSE;
            """
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise Exception(f"Error soft deleting wallets: {e}")
    finally:
        cursor.close()
        conn.close()

with DAG(
    "wallets_table",
    start_date=datetime(2024, 2, 21),
    schedule_interval="*/10 * * * *",
    catchup=False,
    tags=["wallets", "crud-table"]
) as dag:
    create_table = SQLExecuteQueryOperator(
        task_id="create_table",
        conn_id="postgres1_conn",
        sql="sql/create_wallets.sql",
    )

    generate_fake_wallets = PythonOperator(
        task_id="generate_fake_wallets",
        python_callable=generate_fake_wallets,
        op_kwargs={"num_wallets": fake.random_int(min=1, max=50)},
    )

    insert_wallets_task = PythonOperator(
        task_id="insert_wallets",
        python_callable=insert_wallets,
        provide_context=True,
    )

    soft_delete_wallets_task = PythonOperator(
        task_id="soft_delete_wallets",
        python_callable=soft_delete_wallets,
        provide_context=True,
    )

    create_table >> generate_fake_wallets >> insert_wallets_task >> soft_delete_wallets_task