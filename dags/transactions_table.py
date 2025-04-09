from itertools import count
import json

from datetime import datetime
from faker import Faker

from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

fake = Faker()

def generate_fake_transactions(num_transactions, **context):
    transactions = []
    for _ in range(num_transactions):
        transaction = {
            "wallet_id": fake.random_int(min=1, max=100),
            "amount": fake.random_number(digits=3),
            "status": fake.random_element(elements=(
                'pending','paid', 'refused', 'refunded',
                'cancelled', 'failed', 'disputed',
                'chargeback', 'reversed', 'completed',
                'processing', 'on_hold', 'partially_refunded',
                'partially_paid', 'voided'
            )),
            "type": fake.random_element(elements=(
                'credit', 'debit'
            )),
            "method": fake.random_element(elements=(
                'credit_card', 'debit_card', 'paypal',
                'pix', 'boleto', 'cash', 'gift_card',
                'bank_transfer', 'crypto'
            )),
            "additional_info": json.dumps({
                "end_to_end_id": fake.iban(),
                "currency": fake.currency_code(),
                "sku": fake.random_int(min=1000, max=9999),
                "coordinates": fake.local_latlng(country_code=fake.country_code()),
                "merchant_name": fake.company(),
                "description": fake.sentence(),
            })
        }
        transactions.append(transaction)
    # Push the generated transactions to XCom
    context["ti"].xcom_push(key="generated_transactions", value=transactions)

def insert_transactions(**context):
    postgres_hook = PostgresHook(postgres_conn_id="postgres1_conn")
    conn = postgres_hook.get_conn()
    cursor = conn.cursor()
    
    transactions = context["ti"].xcom_pull(key="generated_transactions", task_ids="generate_fake_transactions")
    
    transaction_values = [(
        transaction["wallet_id"],
        transaction["amount"],
        transaction["status"],
        transaction["type"],
        transaction["method"],
        transaction["additional_info"]
    ) for transaction in transactions]
    
    try:
        cursor.executemany(
            """
            INSERT INTO transactions (
                wallet_id,
                amount,
                status,
                type,
                method,
                additional_info
            ) VALUES (%s, %s, %s, %s, %s, %s);
            """,
            transaction_values
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise Exception(f"Error inserting transactions: {e}")
    finally:
        cursor.close()
        conn.close()

def update_transactions(**context):
    postgres_hook = PostgresHook(postgres_conn_id="postgres1_conn")
    conn = postgres_hook.get_conn()
    cursor = conn.cursor()

    try:
        cursor.execute(
            f"""
            UPDATE transactions
            SET
                status = CAST(
                    (
                        SELECT status
                        FROM (
                            VALUES ('paid'), ('refused'), ('refunded'), ('cancelled'), ('failed'), ('chargeback'), ('reversed'), ('completed'), ('partially_refunded'), ('partially_paid'), ('voided')
                        ) AS random_status(status)
                        ORDER BY random()
                        LIMIT 1
                    ) AS transaction_status
                ),
                updated_at = NOW()
            WHERE
                status IN ('pending', 'disputed', 'processing', 'on_hold')
                AND updated_at IS NULL;
            """
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise Exception(f"Error updating transactions: {e}")
    finally:
        cursor.close()
        conn.close()

def soft_delete_transactions(**context):
    postgres_hook = PostgresHook(postgres_conn_id="postgres1_conn")
    conn = postgres_hook.get_conn()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            UPDATE transactions
            SET deleted_at = NOW()
            WHERE
                deleted_at IS NULL
                AND status IN ('failed', 'voided');
            """
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise Exception(f"Error updating transactions: {e}")
    finally:
        cursor.close()
        conn.close()

with DAG(
    "transactions_table",
    start_date=datetime(2024, 2, 21),
    schedule_interval="* * * * *",
    catchup=False,
    tags=["transactions", "crud-table"]
) as dag:
    create_table = SQLExecuteQueryOperator(
        task_id="create_table",
        conn_id="postgres1_conn",
        sql="sql/create_transactions.sql",
    )
    
    generate_fake_transactions = PythonOperator(
        task_id="generate_fake_transactions",
        python_callable=generate_fake_transactions,
        op_kwargs={"num_transactions": fake.random_int(min=100, max=2000)}
    )

    insert_transactions_task = PythonOperator(
        task_id="insert_transactions",
        python_callable=insert_transactions,
        provide_context=True,
    )

    update_transactions_task = PythonOperator(
        task_id="update_transactions",
        python_callable=update_transactions,
        provide_context=True,
    )

    soft_delete_transactions_task = PythonOperator(
        task_id="soft_delete_transactions",
        python_callable=soft_delete_transactions,
        provide_context=True,
    )

    create_table >> generate_fake_transactions >> insert_transactions_task >> update_transactions_task >> soft_delete_transactions_task