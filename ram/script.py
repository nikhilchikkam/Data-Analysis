import numpy as np
from sklearn.cluster import DBSCAN,KMeans # package to implement clustering algorithms
from sklearn.preprocessing import StandardScaler # package to standardize the features
from EDA import *

def data_preprocessing(data):
    """
    This function takes raw_data as input and performs data cleaning according to the project requirements
    and also caculates some attributes.
    :param data: The raw data that is read from the csv file
    :return : returns the cleaned data
    """

    data["CRASH DATE"] = pd.to_datetime(data["CRASH DATE"])
    data = data.drop(data[data["LATITUDE"].isna()].index)
    # data = data.drop(data[data["LONGITUDE"].isna()].index)
    data = data.drop(data[data["LATITUDE"] == 0].index)

    # drop zipcode with nans
    data = data.drop(data[data["ZIP CODE"].isna()].index)

    data["NUMBER OF KILLS"] = data['NUMBER OF PERSONS KILLED'] +\
            data['NUMBER OF CYCLIST KILLED'] + \
            data['NUMBER OF PEDESTRIANS KILLED']\
            + data['NUMBER OF MOTORIST KILLED']
        
    data["NUMBER OF INJURED"] = data["NUMBER OF PERSONS INJURED"] + \
        data['NUMBER OF PEDESTRIANS INJURED'] + \
            data['NUMBER OF MOTORIST INJURED'] \
        + data['NUMBER OF CYCLIST INJURED']

    data['NUMBER OF CASUALTIES'] = data["NUMBER OF KILLS"] + data["NUMBER OF INJURED"]
    columns_to_drop = ['LOCATION', 'NUMBER OF PERSONS INJURED',
        'NUMBER OF PERSONS KILLED', 'NUMBER OF PEDESTRIANS INJURED',
        'NUMBER OF PEDESTRIANS KILLED', 'NUMBER OF CYCLIST INJURED',
        'NUMBER OF CYCLIST KILLED', 'NUMBER OF MOTORIST INJURED',
        'NUMBER OF MOTORIST KILLED']

    data = data.drop(columns = columns_to_drop, axis = 1)
    return data


def Perform_DBSCAN(data, eps = 0.1, minpts = 20, month="June", year="2019"):
    """
    This function performs DBSCAN using sklearn package
    """
    features = data[['LATITUDE', 'LONGITUDE']]

    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    # Perform DBSCAN clustering
    dbscan = DBSCAN(eps=eps, min_samples=minpts)
    labels = dbscan.fit_predict(scaled_features)

    # Add cluster labels to the original dataset
    data['Cluster'] = labels

    data = data.drop(data[data["Cluster"]== -1].index)
    cluster_centers = []
    unique_labels = np.unique(labels)
    for label in unique_labels:
        if label == -1:
            continue  # Skip noise points
        cluster_points = scaled_features[labels == label]
        cluster_center = np.mean(cluster_points, axis=0)
        cluster_centers.append(cluster_center)

    # Convert cluster_centers to original scale
    cluster_centers_original_scale = scaler.inverse_transform(cluster_centers)

    # # Display the cluster centers in the original scale
    # for i, center in enumerate(cluster_centers_original_scale):
    #     print(f"Cluster {i + 1} Center: {center}")

    # Visualize the clusters
    plt.scatter(data['LONGITUDE'], data['LATITUDE'], c=data['Cluster'], cmap='Dark2', s=2)
    plt.title(f'NYC Crash Data Clusters (DBSCAN) {month} {year}')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.show()

    return data


def main():
    """
    This function is the main function
    This function drives the program according to the project needs
    """
    # read the data
    raw_data = pd.read_csv(r"E:\Assignments\Summer 2024\Big Data\final exam q3\Vehicle_Collisions.csv", low_memory=False)

    nyc_map = folium.Map(location=[40.7128, -74.0060], zoom_start=10)

    data = data_preprocessing(raw_data)

    # data from 2019 and 2020
    data19_20 = data[(data["CRASH DATE"].dt.year == 2019) |  (data["CRASH DATE"].dt.year == 2020)]

    # data frmo 2020
    data_2020 = data19_20[data19_20["CRASH DATE"].dt.year == 2020]
    
    # data with 2019 and 2020 data with june and july
    data_june_july_19_20 = data19_20[(data19_20["CRASH DATE"].dt.month == 6) |  (data19_20["CRASH DATE"].dt.month == 7)]
    
    # queens data with june july 2019, 2020
    Queens = data_june_july_19_20[data_june_july_19_20["BOROUGH"] == "QUEENS"] # has data for Queens june, july of 2019 and 2020.
  
    June_2019 = Queens[(Queens["CRASH DATE"].dt.year == 2019) & (Queens["CRASH DATE"].dt.month == 6)]
    June_2020 = Queens[(Queens["CRASH DATE"].dt.year == 2020) & (Queens["CRASH DATE"].dt.month == 6)]
    July_2019 = Queens[(Queens["CRASH DATE"].dt.year == 2019) & (Queens["CRASH DATE"].dt.month == 7)]
    July_2020 = Queens[(Queens["CRASH DATE"].dt.year == 2020) & (Queens["CRASH DATE"].dt.month == 7)]

    july = Queens[(Queens["CRASH DATE"].dt.month == 7)]
    june = Queens[(Queens["CRASH DATE"].dt.month == 6)]
    Q2019 = Queens[(Queens["CRASH DATE"].dt.year == 2019)]
    Q2020 = Queens[(Queens["CRASH DATE"].dt.year == 2020)]

    zipcode_compare(Q2019, Q2020)
    street_compare(Q2019, Q2020)
    analyze_contributing_factors(Q2019, Q2020)

    analyze_vehicle_types(Q2019, Q2020)
    
    daily_comparision(June_2019, June_2020, "June", 2019, 2020)
    daily_comparision(July_2019, July_2020, "July", 2019, 2020)

    clustered_dataJUNE2019 = Perform_DBSCAN(June_2019, 0.1, 15, "June", 2019)
    clustered_dataJUNE2020 = Perform_DBSCAN(June_2020, 0.1, 15, "June", 2020)
    clustered_dataJULY2019 = Perform_DBSCAN(July_2019, 0.1, 15, "July", 2019)
    clustered_dataJULY2020 = Perform_DBSCAN(July_2020, 0.1, 15, "July", 2020)

    analyse_numberof_injuries(Q2019,Q2020,July_2019,July_2020, 2019, 2020)

    start_date = '2019-01-01'
    end_date = '2020-10-31'
    qdata = data19_20[data19_20["BOROUGH"] == "BROOKLYN"]
    data_for_456 = qdata[(qdata['CRASH DATE'] >= start_date) & (qdata['CRASH DATE'] <= end_date)]

    consecutive_crashes_for_100days(data_for_456)
    analyze_day_ofthe_week(data_for_456)

    analyze_hourly_Crashes(data_for_456)

    find_12days_with_most_Accidents(data_2020)

if __name__ == "__main__":
    """
    This is the program's main guard
    """
    main()
