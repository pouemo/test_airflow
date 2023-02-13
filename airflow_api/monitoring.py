import logging
import json
import time
from airflow_client import client
from airflow_client.client.api import dag_run_api
from pprint import pprint

API = ""

def get_sleep() -> int:
    """
    Fetches period to wait before lauching next monitor process
    : return :
    """

    return 5

def monitor():
    """
    Fetches failed dag run and return them
    """

    configuration = client.Configuration(
        host = "http://localhost:8080/api/v1",
        username = 'airflow',
        password = 'airflow'
    )

    with client.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = dag_run_api.DAGRunApi(api_client)
        dag_id = "celery_executor_kill" # str | The DAG ID.
        state = ["running"]
        order_by = "start_date"
        limit = 100 # int | The numbers of items to return. (optional) if omitted the server will use the default value of 100
        offset = 0 # int | The number of items to skip before starting to collect the result set. (optional)
        # execution_date_gte = time.dateutil_parser('1970-01-01T00:00:00.00Z')

        while True:
            print("\n Locking for running dag .... \n")

            try:
            # List DAG runs
                api_response = api_instance.get_dag_runs(dag_id, limit=limit, offset=offset, state=state, order_by=order_by)
                pprint(api_response)
            except client.ApiException as e:
                print("Exception when calling DAGRunApi->get_dag_runs: %s\n" % e)
            time.sleep(get_sleep())

if __name__ == '__main__':
    monitor()