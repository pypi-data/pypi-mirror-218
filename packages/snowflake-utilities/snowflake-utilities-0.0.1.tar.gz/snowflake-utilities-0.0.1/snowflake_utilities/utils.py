r"""Submodule utils.py includes the following functions:

- **get_snowflake_connection** - returns a connection to Snowflake

- **check_resource_viable** - checks if a resource type is viable (i.e. is the string a resource type in Snowflake)

- **print_resources** - prints the resources in Snowflake

"""

import os
import snowflake.connector
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())


def get_snowflake_connection():
    """
    Returns a connection to Snowflake. Assuming the following environment variables are set:
    SNOWFLAKE_USERNAME - the username
    SNOWFLAKE_PASSWORD - the password
    SNOWFLAKE_ACCOUNT - the account name (the beginning of the URL when you log in to Snowflake)

    Parameters
    ----------
    None : None

    Returns
    -------
    conn : snowflake.connector.connection.SnowflakeConnection
        A connection to Snowflake

    """

    conn = snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USERNAME"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
    )
    return conn


def check_resource_viable(resource_type: str = "WAREHOUSES"):
    """
    Checks if a resource type is viable (i.e. it is not a table).

    Parameters
    ----------
    resource_type : str
        The type of resource to check

    Returns
    -------
    is_viable : bool
        True if the resource type is viable, False otherwise

    """
    viable_resource_types = [
        "WAREHOUSE",
        "DATABASE",
        "SCHEMA",
        "TABLE",
        "WAREHOUSES",
        "DATABASES",
        "SCHEMAS",
        "TABLES",
    ]
    is_viable = resource_type in viable_resource_types

    if not is_viable:
        raise ValueError(
            f"Resource type {resource_type} is not viable. Please choose from {viable_resource_types}"
        )


def print_resources(
    conn: snowflake.connector.connection.SnowflakeConnection = get_snowflake_connection(),
    resource_type: str = "WAREHOUSES",
):
    """
    Prints the list of resources of a given type in Snowflake.

    Parameters
    ----------
    conn : snowflake.connector.connection.SnowflakeConnection
        A connection to Snowflake
    resource_type : str
        The type of resource to print (e.g. WAREHOUSES, DATABASES, SCHEMAS, TABLES)

    Returns
    -------
    all_rows : list
        A list of all rows returned by the query

    """
    check_resource_viable(resource_type=resource_type)

    cs = conn.cursor()
    cs.execute(f"SHOW {resource_type}")
    all_rows = cs.fetchall()
    _ = [print(row) for row in all_rows]
    cs.close()
    return all_rows
