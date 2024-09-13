import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError


def create_connection(host_name, user_name, user_password, db_name):
    try:
        # Connect to the MySQL server
        engine = create_engine(f'mysql+mysqlconnector://{user_name}:{user_password}@{host_name}')
        with engine.connect() as connection:
            # Create the database if it doesn't exist
            connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name}"))

        # Connect to the specific database
        engine = create_engine(f'mysql+mysqlconnector://{user_name}:{user_password}@{host_name}/{db_name}')
        print("MySQL Database connection successful and database ensured")
    except SQLAlchemyError as e:
        print(f"The error '{e}' occurred")
    return engine


def drop_table_if_exists(engine, table_name):
    drop_table_query = f"DROP TABLE IF EXISTS {table_name};"
    try:
        with engine.connect() as connection:
            connection.execute(text(drop_table_query))
            print(f"Table {table_name} dropped successfully")
    except SQLAlchemyError as e:
        print(f"The error '{e}' occurred while dropping the table")


def create_table_if_not_exists(engine, table_name):
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        CRASH_DATE DATETIME,
        LATITUDE FLOAT,
        LONGITUDE FLOAT,
        ZIP_CODE VARCHAR(255),
        NUMBER_OF_KILLS INT,
        NUMBER_OF_INJURED INT,
        NUMBER_OF_CASUALTIES INT,
        BOROUGH VARCHAR(255)
    );
    """
    with engine.connect() as connection:
        connection.execute(text(create_table_query))


def push_data_to_db(data, engine, table_name="crash_data"):
    """
    Pushes data into MySQL database in smaller chunks
    :param data: The data to be pushed
    :param engine: The SQLAlchemy engine object
    :param table_name: The table name
    """
    chunk_size = 10000  # Define a chunk size
    try:
        with engine.begin() as connection:  # Use begin to start a transaction
            for start in range(0, len(data), chunk_size):
                end = start + chunk_size
                chunk = data.iloc[start:end]
                chunk.to_sql(table_name, con=connection, if_exists='append', index=False)
                print(f"Pushed rows {start} to {end} to {table_name}")
        print(f"Data pushed to {table_name} successfully")
    except SQLAlchemyError as e:
        print(f"The error '{e}' occurred")
        engine.dispose()  # Close the engine to prevent further errors


def pull_data_from_db(engine, table_name="crash_data"):
    """
    Pulls data from MySQL database
    :param engine: The SQLAlchemy engine object
    :param table_name: The table name
    :return : returns the data from database
    """
    query = f"SELECT * FROM {table_name}"
    try:
        with engine.connect() as connection:
            data = pd.read_sql(query, connection)
        return data
    except SQLAlchemyError as e:
        print(f"The error '{e}' occurred")
        return pd.DataFrame()  # Return an empty DataFrame in case of error
