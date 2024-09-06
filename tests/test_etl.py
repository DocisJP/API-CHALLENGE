import pytest
import pandas as pd
from etl.utils import create_db_engine, read_csv, validate_schema, handle_null_values
from sqlalchemy import text, Table, Column, Integer, String, MetaData

def test_create_db_engine(test_db_url):
    engine = create_db_engine({"url": test_db_url})
    assert engine is not None

def test_read_csv(tmp_path):
    d = tmp_path / "test_data"
    d.mkdir()
    test_csv = d / "test.csv"
    test_csv.write_text("id,name\n1,Test Name")

    df = read_csv(test_csv)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    assert list(df.columns) == ['id', 'name']

def test_validate_schema(test_engine):
    metadata = MetaData()
    Table('departments', metadata,
          Column('id', Integer, primary_key=True),
          Column('department', String))
    metadata.create_all(test_engine)

    df = pd.DataFrame({'id': [1], 'department': ['Test']})
    validated_df = validate_schema(df, 'departments', test_engine)
    assert list(validated_df.columns) == ['id', 'department']

def test_handle_null_values():
    df = pd.DataFrame({'id': [1, None], 'department': ['Test', None]})
    handled_df = handle_null_values(df, 'departments')
    assert handled_df['id'].isnull().sum() == 0
    assert handled_df['department'].isnull().sum() == 0

def test_postgres_specific_features(test_engine):
    with test_engine.connect() as conn:
        result = conn.execute(text("SELECT EXTRACT(YEAR FROM TIMESTAMP '2021-01-01 00:00:00')")).scalar()
        assert result == 2021