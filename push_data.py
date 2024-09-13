import pandas as pd
from db_operations import create_connection, drop_table_if_exists, create_table_if_not_exists, push_data_to_db


def data_preprocessing(data):
    """
    This function takes raw_data as input and performs data cleaning according to the project requirements
    and also calculates some attributes.
    :param data: The raw data that is read from the csv file
    :return : returns the cleaned data
    """
    data["CRASH DATE"] = pd.to_datetime(data["CRASH DATE"]+ " " +data["CRASH TIME"])
    data = data.drop(data[data["LATITUDE"].isna()].index)
    data = data.drop(data[data["LATITUDE"] == 0].index)
    data = data.drop(data[data["ZIP CODE"].isna()].index)
    data["NUMBER OF KILLS"] = data['NUMBER OF PERSONS KILLED'] + \
                              data['NUMBER OF CYCLIST KILLED'] + \
                              data['NUMBER OF PEDESTRIANS KILLED'] \
                              + data['NUMBER OF MOTORIST KILLED']

    data["NUMBER OF INJURED"] = data["NUMBER OF PERSONS INJURED"] + \
                                data['NUMBER OF PEDESTRIANS INJURED'] + \
                                data['NUMBER OF MOTORIST INJURED'] \
                                + data['NUMBER OF CYCLIST INJURED']

    data['NUMBER OF CASUALTIES'] = data["NUMBER OF KILLS"] + data["NUMBER OF INJURED"]
    columns_to_keep = ['CRASH DATE', 'LATITUDE', 'LONGITUDE', 'ZIP CODE',
                       'NUMBER OF KILLS', 'NUMBER OF INJURED', 'NUMBER OF CASUALTIES', 'BOROUGH']

    data = data[columns_to_keep]
    # Rename columns to match SQL table
    data.columns = ['CRASH_DATE', 'LATITUDE', 'LONGITUDE', 'ZIP_CODE',
                    'NUMBER_OF_KILLS', 'NUMBER_OF_INJURED', 'NUMBER_OF_CASUALTIES', 'BOROUGH']
    return data


if __name__ == "__main__":
    try:
        # Assuming 'data' is loaded from a CSV file for the initial run
        raw_data = pd.read_csv(r"C:\Users\nika\Desktop\final exam q3\Vehicle_Collisions.csv", low_memory=False)
        cleaned_data = data_preprocessing(raw_data)

        # MySQL database connection details
        host_name = "localhost"
        user_name = "root"
        user_password = "nc8121"
        db_name = "nyc_crash_data"

        # Create a connection to the MySQL database
        engine = create_connection(host_name, user_name, user_password, db_name)

        # Drop the table if it exists
        drop_table_if_exists(engine, "crash_data")

        # Create the table
        create_table_if_not_exists(engine, "crash_data")

        # Push cleaned data to the database
        push_data_to_db(cleaned_data, engine)

    except Exception as e:
        print(f"An error occurred: {e}")
        if engine:
            engine.dispose()  # Close the engine to prevent further errors
