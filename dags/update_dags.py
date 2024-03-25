from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 12, 26),
    'catchup': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('update_dags_new',
          default_args=default_args,
          description='A DAG to update dags',
          schedule_interval=timedelta(days=1),
        #   catchup=False
          )

print("-------------------------+++++++++++++--------------------------------------------------")

# Task to clone the Git repository
clone_or_pull_repo = BashOperator(
    task_id='clone_or_pull_repo',
    bash_command='git_pull.sh',
    dag=dag,
)


# Task to print the contents of the data directory
print_files = BashOperator(
    task_id='print_files',
    bash_command='ls -lah /opt/airflow/temp',
    dag=dag,
)

# Task to copy DAG files to the Airflow dags directory
# airflow dags list -> forces ariflow to instantly recognize dags from pricelabd repo
copy_dags = BashOperator(
    task_id='copy_dags',
    bash_command='cp -r /opt/airflow/temp/airflow/dags/* /opt/airflow/dags && airflow dags list',
    dag=dag,
)


clone_or_pull_repo >> print_files >> copy_dags
