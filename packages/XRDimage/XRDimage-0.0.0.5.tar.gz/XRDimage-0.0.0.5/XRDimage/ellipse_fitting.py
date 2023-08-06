import cv2
import pandas as pd
import numpy as np

def fit_ellipse(xcoord, ycoord):
    """
    Fit an ellipse to the given cluster points and extract ellipse parameters.

    Authors: 
        Ethan Fang

    :param xcoord: X-coordinates of the cluster points.
    :type xcoord: list or numpy.ndarray
    :param ycoord: Y-coordinates of the cluster points.
    :type ycoord: list or numpy.ndarray
    :return: DataFrame containing ellipse information sorted by increasing major axis length.
    :rtype: pandas.DataFrame
    """
    # Create a list to store ellipse information
    ellipse_data = []

    # Iterate over each cluster
    for cluster_idx in range(len(xcoord)):
        # Get the coordinates for the current cluster
        coordinates = np.column_stack((xcoord[cluster_idx], ycoord[cluster_idx]))
        center = (1023, 1023)

        # Fit an ellipse to the coordinates
        ellipse = cv2.fitEllipse(coordinates)

        # Extract the ellipse parameters
        center, axes, angle = ellipse
        major_axis_length = max(axes)
        minor_axis_length = min(axes)

        # Calculate the eccentricity of the ellipse
        a = major_axis_length / 2.0
        b = minor_axis_length / 2.0
        eccentricity = np.sqrt(1 - (b**2 / a**2))

        # Store the ellipse information in a dictionary
        ellipse_info = {
            'Cluster': cluster_idx,
            'Eccentricity': eccentricity,
            'Center': center,
            'Major Axis Length': major_axis_length,
            'Minor Axis Length': minor_axis_length,
            'Angle': angle
        }

        # Append the dictionary to the ellipse_data list
        ellipse_data.append(ellipse_info)

    # Create a DataFrame from the ellipse_data list
    df_ellipse = pd.DataFrame(ellipse_data)

    # Sort the DataFrame by increasing major axis length
    df_ellipse = df_ellipse.sort_values('Major Axis Length')

    return df_ellipse

    '''
    CHANGELOG:

    v0_1 (July 10 2023) 
    '''
