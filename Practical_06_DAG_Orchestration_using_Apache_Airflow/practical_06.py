"""
Practical 6: DAG Orchestration using Apache Airflow
Name: Shivam Singh | Roll No. 56 | Student ID 5135873 | T.Y. Data Science
"""

# ===== Task 1: Airflow Workflow DAG Configuration =====
from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.empty import EmptyOperator

default_args = {
    "owner": "data_engineering_lab",
    "start_date": datetime(2026, 1, 1)
}

with DAG(
    "university_etl_orchestration",
    default_args=default_args,
    schedule=timedelta(days=1),
    catchup=False
) as dag:

    start_pipeline = EmptyOperator(task_id="start_pipeline")

    execute_extraction = BashOperator(
        task_id="run_extraction_script",
        bash_command="python3 /content/data_extraction.py"
    )

    pipeline_complete = BashOperator(
        task_id="log_pipeline_success",
        bash_command='echo "ETL completed successfully"'
    )

    start_pipeline >> execute_extraction >> pipeline_complete

