"""
This module implements dist and dist_matrix, functions that calculate distances between two points
and build a distance matrix for multiple points.

dist(x, y): function to compute geographic distance in miles between two points.

dist_matrix(lat_long_df): function to compute distance matrix for data frame of points.

It requires the packages math, scipy, and pandas to run.
"""

from math import sin, cos, sqrt, atan2, radians
from scipy.spatial.distance import pdist, squareform
import pandas as pd


# pylint: disable=invalid-name
def dist(x, y):
    """
    Function to compute the distance between two points x, y. Source:
    https://stackoverflow.com/questions/58943300/python-distance-matrix-between-geographic-coordinates
    :param x: tuple - coordinates of first location
    :param y: tuple - coordinates of second location
    :return: float - distance in miles bewteen two points
    """
    if len(x) != 2 or len(y) != 2:
        raise TypeError("Incorrect coordinate shape")
    lat1 = radians(x[0])
    lon1 = radians(x[1])
    lat2 = radians(y[0])
    lon2 = radians(y[1])

    r = 6373.0

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = r * c

    # convert to miles
    distance = distance / 1.609344

    return round(distance, 4)


def dist_matrix(lat_long_df):
    """
    Method that computes a distance matrix from a data frame of latitudes and longitudes.
    :param lat_long_df: pandas data frame - data frames containing each team,
        the latitudes, and longitude
    :return: numpy array - shape(n,n) where n is number of rows in lat_long_df.
        each entry is the distance between the row team and column team
    """
    if "Latitude" not in lat_long_df.columns or "Longitude" not in lat_long_df.columns:
        raise ValueError("No Latitude or Longitude column")
    if "home team" not in lat_long_df.columns:
        raise ValueError("No home team column")
    if len(lat_long_df) < 1:
        raise ValueError("Need at least 1 row of data")
    lat_long = lat_long_df[["Latitude", "Longitude"]]
    distances = pdist(lat_long.values, metric=dist)
    points = lat_long_df["home team"]
    result = pd.DataFrame(squareform(distances), columns=points, index=points)
    return result.to_numpy()
