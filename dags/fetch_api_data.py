import requests
import pandas as pd
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook


def fetch_and_upload(ds):
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd"
    response = requests.get(url)
    data = response.json()
    
    df = pd.DataFrame(data)
    local_file_path = f"/tmp/crypto_data_{ds}.csv"
    df.to_csv(local_file_path, index=False)
    
    print(f"DEBUG: File created at {local_file_path}")

    s3_hook = S3Hook(aws_conn_id='aws_default')
    
    s3_hook.load_file(
        filename=local_file_path,
        key=f"coingecko/{ds}/crypto_data.csv",
        bucket_name="coin-crypto-data",
        replace=True
    )

with DAG(
    dag_id="fetch_api_data",
    start_date=datetime(2026, 1, 1),
    schedule="30 10 * * *",
    catchup=False
) as dag:
    upload_task = PythonOperator(
        task_id="fetch_api_and_upload_s3",
        python_callable=fetch_and_upload
    )

    upload_task