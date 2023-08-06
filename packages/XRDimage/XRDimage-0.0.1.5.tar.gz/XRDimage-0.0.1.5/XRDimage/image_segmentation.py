import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import imageio
import math
from sklearn.cluster import KMeans
from PIL import Image

def process_clusters(image_path, percent=0.15, number_cluster=15):
    """
    Given the image path, a percent for threshold, and an estimate number of clusters,
    obtain a dataframe of all clusters.

    Authors:
        Ethan Fang

    :param image_path: The path to the input image file.
    :type image_path: str
    :param percent: The percentage of pixels to consider, defaults to 0.15.
    :type percent: float, optional
    :param number_cluster: The number of clusters to find, defaults to 15.
    :type number_cluster: int, optional
    :return: The DataFrame with the processed results.
    :rtype: pandas.DataFrame
    """

    df = find_ring_coordinates(image_path, percent)
    df = find_clusters(df, number_cluster)

    return df

    '''
    CHANGELOG:

    v0_1 (July 10 2023) 
    '''

def calculate_distance(x1, y1, x2, y2):
    """
    Calculate the Euclidean distance between two points.

    Authors:
        Ethan Fang

    :param x1: X-coordinate of the first point.
    :type x1: float
    :param y1: Y-coordinate of the first point.
    :type y1: float
    :param x2: X-coordinate of the second point.
    :type x2: float
    :param y2: Y-coordinate of the second point.
    :type y2: float
    :return: The Euclidean distance between the two points.
    :rtype: float
    """
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance

    '''
    CHANGELOG:

    v0_1 (July 10 2023) 
    '''


def find_ring_coordinates(image_path, percent=0.15):
    """
    Find the coordinates of pixels with the highest intensities in an image.

    Authors:   
        Ethan Fang

    :param image_path: The path to the input image file.
    :type image_path: str
    :param percent: The percentage of pixels to consider, defaults to 0.15.
    :type percent: float, optional
    :return: A DataFrame containing the coordinates and intensities of the selected pixels.
    :rtype: pandas.DataFrame
    """
    image = Image.open(image_path).convert("L")
    intensities = np.array(image).flatten()
    intensities_normalized = intensities / 16383.0

    num_pixels = int(len(intensities_normalized) * percent)
    top_indices = np.argpartition(intensities_normalized, -num_pixels)[-num_pixels:]

    # Extract pixel coordinates and intensities
    pixels = []
    width, height = image.size
    for index in top_indices:
        y, x = divmod(index, width)
        intensity = intensities_normalized[index]
        pixels.append((int(x), int(y), intensity))
        
    df = pd.DataFrame(pixels, columns=["x", "y", "intensity"])
    
    # Obtaining coordinates
    threshold = df["intensity"][0]

    image = np.array(Image.open(image_path))

    distances, distanceCounter, xCoordinates, yCoordinates = [], [], [], []
    pixelNumber = 0
    mask = np.zeros_like(image, dtype=bool)
    for index, row in df.iterrows():
        x = int(row['x'])
        y = int(row['y'])
        distances.append(calculate_distance(x, y, 1023, 1023))
        distanceCounter.append(pixelNumber)
        image[x, y] = 1
        mask[x, y] = True
        pixelNumber += 1

    # Set the rest of the pixels not in the mask equal to 0
    image[~mask] = 0

    # Finish the dataframe
    distances, distanceCounter, df["x"], df["y"] = zip(*sorted(zip(distances, distanceCounter, df["x"], df["y"])))
    df['Pixel Number'] = distanceCounter
    df['Distance'] = distances
    df = df[df['Distance'] > 400]
    df = df.reset_index(drop=True)
    return df
    
    '''
    CHANGELOG:

    v0_1 (July 10 2023) 
    '''


def find_clusters(df, number_cluster=15):
    """
    Find clusters in the given DataFrame using K-means clustering.

    Authors:
        Ethan Fang

    :param df: The DataFrame containing the coordinates and intensities of the pixels.
    :type df: pandas.DataFrame
    :param number_cluster: The number of clusters to find, defaults to 15.
    :type number_cluster: int, optional
    :return: The DataFrame with an additional 'Cluster' column indicating the cluster label for each pixel.
    :rtype: pandas.DataFrame
    """
    distanced = df['Distance'].values.reshape(-1, 1)

    kmeans = KMeans(number_cluster)
    kmeans.fit(distanced)

    cluster_labels = kmeans.labels_
    df['Cluster'] = cluster_labels

    # Sort the clusters by their size
    cluster_sizes = []
    for label in np.unique(cluster_labels):
        cluster_size = np.sum(cluster_labels == label)
        cluster_sizes.append((label, cluster_size))
    cluster_sizes.sort(key=lambda x: x[1])
    cmap = plt.cm.tab20
    kmeansX, kmeansY = [], []
    # Plot each cluster on the image
    for i, (label, color) in enumerate(zip(np.unique(cluster_labels), cmap.colors)):
        cluster_points = df[df['Cluster'] == label]
        # Do something with the cluster points, e.g., kmeansX.append(cluster_points['x'].values)
    return df

    '''
    CHANGELOG:

    v0_1 (July 10 2023) 
    '''
