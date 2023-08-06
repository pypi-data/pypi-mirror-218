r"""Submodule create.py includes the following functions:

- **create_warehouse** - creates a warehouse in Snowflake if it does not already exist

- **create_database** - creates a database in Snowflake if it does not already exist

- **create_schema** - creates a schema in Snowflake if it does not already exist

"""


import snowflake.connector
from .utils import get_snowflake_connection


def create_warehouse(
    conn: snowflake.connector.connection.SnowflakeConnection = get_snowflake_connection(),
    warehouse_name: str = "tiny_warehouse_mg",
):
    """
    Creates a warehouse in Snowflake if it does not already exist.

    Parameters
    ----------
    conn : snowflake.connector.connection.SnowflakeConnection
        A connection to Snowflake
    warehouse_name : str
        The name of the warehouse to create

    Returns
    -------
    None : None

    """
    cs = conn.cursor()
    _ = cs.execute(f"CREATE WAREHOUSE IF NOT EXISTS {warehouse_name}")
    cs.close()


def create_database(
    conn: snowflake.connector.connection.SnowflakeConnection = get_snowflake_connection(),
    database_name: str = "mydb",
):
    """
    Creates a database in Snowflake if it does not already exist.

    Parameters
    ----------
    conn : snowflake.connector.connection.SnowflakeConnection
        A connection to Snowflake
    database_name : str
        The name of the database to create

    Returns
    -------
    None : None

    """
    cs = conn.cursor()
    _ = cs.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
    cs.close()


def create_schema(
    conn: snowflake.connector.connection.SnowflakeConnection = get_snowflake_connection(),
    schema_name: str = "myschema",
):
    """
    Creates a schema in Snowflake if it does not already exist.

    Parameters
    ----------
    conn : snowflake.connector.connection.SnowflakeConnection
        A connection to Snowflake
    schema_name : str
        The name of the schema to create

    Returns
    -------
    None : None

    """
    cs = conn.cursor()
    _ = cs.execute(f"CREATE SCHEMA IF NOT EXISTS {schema_name}")
    cs.close()
