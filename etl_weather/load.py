from __future__ import annotations
from pathlib import Path
import pandas as pd
from airflow.providers.postgres.hooks.postgres import PostgresHook
from ConnectUpsert.connect_postgres import create_weather_table, create_weather_temp_table, merge_data
from ConnectUpsert.upsert_postgres import upsert_data_to_postgres
from sqlalchemy import Table, MetaData


# Fungsi untuk menyimpan ke CSV (Backup atau Audit)
def load_to_csv(records: list[dict], out_path: str | Path = "data/staging/staging_weather_data.csv") -> str:
    """
    Simpan records hasil transform ke CSV.
    """
    dst = Path(out_path)
    dst.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame.from_records(records or []).to_csv(dst, index=False)
    return str(dst)

# Fungsi untuk memuat data ke PostgreSQL (UPSERT)
def load_to_postgres(records: list[dict], table: str = "public.weather_hourly", pg_conn_id: str = "postgres_default", dag=None) -> str:
    """
    Memuat data ke Postgres dengan UPSERT.
    """
    # Memanggil fungsi create_weather_table dan create_weather_temp_table
    create_weather_table(pg_conn_id=pg_conn_id, dag=dag)
    create_weather_temp_table(pg_conn_id=pg_conn_id, dag=dag)
    
    # Memanggil merge_data untuk melakukan UPSERT ke PostgreSQL
    merge_data(pg_conn_id=pg_conn_id, dag=dag)
    
    return f"Data successfully loaded and merged into {table}"