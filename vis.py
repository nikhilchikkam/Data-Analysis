import pandas as pd
from sqlalchemy import create_engine, inspect
import matplotlib.pyplot as plt


def create_connection(host_name, user_name, user_password, db_name):
    """Create a database connection."""
    connection_str = f"mysql+pymysql://{user_name}:{user_password}@{host_name}/{db_name}"
    engine = create_engine(connection_str)
    return engine


def get_table_columns(engine, table_name):
    """Fetch the column names of a table."""
    inspector = inspect(engine)
    columns = [column['name'] for column in inspector.get_columns(table_name)]
    return columns


def fetch_day_of_week_data(engine):
    query = """
    SELECT 
        `CRASH_DATE`
    FROM 
        `crash_data`
    WHERE 
        `CRASH_DATE` BETWEEN '2019-01-01' AND '2020-10-31' AND `BOROUGH` = 'BROOKLYN';
    """
    return pd.read_sql(query, engine)


def fetch_hourly_crash_data(engine):
    query = """
    SELECT 
        `CRASH_DATE`
    FROM 
        `crash_data`
    WHERE 
        `CRASH_DATE` BETWEEN '2019-01-01' AND '2020-10-31'
        AND `BOROUGH` = 'BROOKLYN';
    """
    return pd.read_sql(query, engine)


def analyze_day_of_the_week(data):
    """
    Analyze and plot crashes by day of the week.
    """
    data['CRASH_DATE'] = pd.to_datetime(data['CRASH_DATE'])
    data['YEAR'] = data['CRASH_DATE'].dt.year
    data['DAY_OF_WEEK'] = data['CRASH_DATE'].dt.day_name()

    # Filter data for 2019 and 2020
    data = data[data['YEAR'].isin([2019, 2020])]

    # Group by year and day of the week
    daily_crashes = data.groupby(['DAY_OF_WEEK', 'YEAR']).size().unstack()

    # Reorder the days for plotting
    ordered_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    daily_crashes = daily_crashes.reindex(ordered_days)

    # Plot
    daily_crashes.plot(kind='bar', figsize=(15, 8))
    plt.xlabel('Day of the Week')
    plt.ylabel('Number of Crashes')
    plt.title('Brooklyn - Day of the Week Crash Comparison (2019 vs 2020)')
    plt.legend(title='Year')
    plt.show()


def analyze_hourly_crashes(data):
    """
    Analyze and plot crashes by hour of the day.
    """
    data['CRASH_DATE'] = pd.to_datetime(data['CRASH_DATE'])
    if data['CRASH_DATE'].dt.hour.isnull().all():
        print("The CRASH_DATE column does not contain time information.")
        return

    data['HOUR'] = data['CRASH_DATE'].dt.hour

    # Extract the year and hour
    data['YEAR'] = data['CRASH_DATE'].dt.year

    # Filter data for 2019 and 2020
    data = data[data['YEAR'].isin([2019, 2020])]

    # Group by hour
    hourly_crashes = data.groupby('HOUR').size()

    # Plot
    hourly_crashes.plot(kind='bar', figsize=(15, 8))
    plt.xlabel('Hour of Day')
    plt.ylabel('Number of Crashes')
    plt.title('Brooklyn - Hourly Crash Comparison')
    plt.xticks(range(0, 24), range(0, 24))  # Setting x-ticks to show every hour
    plt.show()


if __name__ == "__main__":
    # MySQL database connection details
    host_name = "localhost"
    user_name = "root"
    user_password = "nc8121"
    db_name = "nyc_crash_data"

    # Create a connection to the MySQL database
    engine = create_connection(host_name, user_name, user_password, db_name)

    # Check column names
    table_columns = get_table_columns(engine, 'crash_data')
    print("Columns in 'crash_data' table:", table_columns)

    # Fetch data
    if 'CRASH_DATE' in table_columns:
        day_of_week_data = fetch_day_of_week_data(engine)
        analyze_day_of_the_week(day_of_week_data)
        hourly_crash_data = fetch_hourly_crash_data(engine)
        analyze_hourly_crashes(hourly_crash_data)
    else:
        print("'CRASH_DATE' column not found in 'crash_data' table.")
