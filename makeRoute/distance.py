import pandas as pd
import numpy as np
from math import sin, cos, sqrt, atan2, radians

from scipy.spatial.distance import pdist, squareform

def dist(x, y):
    """Function to compute the distance between two points x, y"""

    lat1 = radians(x[0])
    lon1 = radians(x[1])
    lat2 = radians(y[0])
    lon2 = radians(y[1])

    R = 6373.0

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    # convert to miles
    distance = distance/1.609344

    return round(distance, 4)

def dist_matrix(lat_long_df):
    lat_long = lat_long_df[['Latitude', 'Longitude']]
    distances = pdist(lat_long.values, metric=dist)
    points = lat_long_df['home team']
    result = pd.DataFrame(squareform(distances), columns=points, index=points)
    return result.to_numpy()

# schedule = pd.read_csv('final_mlb_schedule.csv')
# teamlist = ['Texas Rangers','Colorado Rockies', 'Baltimore Orioles', 'Seattle Mariners']#, 'Miami Marlins', 'Los Angeles Angels']
# teamlist2 = ['Texas Rangers', 'Baltimore Orioles', 'Seattle Mariners', 'Colorado Rockies']
#
# teamCoords = schedule[['home team', 'Latitude', 'Longitude']]
# teamCoords = teamCoords.drop_duplicates()
# teamCoords = teamCoords.loc[(teamCoords['home team'].isin(teamlist2))].reset_index()
# teamCoords['home team'] = teamCoords['home team'].astype('category')
# teamCoords['home team'] = teamCoords['home team'].cat.set_categories(teamlist2)
# #print(teamCoords['home team'])
# teamCoords = teamCoords.sort_values(by=['home team'], ascending = True)
# #print(teamCoords)
#
# lat_long = teamCoords[['Latitude', 'Longitude']]
# #print(lat_long)
#
# distances = pdist(lat_long.values, metric=dist)
#
# points = teamCoords['home team']
#
# result = pd.DataFrame(squareform(distances), columns=points, index=points)
#
# print(result)