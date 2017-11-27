from datetime import timedelta
from datetime import datetime
import logging
import os
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2017, 11, 1),
    'email': ['airflow@airflow.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

THIS_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

with DAG('test2', schedule_interval=timedelta(days=1), default_args=default_args) as dag:

    test = BashOperator(
        task_id = 'test',
        depends_on_past=False,
        bash_command='echo "*** {{ params.dag_path }}"',
        params={'dag_path': '###%s' % THIS_SCRIPT_DIR},
        dag=dag
    )
