from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from extracao_mysql import extrair_metadados_mysql
from indexacao import indexar_metadados

dag_args = {
    'concurrency': 10,
    'max_active_runs': 1,
    'schedule_interval': '@daily',
    'catchup': False
}

default_args = {
    'owner': 'amundsen',
    'start_date': datetime(2023, 3, 1),
    'depends_on_past': False,
    'retries': 0,
    'execution_timeout': timedelta(minutes=120)
}

with DAG('metadados_mysql_dag', default_args=default_args, **dag_args) as dag:
    extracao_metadados_mysql_task = PythonOperator(
        task_id='extracao_metadados_mysql',
        python_callable=extrair_metadados_mysql
    )

    indexacao_metadados_task = PythonOperator(
        task_id='indexacao_metadados',
        python_callable=indexar_metadados
    )

    extracao_metadados_mysql_task >> indexacao_metadados_task
