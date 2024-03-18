from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from extracao_postgresql import extrair_metadados_postgres
from indexacao import indexar_metadados

dag_args = {
    'max_active_runs': 1,
    'schedule_interval': '@daily',
    'catchup': False
}

default_args = {
    'owner': 'amundsen',
    'start_date': datetime(2023, 3, 1),
    'depends_on_past': False,
    'retries': 0,
}

with DAG('metadados_postgres_dag', default_args=default_args, **dag_args) as dag:
    extracao_metadados_postgres_task = PythonOperator(
        task_id='extracao_metadados_postgres',
        python_callable=extrair_metadados_postgres
    )

    indexacao_metadados_task = PythonOperator(
        task_id='indexacao_metadados',
        python_callable=indexar_metadados
    )

    extracao_metadados_postgres_task >> indexacao_metadados_task
