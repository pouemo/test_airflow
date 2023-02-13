FROM apache/airflow:latest-python3.8

WORKDIR /home

ENV SQLALCHEMY_WARN_20 1

RUN airflow version

COPY ./airflow.cfg /opt/airflow/

COPY ./dags/ /opt/airflow/dags/


