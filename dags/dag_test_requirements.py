from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator


default_args = {
    'owner': 'Andrea',
    'retry': 5,
    'retry_delay': timedelta(minutes=5)
}


def check__sklearn():
    import sklearn
    print(f"sklearn with version: {sklearn.__version__} ")


def check__pandas():
    import pandas
    print(f"pandas with version: {pandas.__version__}")

def check__plotly():
    import plotly
    print(f"plotly with version: {plotly.__version__}")

def check__streamlit():
    import streamlit
    print(f"streamlit with version: {streamlit.__version__}")

def check__streamlit_extra():
    import streamlit_extras
    print(f"streamlit-extras imported")

def check__beautifulsoup():
    from bs4 import BeautifulSoup
    print(f"BeautifulSoup imported")

def check_click():
    import click
    print(f"Click imported")

def check_requests():
    import requests
    print(f"Requests imported")

def check_joblib():
    import joblib
    print(f"joblib imported")





with DAG(
    default_args=default_args,
    dag_id="dag_python_dependencies_v08",
    start_date=datetime(2024, 4, 29),
    schedule_interval='@daily'
) as dag:
    task1 = PythonOperator(
        task_id='check__sklearn',
        python_callable=check__sklearn
    )
    
    task2 = PythonOperator(
        task_id='check__pandas',
        python_callable=check__pandas
    )

    task3 = PythonOperator(
        task_id='check__plotly',
        python_callable=check__plotly

    )
    task4 = PythonOperator(
        task_id='check__streamlit',
        python_callable=check__streamlit
    )
    task5 = PythonOperator(
        task_id='check__streamlit_extra',
        python_callable=check__streamlit_extra
    )
    task6 = PythonOperator(
        task_id='check__beautifulsoup',
        python_callable=check__beautifulsoup
    )
    task7= PythonOperator(
        task_id = "check_click",
        python_callable = check_click
    )
    task8= PythonOperator(
        task_id = "check_requests",
        python_callable = check_requests
    )
    task9= PythonOperator(
        task_id = "check_joblib",
        python_callable = check_joblib
    )

    task1 >> task2 >> task3 >> task4 >> task5 >> task6 >> task7 >> task8 >> task9