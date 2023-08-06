r"""Submodule upload.py includes the following functions:

- **upload_pandas_df_to_snowflake** - uploads a Pandas DataFrame to Snowflake

"""


import os
import pandas as pd
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine


def upload_pandas_df_to_snowflake(
    data: pd.DataFrame = pd.DataFrame(),
    warehouse_name: str = "tiny_warehouse_mg",
    database_name: str = "mydb",
    schema_name: str = "myschema",
    table_name: str = "mytable",
    if_exists: str = "replace",
):
    """
    Uploads a Pandas DataFrame to Snowflake.

    Parameters
    ----------
    data : pd.DataFrame
        The Pandas DataFrame to upload
    warehouse_name : str
        The name of the warehouse to use
    database_name : str
        The name of the database to use in Snowflake
    schema_name : str
        The name of the schema to use in Snowflake
    table_name : str
        The name of the table to use in Snowflake
    if_exists : str
        The action to take if the table already exists in Snowflake
        Options are 'fail', 'replace', 'append'

    Returns
    -------
    new_df : pd.DataFrame
        The Pandas DataFrame that was pulled from Snowflake following the upload

    """
    engine = create_engine(
        URL(
            account=os.getenv("SNOWFLAKE_ACCOUNT"),
            user=os.getenv("SNOWFLAKE_USERNAME"),
            password=os.getenv("SNOWFLAKE_PASSWORD"),
            database=database_name,
            schema=schema_name,
            warehouse=warehouse_name,
        )
    )

    with engine.connect() as conn, conn.begin():
        data.to_sql(table_name, conn, if_exists=if_exists, index=False)
        new_df = pd.read_sql(f"SELECT * FROM {table_name}", conn)

    engine.dispose()

    return new_df