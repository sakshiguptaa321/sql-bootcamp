from pathlib import Path
import os

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL


def find_repo_root(start: Path) -> Path:
    for path in [start, *start.parents]:
        if (path / '.env').exists() or (path / 'pyproject.toml').exists():
            return path
    return start


@st.cache_resource(show_spinner=False)
def get_engine():
    repo_root = find_repo_root(Path(__file__).resolve())
    load_dotenv(repo_root / '.env')
    connection_url = URL.create(
        'oracle+oracledb',
        username=os.environ['ORACLE_USER'],
        password=os.environ['ORACLE_PASSWORD'],
        host=os.getenv('ORACLE_HOST', 'localhost'),
        port=int(os.getenv('ORACLE_PORT', '1522')),
        query={'service_name': os.getenv('ORACLE_SERVICE_NAME', 'FREEPDB1')},
    )
    return create_engine(connection_url, pool_pre_ping=True)


@st.cache_data(ttl=300, show_spinner=False)
def run_query(query: str, params: dict | None = None) -> pd.DataFrame:
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql(text(query), conn, params=params or {})
