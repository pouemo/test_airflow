from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import time

def hello_function():
    print('Hello, this is the first task of the DAG')
    time.sleep(5)
	
def last_function():
    print('DAG run is done.')

def sleeping_function():
    print("Sleeping for 5 seconds")
    time.sleep(5)

with DAG(
    dag_id="celery_executor_demo",
    start_date=datetime(2021,1,1),
    schedule_interval="@hourly",
    catchup=False) as dag:
    
    task1=PythonOperator(task_id="start", python_callable=hello_function)
  
    task2_1=PythonOperator(task_id="sleepy_1", python_callable=sleeping_function)
    
    task2_2=PythonOperator(task_id="sleepy_2", python_callable=sleeping_function)
    
    task2_3=PythonOperator(task_id="sleepy_3", python_callable=sleeping_function)
	    
    # Other 11 tasks are the same as task2_1 except for their task_id.
	# You can refer to the link below for reference
	
	# subprocess.call(['rsync', '-avz', '--min-size=0', '--include=*.txt', SRC_DIR_1, SRC_DIR_2 ])
	
    task6=PythonOperator(task_id="end", python_callable=last_function)
    
    task1 >> [task2_1, task2_2, task2_3] >> task6
