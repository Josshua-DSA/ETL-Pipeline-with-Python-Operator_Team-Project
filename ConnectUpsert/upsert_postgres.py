from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow import DAG

def upsert_data_to_postgres(pg_conn_id: str = "postgres_default", table: str = "weather_hourly", dag: DAG = None) -> SQLExecuteQueryOperator:
    """
    Melakukan UPSERT ke tabel PostgreSQL menggunakan query INSERT ... ON CONFLICT.
    Jika terjadi konflik pada kolom primary key, data yang ada akan diperbarui.
    """

    # SQL query untuk UPSERT menggunakan INSERT ... ON CONFLICT
    query = f"""
        INSERT INTO {table}
        SELECT *
        FROM weather_temp
        ON CONFLICT ("ts") 
        DO UPDATE
        SET
            "temperature" = excluded."temperature",
            "rain" = excluded."rain",
            "source_file" = excluded."source_file",
            "batch_id" = excluded."batch_id";
    """

    # Menggunakan SQLExecuteQueryOperator untuk mengeksekusi query
    return SQLExecuteQueryOperator(
        task_id="upsert_data_to_postgres",
        sql=query,
        postgres_conn_id=pg_conn_id,
        autocommit=True,
        dag=dag
    )
