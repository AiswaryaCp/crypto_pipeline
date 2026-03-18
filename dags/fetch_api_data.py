import requests
import pandas as pd
import boto3
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator


def fetch_and_upload():
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd"
    data = requests.get(url).json()

    df = pd.DataFrame(data)
    print(df.head())

    csv_file_name = f"crypto_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(csv_file_name, index=False)

    s3 = boto3.client('s3')
    s3.upload_file(csv_file_name, "coin-crypto-data", csv_file_name)

with DAG(
    dag_id="fetch_api_data",
    start_date=datetime(2024, 1, 1),
    schedule="30 10 * * *",
    catchup=False
) as dag:
    upload_task = PythonOperator(
        task_id="fetch_api_and_upload_s3",
        python_callable=fetch_and_upload
    )

    upload_task
