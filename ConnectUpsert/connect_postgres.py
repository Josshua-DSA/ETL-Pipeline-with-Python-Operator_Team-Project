from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow import DAG

def create_weather_table(pg_conn_id: str = "postgres_default", dag: DAG = None):
    query = """
        CREATE TABLE IF NOT EXISTS weather_hourly (
            "ts" TIMESTAMP PRIMARY KEY,
            "temperature" NUMERIC,
            "rain" NUMERIC,
            "source_file" TEXT,
            "batch_id" TEXT
        );
    """
    return SQLExecuteQueryOperator(
        task_id="create_weather_table",
        sql=query,
        postgres_conn_id=pg_conn_id,
        autocommit=True,
        dag=dag
    )

def create_weather_temp_table(pg_conn_id: str = "postgres_default", dag: DAG = None):
    query = """
        DROP TABLE IF EXISTS weather_temp;
        CREATE TABLE weather_temp (
            "ts" TIMESTAMP PRIMARY KEY,
            "temperature" NUMERIC,
            "rain" NUMERIC,
            "source_file" TEXT,
            "batch_id" TEXT
        );
    """
    return SQLExecuteQueryOperator(
        task_id="create_weather_temp_table",
        sql=query,
        postgres_conn_id=pg_conn_id,
        autocommit=True,
        dag=dag
    )

def merge_data(pg_conn_id: str = "postgres_default", dag: DAG = None):
    query = """
        INSERT INTO weather_hourly
        SELECT *
        FROM (
            SELECT DISTINCT *
            FROM weather_temp
        ) t
        ON CONFLICT ("ts") DO UPDATE
        SET
            "temperature" = excluded."temperature",
            "rain" = excluded."rain",
            "source_file" = excluded."source_file",
            "batch_id" = excluded."batch_id";
    """
    return SQLExecuteQueryOperator(
        task_id="merge_data",
        sql=query,
        postgres_conn_id=pg_conn_id,
        autocommit=True,
        dag=dag
    )
