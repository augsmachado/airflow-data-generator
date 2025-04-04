import json

from datetime import datetime
from faker import Faker

from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

fake = Faker()

def generate_fake_users(num_users, **context):
    users = []
    for _ in range(num_users):
        user = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.email(),
            'birth_date': fake.date_of_birth().isoformat(),
            'tax_id': fake.ssn(),
            'is_active': fake.boolean(),
            'additional_info': json.dumps({
                'address': fake.address(),
                'favorite_color': fake.color_name(),
                'favorite_food': fake.word(),
                'favorite_movie': fake.word(),
                'favorite_music_genre': fake.word(),
            })
        }
        users.append(user)

    # Push the generated users to XCom
    context['ti'].xcom_push(key='generated_users', value=users)


def insert_users(**context):
    postgres_hook = PostgresHook(postgres_conn_id="postgres1_conn")
    conn = postgres_hook.get_conn()
    cursor = conn.cursor()

    users = context['ti'].xcom_pull(key='generated_users', task_ids='generate_fake_users')

    for user in users:
        try:
            cursor.execute(
                """
                INSERT INTO users (
                    first_name,
                    last_name,
                    email,
                    birth_date,
                    tax_id,
                    is_active,
                    additional_info
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (email) DO NOTHING;
                """,
                (
                    user['first_name'],
                    user['last_name'],
                    user['email'],
                    user['birth_date'],
                    user['tax_id'],
                    user['is_active'],
                    user['additional_info'])
            )
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"Error inserting user: {user}. Error: {e}")

def update_users(**context):
    postgres_hook = PostgresHook(postgres_conn_id="postgres1_conn")
    conn = postgres_hook.get_conn()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            UPDATE users
            SET email = lower(first_name || '.' || last_name || '@' || split_part(email, '@', 2)),
                updated_at = NOW()
            WHERE updated_at IS NULL;
            """
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error updating users: {e}")

with DAG('users_table',
    start_date=datetime(2024, 2, 21),
    schedule_interval="*/2 * * * *",
    catchup=False
) as dag:
    create_table = SQLExecuteQueryOperator(
        task_id="create_table",
        conn_id="postgres1_conn",
        sql="sql/create_users.sql",
    )

    generate_fake_users = PythonOperator(
        task_id='generate_fake_users',
        python_callable=generate_fake_users,
        op_kwargs={'num_users': 10}
    )

    insert_users_task = PythonOperator(
        task_id='insert_users',
        python_callable=insert_users,
        provide_context=True,
    )

    update_users_task = PythonOperator(
        task_id='update_users',
        python_callable=update_users,
        provide_context=True,
    )

    fetch_records = SQLExecuteQueryOperator(
        task_id="fetch_records",
        conn_id="postgres1_conn",
        sql="SELECT * FROM users;",
    )

    # Define the task dependencies
    create_table >> generate_fake_users >> insert_users_task >> update_users_task >> fetch_records