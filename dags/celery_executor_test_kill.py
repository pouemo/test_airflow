from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import time
from random import randint
import subprocess

import settings


	
def rsync_first_step(**kwargs):
    print('first step')
    time.sleep(60)
    	

def rsync_second_step(**kwargs):
    print('Second step ')
    
    time.sleep(60)
    	

with DAG(
    dag_id="celery_executor_kill",
    start_date=datetime(2023,1,1),
    schedule_interval="@once",
    catchup=False) as dag:
    
    print(dag)
    
    print(settings.NUM_RETRY_STEP_1)
    
    task1=PythonOperator(task_id="step1", python_callable=rsync_first_step, provide_context=True,  retries=settings.NUM_RETRY_STEP_1, retry_delay=5)
  
    task2=PythonOperator(task_id="step_2", python_callable=rsync_second_step, provide_context=True, retries=0, retry_delay=5)
    
    task1 >> task2
    
    
