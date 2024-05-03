from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

default_args = {
    "owner" : "Andrea",
    "retries": 2,
    "retry_delay": timedelta(minutes = 5)
}

with DAG(
    dag_id = "immo_pipeline",
    default_args = default_args,
    description = "Scrapping immoweb, training pipeline for houses in Belgium",
    start_date = days_ago(1),
    schedule_interval= '@daily'

) as dag:

    today = datetime.now().strftime("%Y%m%d")

    path_params = {
    'scrape_func': "/opt/airflow/ml/1-Scrape/scrape_main.py",
    'links_dated_csv': f"/opt/airflow/ml/0-Resources/links_{today}.csv",
    'raw_dated_csv' :  f"/opt/airflow/ml/0-Resources/raw_{today}.csv",
    'merge_func': "/opt/airflow/ml/2-Merge/merge_csv.py",
    'raw_merged_csv' :  "/opt/airflow/ml/0-Resources/raw_merged.csv",
    'clean_dated_csv' :  f"/opt/airflow/ml/0-Resources/clean_{today}.csv",
    'encoder_pickle' :  "/opt/airflow/ml/0-Resources/encoder.pkl",
    'scaler_pickle' : "/opt/airflow/ml/0-Resources/scaler.pkl",
    'model_dated_pickle' : f"/opt/airflow/ml/0-Resources/model_{today}.pkl",
    'train_func' : "/opt/airflow/ml/3-Train/random_forest.py",
    'metrics_json': "/opt/airflow/ml/0-Resources/metrics.json" 
    }

    task1= BashOperator(
    task_id = "scrape_task",
    bash_command = "python3 {{ params.scrape_func }} --path_raw={{ params.raw_dated_csv }} --path_links={{ params.links_dated_csv }}",
    params=path_params
    )
    task2= BashOperator(
        task_id = "merge_task",
        bash_command = "python3 {{ params.merge_func }} --raw_dated_csv={{ params.raw_dated_csv }} --raw_merged_csv={{ params.raw_merged_csv }}",
        params=path_params
    )
    task3= BashOperator(
        task_id = "train_task",
        bash_command = "python3 {{ params.train_func }} --path_raw={{ params.raw_merged_csv }} --path_clean={{ params.clean_dated_csv }} --path_encoder={{ params.encoder_pickle }} --path_scaler={{ params.scaler_pickle }} --path_model={{ params.model_dated_pickle }} --path_metrics={{ params.metrics_json }}",
        params=path_params
    )

task1>>task2>>task3