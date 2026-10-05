from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.filesystem import FileSensor


default_args = {
    "owner": "data-engineering",
    "retries": 3,
    "retry_delay": timedelta(minutes=2),
}


with DAG(
    dag_id="customer_etl_pipeline",
    start_date=datetime(2026, 10, 1),
    schedule="@daily",
    catchup=False,
    default_args=default_args,
) as dag:

    wait_for_file = FileSensor(
        task_id="wait_for_customer_file",
        filepath="customers.csv",
        poke_interval=30,
        timeout=300,
        mode="poke",
    )

    def extract_task(**context):

        records = 5

        context["ti"].xcom_push(
            key="records_extracted",
            value=records
        )

        print(
            f"Extracted {records} records"
        )

    extract = PythonOperator(
        task_id="extract",
        python_callable=extract_task,
    )

    def validate_task(**context):

        records = context["ti"].xcom_pull(
            task_ids="extract",
            key="records_extracted"
        )

        print(
            f"Validating {records} records"
        )

    validate = PythonOperator(
        task_id="validate",
        python_callable=validate_task,
    )

    wait_for_file >> extract >> validate

context["ti"].xcom_push(
    key="records_extracted",
    value=records
)

xcom_pull()

default_args = {
    "owner": "data-engineering",
    "retries": 3,
    "retry_delay": timedelta(minutes=2),
}

def task_failure_alert(context):

    task_id = context["task_instance"].task_id

    print(
        f"Task failed: {task_id}"
    )

default_args = {
    "owner": "data-engineering",
    "retries": 3,
    "retry_delay": timedelta(minutes=2),
    "on_failure_callback": task_failure_alert
}