import pandas as pd
import matplotlib.pyplot as plt # package to plot the graphs
import folium # package to generate interactive heatmaps.
from folium.plugins import HeatMap # package to create heatmaps

def zipcode_compare(Q2019, Q2020):
    """
    This function takes two dataframes as inputs and finds the value counts of the zip code and plots the top 10 zipcode with
    highest crashes.

    """
    # zip code comparison on 2019 2020 Queens borough
    zipsc19 = Q2019["ZIP CODE"].value_counts()[:10].to_frame(name="Crashes in 2019").reset_index()
    zipsc20 = Q2020["ZIP CODE"].value_counts()[:10].to_frame(name="Crashes in 2020").reset_index()
    merged_df = pd.merge(zipsc19, zipsc20, on='ZIP CODE', how='inner')
    merged_df.set_index("ZIP CODE", inplace=True)
    merged_df.plot(kind="bar")
    plt.title("Zipcode with most crashes in 2019 vs 2020")
    plt.xlabel("Zipcodes")
    plt.ylabel("Number of Crashes")
    plt.show()

    data = Q2019[Q2019["ZIP CODE"] == 11434.0]
    nyc_map_19 = folium.Map(location=[40.7128, -74.0060], zoom_start=10)
    heat_data_19 = [[row['LATITUDE'], row['LONGITUDE']] for index, row in data.iterrows()]
    HeatMap(heat_data_19).add_to(nyc_map_19)
    nyc_map_19.save('ZIPCODE2019_heatmap.html')  # Save the map as an HTML file

    data = Q2020[Q2020["ZIP CODE"] == 11385.0]
    nyc_map_20 = folium.Map(location=[40.7128, -74.0060], zoom_start=10)
    heat_data_20 = [[row['LATITUDE'], row['LONGITUDE']] for index, row in data.iterrows()]
    HeatMap(heat_data_20).add_to(nyc_map_20)
    nyc_map_20.save('ZIPCODE2020_heatmap.html')


def street_compare(Q2019, Q2020):
    """
    This function takes two dataframes as input and finds value counts for the ON street name and
    plot the bar plot for the top 10 streets
    """
    # street comparision 2019 2020 Queens borough
    ons_19 = Q2019["ON STREET NAME"].value_counts()[:10].to_frame(name="Crashes in 2019").reset_index()
    ons_20 = Q2020["ON STREET NAME"].value_counts()[:10].to_frame(name="Crashes in 2020").reset_index()
    merged_df = pd.merge(ons_19, ons_20, on='ON STREET NAME', how='inner')
    merged_df.set_index("ON STREET NAME", inplace=True)
    merged_df.plot(kind="bar")
    plt.title("ON Street with most crashes in 2019 vs 2020")
    plt.xlabel("Street names ")
    plt.ylabel("Number of Crashes")
    plt.show()

    for i, row in ons_19.iterrows():
        print(row[0])
        nyc_map_s19 = folium.Map(location=[40.7128, -74.0060], zoom_start=10)
        d = Q2019[Q2019["ON STREET NAME"] == row[0]]
        heat_data = [[row['LATITUDE'], row['LONGITUDE']] for index, row in d.iterrows()]
        HeatMap(heat_data).add_to(nyc_map_s19)
        nyc_map_s19.save('STREET19_heatmap.html')  # Save the map as an HTML file
        break

    for i, row in ons_20.iterrows():
        print(row[0])
        nyc_map_s20 = folium.Map(location=[40.7128, -74.0060], zoom_start=10)
        d = Q2020[Q2020["ON STREET NAME"] == row[0]]
        heat_data = [[row['LATITUDE'], row['LONGITUDE']] for index, row in d.iterrows()]
        HeatMap(heat_data).add_to(nyc_map_s20)
        nyc_map_s20.save('STREET20_heatmap.html')  # Save the map as an HTML file
        break


