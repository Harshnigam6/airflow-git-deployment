from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
import os

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 12, 4),
    'catchup': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'run_hello_script_dag',
    default_args=default_args,
    description='A DAG to run the hello script',
    schedule_interval=timedelta(days=1),
)

def wrapper_function():
    def list_directory_contents(directory):
        print(f"Contents of {directory}:")
        for filename in os.listdir(directory):
            print(filename)

    list_directory_contents("/opt/airflow/")
    list_directory_contents("/opt/airflow/data")

    # from hello_script import main  # Assuming scripts is in PYTHONPATH
    from airbnb_los_test import DataQualityChecker

hello_task = PythonOperator(
    task_id='run_hello_script',
    python_callable=wrapper_function,
    dag=dag,
)

# Bash task to run the Python script
run_airbnb_los_test_task = BashOperator(
    task_id='run_airbnb_los_test',
    bash_command='python /opt/airflow/data/task_one.py',
    dag=dag,
)

# Setting up dependencies
hello_task >> run_airbnb_los_test_task
