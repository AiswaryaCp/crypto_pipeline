# Crypto Data Pipeline

This project fetches cryptocurrency prices and stores them in AWS S3 using Apache Airflow.

## Architecture
- **Source:** CoinGecko API
- **Orchestration:** Apache Airflow
- **Storage:** AWS S3
- **Language:** Python 3.12

## Project Structure
- `dags/`: contains the Airflow DAG definitions.
- `requirements.txt`: Python dependencies.
- `.gitignore`: Files excluded from version control.

## Setup Instructions
1. Clone the repo: `git clone <url>`
2. Create environment: `python -m venv env`
3. Install dependencies: `pip install -r requirements.txt`
4. Set up Airflow: `airflow db migrate`
