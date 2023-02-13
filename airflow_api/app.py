import time
import json
import subprocess
import datetime
from datetime import datetime
from random import randint

from flask import Flask, jsonify
from pathlib import Path

import time
from airflow_client import client
from airflow_client.client.api import dag_run_api
from airflow_client.client.api.task_instance_api import TaskInstanceApi
from airflow_client.client.model.dag_run import DAGRun
from airflow_client.client.model.error import Error
from pprint import pprint

app = Flask(__name__)

configuration = client.Configuration(
        host = "http://localhost:8080/api/v1",
        username = 'airflow',
        password = 'airflow'
    )

@app.route('/')
@app.route('/trigger_dag')
def trigger_dag():
    """
    """

    with client.ApiClient(configuration) as api_client:
    # Create an instance of the API class

        api_instance = dag_run_api.DAGRunApi(api_client)
        dag_id = "celery_executor_kill" # str | The DAG ID.
        dag_run = DAGRun(
            dag_run_id=str(randint(0, 100000000)),
            #logical_date=dateutil_parser('1970-01-01T00:00:00.00Z'),
            #execution_date=dateutil_parser('1970-01-01T00:00:00.00Z'),
            #state=DagState("queued"),
        ) # DAGRun | 

        # example passing only required values which don't have defaults set
        try:
            # Trigger a new DAG run
            api_response = api_instance.post_dag_run(dag_id, dag_run)
            pprint(type(api_response) )
            dag_run ={
                'dag_id': api_response.dag_id,
                'dag_run_id': api_response.dag_run_id ,
                'data_interval_end': str(api_response.data_interval_end),
                'data_interval_start': str(api_response.data_interval_start),
                'end_date': None,
                'execution_date': str(api_response.execution_date),
                'external_trigger': True,
                'last_scheduling_decision': None,
                'logical_date': str(api_response.logical_date),
                'run_type': api_response.run_type,
                'start_date': str(api_response.start_date),
                'state': str(api_response.state)
            }
            return  jsonify({'dag_run': json.dumps(dag_run, ensure_ascii=False, skipkeys=True, indent= 4)})
        except client.ApiException as e:
            print("Exception when calling DAGRunApi->post_dag_run: %s\n" % e)

        return jsonify({'status': 'ok'})


@app.route('/param/<id>', methods=['GET'])
def test_airflow_with_params(id):

    with client.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = dag_run_api.DAGRunApi(api_client)
        dag_id = "celery_executor_kill" # str | The DAG ID.
        state = ["failed",  "upstream_failed", "success"]

        task_instance_api = TaskInstanceApi(api_client=api_client)
        task_instances = task_instance_api.get_task_instances(dag_id=dag_id, dag_run_id= id, state=state)

        pprint(task_instances)

        
    return jsonify({'workflow': "toto"})

    

    


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