def analyze_contributing_factors(Q2019, Q2020):
    """
    The function takes two dataframes as inputs and merges the required columns and finds value counts
    and plots the top 10 contributing factors as PIE chart
    """
    # Concatenate all values in each row into a single string
    merged_values_all_rows19 = Q2019[
        ['CONTRIBUTING FACTOR VEHICLE 1', 'CONTRIBUTING FACTOR VEHICLE 2', 'CONTRIBUTING FACTOR VEHICLE 3', \
         'CONTRIBUTING FACTOR VEHICLE 4', 'CONTRIBUTING FACTOR VEHICLE 5'
         ]].astype(str).apply('_'.join, axis=1)

    merged_values_all_rows20 = Q2020[
        ['CONTRIBUTING FACTOR VEHICLE 1', 'CONTRIBUTING FACTOR VEHICLE 2', 'CONTRIBUTING FACTOR VEHICLE 3', \
         'CONTRIBUTING FACTOR VEHICLE 4', 'CONTRIBUTING FACTOR VEHICLE 5'
         ]].astype(str).apply('_'.join, axis=1)

    all_values_string19 = '_'.join(merged_values_all_rows19)
    all_values_string20 = '_'.join(merged_values_all_rows20)

    # Get the total value counts for all values
    total_value_counts19 = pd.Series(all_values_string19.split('_')).value_counts()[:10].to_frame(
        name="count of each factor").reset_index()
    total_value_counts20 = pd.Series(all_values_string20.split('_')).value_counts()[:10].to_frame(
        name="count of each factor").reset_index()

    total_value_counts19.rename(columns={"index": "Contributing Factor"}, inplace=True)
    total_value_counts20.rename(columns={"index": "Contributing Factor"}, inplace=True)

    total_value_counts19 = total_value_counts19.drop(total_value_counts19.index[:1])
    total_value_counts20 = total_value_counts20.drop(total_value_counts20.index[:1])

    # total_value_counts.columns
    fig, axs = plt.subplots(1, 2, figsize=(12, 4))

    axs[0].pie(total_value_counts19["count of each factor"], labels=total_value_counts19["Contributing Factor"],
               autopct='%1.1f%%', startangle=0, textprops={'fontsize': 7})
    axs[0].set_title("Top 10 Contributing Factors in 2019 crashes in Queens")

    axs[1].pie(total_value_counts20["count of each factor"], labels=total_value_counts20["Contributing Factor"],
               autopct='%1.1f%%', startangle=0, textprops={'fontsize': 7})
    axs[1].set_title("Top 10 Contributing Factors in 2020 crashes in Queens")

    fig.suptitle("Pie chart for factors for crashes in 2019 and 2020")
    plt.ylabel(None)
    plt.tight_layout()
    plt.show()


def analyze_vehicle_types(Q2019, Q2020):
    """
    The function takes two dataframes as inputs and merges the required columns and finds value counts
    and plots the top 10 Vehicle types as PIE chart
    """
    # Concatenate all values in each row into a single string
    merged_values_all_rows19 = Q2019[['VEHICLE TYPE CODE 1', 'VEHICLE TYPE CODE 2',
                                      'VEHICLE TYPE CODE 3', 'VEHICLE TYPE CODE 4', 'VEHICLE TYPE CODE 5']].astype(
        str).apply('_'.join, axis=1)

    merged_values_all_rows20 = Q2020[['VEHICLE TYPE CODE 1', 'VEHICLE TYPE CODE 2',
                                      'VEHICLE TYPE CODE 3', 'VEHICLE TYPE CODE 4', 'VEHICLE TYPE CODE 5']].astype(
        str).apply('_'.join, axis=1)

    all_values_string19 = '_'.join(merged_values_all_rows19)
    all_values_string20 = '_'.join(merged_values_all_rows20)

    # Get the total value counts for all values
    total_value_counts19 = pd.Series(all_values_string19.split('_')).value_counts()[:10].to_frame(
        name="count of each vehicle").reset_index()
    total_value_counts20 = pd.Series(all_values_string20.split('_')).value_counts()[:10].to_frame(
        name="count of each vehicle").reset_index()

    total_value_counts19.rename(columns={"index": "Vehicle Type"}, inplace=True)
    total_value_counts20.rename(columns={"index": "Vehicle Type"}, inplace=True)

    total_value_counts19 = total_value_counts19.drop(total_value_counts19.index[0])
    total_value_counts20 = total_value_counts20.drop(total_value_counts20.index[0])

    # total_value_counts.columns
    fig, axs = plt.subplots(1, 2, figsize=(12, 4))

    axs[0].pie(total_value_counts19["count of each vehicle"], labels=total_value_counts19["Vehicle Type"],
               autopct='%1.1f%%', startangle=0, textprops={'fontsize': 7})
    axs[0].set_title("Top 10 Vehicle types involved in 2019 crashes in Queens")

    axs[1].pie(total_value_counts20["count of each vehicle"], labels=total_value_counts20["Vehicle Type"],
               autopct='%1.1f%%', startangle=0, textprops={'fontsize': 7})
    axs[1].set_title("Top 10 Vehicle types involved in 2020 crashes in Queens")

    fig.suptitle("Pie chart Vehicle Types involved in crashes in 2019 and 2020")
    plt.ylabel(None)
    plt.tight_layout()
    plt.show()


def find_12days_with_most_Accidents(data_2020):
    """
    This function takes a pandas dataframe as input and finds the top 12 days with most number of crashes and prints them on to the
    output
    """
    # Count the number of accidents per day
    daily_accidents_2020 = data_2020["CRASH DATE"].value_counts()

    # # Find the 12 days with the most accidents
    top_12_days = daily_accidents_2020.nlargest(12)

    print("The 12 days with the \nmost accidents in 2020 are:")
    print(top_12_days)


