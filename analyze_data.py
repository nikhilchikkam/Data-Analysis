import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from db_operations import create_connection, pull_data_from_db


def plot_raw_data(data):
    """
    Plots the raw data with longitude and latitude.
    """
    plt.figure(figsize=(10, 8))
    plt.scatter(data['LONGITUDE'], data['LATITUDE'], c='gray', marker='o', s=5, label='Data Points')
    plt.title('Raw Data - Longitude vs Latitude')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.legend()
    plt.show()


def Perform_DBSCAN(data, eps, minpts):
    """
    This function performs DBSCAN using sklearn package
    """
    if data.empty:
        print("No data available for clustering")
        return data

    features = data[['LATITUDE', 'LONGITUDE']]
    scaler = StandardScaler()
    features = scaler.fit_transform(features)

    db = DBSCAN(eps=eps, min_samples=minpts).fit(features)
    labels = db.labels_

    data = data.copy()  # Create a copy to avoid SettingWithCopyWarning
    data['CLUSTER'] = labels
    return data

def plot_clusters(data, eps, minpts):
    """
    Plots the clusters with longitude and latitude on the x and y axis.
    """
    plt.figure(figsize=(10, 8))
    unique_clusters = set(data['CLUSTER'])
    colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_clusters))]

    for cluster, color in zip(unique_clusters, colors):
        if cluster == -1:
            # Black used for noise.
            color = [0, 0, 0, 1]

        clustered_points = data[data['CLUSTER'] == cluster]
        plt.plot(clustered_points['LONGITUDE'], clustered_points['LATITUDE'], 'o', markerfacecolor=tuple(color),
                 markeredgecolor='k', markersize=6, label=f'Cluster {cluster}')

    plt.title(f'DBSCAN Clustering of Brooklyn Data (eps={eps}, min_samples={minpts})')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.legend(loc='best')
    plt.show()


if __name__ == "__main__":
    try:
        # MySQL database connection details
        host_name = "localhost"
        user_name = "root"
        user_password = "nc8121"
        db_name = "nyc_crash_data"
        table_name = "crash_data"

        # Create a connection to the MySQL database
        engine = create_connection(host_name, user_name, user_password, db_name)

        # Pull data from the database
        db_data = pull_data_from_db(engine)

        # Ensure 'BOROUGH' column exists
        if 'BOROUGH' not in db_data.columns:
            print("The 'BOROUGH' column is missing in the data.")
        else:
            # Filter data for Brooklyn
            brooklyn_data = db_data[db_data["BOROUGH"] == "QUEENS"].copy()
            data_2019 = brooklyn_data[brooklyn_data['CRASH_DATE'].dt.year == 2019].copy()

            if data_2019.empty:
                print("No data available for Brooklyn.")
            else:
                # Plot raw data before clustering
                plot_raw_data(data_2019)

                # Define the ranges for eps and min_samples
                eps_values = [0.1]
                min_samples_values = [20]

                # Iterate over combinations of eps and min_samples
                for eps in eps_values:
                    for minpts in min_samples_values:
                        # Perform DBSCAN on the filtered Brooklyn data
                        print(f"dbscan with values, eps: {eps}, minpts: {minpts}")
                        clustered_data = Perform_DBSCAN(data_2019, eps, minpts)

                        if not clustered_data.empty:

                            print(clustered_data.head())

                            # Show the unique clusters and their counts
                            unique_clusters = clustered_data['CLUSTER'].unique()
                            print(f"\nUnique clusters identified (eps={eps}, min_samples={minpts}): {unique_clusters}")
                            cluster_counts = clustered_data['CLUSTER'].value_counts().sort_index()
                            print(f"\nCluster counts (eps={eps}, min_samples={minpts}):")
                            print(cluster_counts)

                            # Show the number of clusters and noise points
                            n_clusters = len(set(clustered_data['CLUSTER'])) - (
                                1 if -1 in clustered_data['CLUSTER'] else 0)
                            n_noise = list(clustered_data['CLUSTER']).count(-1)
                            print(f"\nEstimated number of clusters (eps={eps}, min_samples={minpts}): {n_clusters}")
                            print(f"Estimated number of noise points (eps={eps}, min_samples={minpts}): {n_noise}")

                            # Plot the clusters for each combination
                            plot_clusters(clustered_data, eps, minpts)
    except Exception as e:
        print(f"An error occurred: {e}")
        if engine:
            engine.dispose()  # Close the engine to prevent further errors
