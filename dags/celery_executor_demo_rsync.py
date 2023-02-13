from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import time
from random import randint
import subprocess

import settings


	
def rsync_first_step(**kwargs):
    print('first step')
    ran_int = randint(1, 10)
    
    print('ran_int === %d' % ran_int)
    if ran_int % 2:
    	time.sleep(5)
    	print(settings.NUM_RETRY_STEP_1)
    	print("****************************\n")
    else:
    	raise Exception("Fail in first function")
    	

def rsync_second_step(**kwargs):
    print('Second step ')
    
    ran_int = randint(1, 10)
    print('ran_int === %d' % ran_int)
    if ran_int % 2:
    	time.sleep(5)
    	print(settings.NUM_RETRY_STEP_2)
    	print("****************************\n")
    else:
    	raise Exception("Fail in second function")
    	
def rsync_third_step(**kwargs):
    print('Third step ')
    
    ran_int = randint(1, 10)
    print('ran_int === %d' % ran_int)
    if ran_int % 2:
    	time.sleep(5)
    else:
    	print(settings.NUM_RETRY_STEP_3)
    	print("****************************\n")
    	raise Exception("Fail in third function")

with DAG(
    dag_id="celery_executor_demo_rsync",
    start_date=datetime(2023,1,1),
    schedule_interval="@once",
    catchup=False) as dag:
    
    print(dag)
    
    print(settings.NUM_RETRY_STEP_1)
    
    task1=PythonOperator(task_id="step1", python_callable=rsync_first_step, provide_context=True,  retries=settings.NUM_RETRY_STEP_1, retry_delay=5)
  
    task2=PythonOperator(task_id="step_2", python_callable=rsync_second_step, provide_context=True, retries=0, retry_delay=5)
    
    task3=PythonOperator(task_id="step_3", python_callable=rsync_third_step, provide_context=True, retries=0, retry_delay=5)
    
    task1 >> task2 >> task3
    
    
