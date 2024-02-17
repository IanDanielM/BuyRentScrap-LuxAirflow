from datetime import datetime
from main import get_data, load_data

from airflow import DAG
from airflow.operators.python_operator import PythonOperator


default_args = {
    'owner': 'LuxAcademy',
    'start_date': datetime(2020, 1, 1),
    'retries': 3,
}



with DAG('extract_dag', default_args=default_args, schedule_interval='@daily') as dag:
    task1 = PythonOperator(
        task_id='extract_data',
        python_callable=get_data,
        op_args=["https://www.buyrentkenya.com/property-for-rent"],
    )

    task2 = PythonOperator(
        task_id='load_data',
        python_callable=load_data,
        op_args=[task1.output, "houses_for_rent.csv"],
    )

    task1 >> task2