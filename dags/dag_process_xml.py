
from datetime import timedelta
from datetime import datetime
import json

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from python_code.process_xml import process_xml_file

config = open("/opt/airflow/dags/config/config.json",'r')
config = json.loads(config.read())
root_path = config['root_path']
file_path = config['file_path']

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
}

with DAG(
    'coding_challenge',
    default_args=default_args,
    schedule_interval=None,
    start_date=datetime(1997,9,16),
    tags=['challenger'],
) as dag:

    t1 = PythonOperator(
        task_id='process_xml',
        python_callable=process_xml_file,
        op_args=[root_path+file_path, config['neo4j']['host'], config['neo4j']['port']]
    )

    t1