def daily_comparision(month_yr1, month_yr2, month, year1, year2):
    """
    This function take two pandas dataframes and month and year values as inputs
    and finds the number of crashes occured per day and group them by date and plots a bar plot
    """
    crash_counts_month_yr1 = month_yr1.groupby(month_yr1['CRASH DATE'].dt.date).size()
    crash_counts_month_yr2 = month_yr2.groupby(month_yr2['CRASH DATE'].dt.date).size()

    # Create a new DataFrame for plotting
    comparison_data = pd.DataFrame({'2019': crash_counts_month_yr1, '2020': crash_counts_month_yr2})

    # Plotting
    comparison_data.plot(kind='bar', figsize=(15, 8))
    plt.xlabel('Crash Date')
    plt.ylabel('Number of Crashes')
    plt.title(f'Daily Crash Comparison: {month} {year1} vs {month} {year2}')
    plt.show()


def analyze_day_ofthe_week(data):
    """
    The function takes a pandas dataframe as input and groups the days of the week with the number of crashes on
    that day. and plots a bar plot for each day of the week with number of crashes
    """
    # needs data from jan 2019 to oct 2020
    # Week Crash comparison between 2019 and 2020 (day wise)
    data['YEAR'] = data['CRASH DATE'].dt.year
    data['DAY OF WEEK'] = data['CRASH DATE'].dt.day_name()

    # Filter data for 2019 and 2020
    data = data[data['YEAR'].isin([2019, 2020])]

    # Group by year and day of the week
    daily_crashes = data.groupby(['DAY OF WEEK', 'YEAR']).size().unstack()

    # Reorder the days for plotting
    ordered_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    daily_crashes = daily_crashes.reindex(ordered_days)
    data.head()

    # Plot
    daily_crashes.plot(kind='bar', figsize=(15, 8))
    plt.xlabel('Day of the Week')
    plt.ylabel('Number of Crashes')
    plt.title('Day of the week Crash Comparison')
    plt.legend(title='Year')
    plt.show()


def analyze_hourly_Crashes(data):
    """
    The function takes a pandas dataframe as input and groups the hours of the day with the number of crashes on
    that day. and plots a bar plot for each hour of the day with number of crashes
    """
    # needs data from jan 2019 to oct 2020
    # Hourly Crash Comparison between for all days 2019 and 2020
    data['CRASH TIME'] = pd.to_timedelta(data['CRASH TIME'] + ':00')

    # Extract the year and hour
    data['YEAR'] = data['CRASH DATE'].dt.year
    data['HOUR'] = data['CRASH TIME'].dt.components.hours

    # Filter data for 2019 and 2020
    data = data[data['YEAR'].isin([2019, 2020])]

    # Group by year and hour
    hourly_crashes = data.groupby('HOUR').size()

    # Plot
    hourly_crashes.plot(kind='bar', figsize=(15, 8))
    plt.xlabel('Hour of Day')
    plt.ylabel('Number of Crashes')
    plt.title('Hourly Crash Comparison for 2019 and 2020')
    plt.xticks(range(0, 24), range(0, 24))  # Setting x-ticks to show every hour
    plt.legend(title='Year')
    plt.show()


def consecutive_crashes_for_100days(data):
    """
    The function takes data as input pandas dataframe and finds the number consecutive 100 days with
    most crashes. and prints to the ouput
    """
    # needs data from jan 2019 to oct 2020
    # Count the number of accidents per day
    daily_accidents = data.groupby('CRASH DATE').size()

    # Use rolling window of 100 days to sum the accidents
    rolling_sum = daily_accidents.rolling(window=99).sum()

    # Find the period with the maximum number of accidents
    max_accidents = rolling_sum.max()
    max_period_start = rolling_sum.idxmax()
    max_period_end = max_period_start + pd.Timedelta(days=100)
    print(
        f"The 100 consecutive days with the most accidents is from {max_period_start.date()} to {max_period_end.date()}, with {max_accidents} accidents.")




def analyse_numberof_injuries(yyear1, yyear2, mmonth1, mmonth2, year1, year2):
    """
    This function takes two years and two months' dataframe and year1 and year2 numeric values
    find the number of injured per dataframe and plot a graph to compare the values of the month
    with the year and another month and another year.
    """
    # to plot the number of people injured in total
    noc19 = yyear1["NUMBER OF INJURED"].sum()
    noc20 = yyear2["NUMBER OF INJURED"].sum()
    nojy19 = mmonth1["NUMBER OF INJURED"].sum()
    nojy20 = mmonth2["NUMBER OF INJURED"].sum()

    cframe = pd.DataFrame({"YEAR" : [year1, year2], "numberofinjuriesJULY" : [nojy19, nojy20], "numberofInjuriesYear": [noc19, noc20]})
    cframe.set_index("YEAR", inplace=True)
    cframe.plot(kind='bar')
    plt.title("Number of injuries in 2019 and 2020 compared with july injuries")
    plt.xlabel("Year")
    plt.ylabel("Number of Casualties")
    plt.show()