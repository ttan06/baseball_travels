import pandas as pd
import numpy as np
from makeRoute.distance import dist

df = pd.read_csv('data/Consumer_Airfare_Report__Table_6_-_Contiguous_State_City-Pair_Markets_That_Average_At_Least_10_Passengers_Per_Day_20240309.csv')
team_airport_key = pd.read_csv('data/team_airport_key.csv')

cities = df[['city1', 'city2','fare', 'Year', 'quarter']]
cities = cities.loc[df['Year'] == 2023]
cities = cities.loc[df['quarter'] == 3]

df_filtered = cities[cities['city1'].isin(team_airport_key['AirportCity']) & cities['city2'].isin(team_airport_key['AirportCity'])]

teams1 = []
teams2 = []
for team1 in team_airport_key['Team']:
    for team2 in team_airport_key['Team']:
        teams1.append(team1)
        teams2.append(team2)

df_team_base = pd.DataFrame({'Team1':teams1, 'Team2':teams2})
df_team_base = df_team_base.merge(team_airport_key, left_on=['Team1'], right_on=['Team'], how='left')
df_team_base['AirportCity1'] = df_team_base['AirportCity']
df_team_base= df_team_base.drop(columns = ['Team', 'AirportCity'])
df_team_base = df_team_base.merge(team_airport_key, left_on=['Team2'], right_on=['Team'], how='left')
df_team_base['AirportCity2'] = df_team_base['AirportCity']
df_team_base= df_team_base.drop(columns = ['Team', 'AirportCity'])
df_filtered = df_filtered.drop(columns = ['Year', 'quarter'])
df_reverse = pd.DataFrame({'city1': df_filtered['city2'], 'city2': df_filtered['city1'], 'fare':df_filtered['fare']})
df_full = pd.concat([df_filtered, df_reverse])
df_full = df_full.sort_values(by = ['city1', 'city2']).reset_index().drop(columns = ['index'])
df_flights = df_team_base.merge(df_full, left_on = ['AirportCity1', 'AirportCity2'], right_on = ['city1', 'city2'], how = 'left')
#df_flights.loc[df_flights['AirportCity1'] == df_flights['AirportCity2'], ['fare']] = 0
df_flights['city1'] = df_flights['AirportCity1']
df_flights['city2'] = df_flights['AirportCity2']
df_travel = df_flights.drop(columns = ['AirportCity1', 'AirportCity2'])

coords = pd.read_csv('data/final_mlb_schedule.csv')
coords = coords[['home team', 'Latitude', 'Longitude']]
coords = coords.drop_duplicates().reset_index().drop(columns = ['index'])
coords['coords'] = list(zip(coords.Latitude, coords.Longitude))
coords = coords[['home team', 'coords']]

df_travel = df_travel.merge(coords, left_on = ['Team1'], right_on = ['home team'], how = 'left')
df_travel = df_travel.drop(columns = ['home team'])
df_travel = df_travel.rename(columns={'coords': 'coords1'})
df_travel = df_travel.merge(coords, left_on = ['Team2'], right_on = ['home team'], how = 'left')
df_travel = df_travel.drop(columns = ['home team'])
df_travel = df_travel.rename(columns={'coords': 'coords2'})
dists = []
for i in range(len(df_travel)):
    distance = dist(df_travel['coords1'][i], df_travel['coords2'][i])
    dists.append(distance)
df_travel['dist'] = dists
df_travel = df_travel.rename(columns={'fare': 'airfare'})
avg_mpg = 36
cost_per_gallon = 3.29
cost_per_mile = cost_per_gallon / avg_mpg

df_travel['car_fare'] = df_travel['dist'] * cost_per_mile
df_travel['fare'] = df_travel['airfare']
df_travel['fare'] = df_travel['fare'].fillna(df_travel['car_fare'])
df_travel['min_fare'] = df_travel[['car_fare','fare']].min(axis=1)

#only take mininum fare where distance is less than 125 i.e. less than 2.5 hours drive time
df_travel['fare'] = np.where(df_travel['dist'] < 125, df_travel['min_fare'], df_travel['fare'])

#df_flights.loc[df_flights['AirportCity1'] == df_flights['AirportCity2'], ['fare']] = 0
#print(df_travel.loc[(df_travel['Team1']=='Baltimore Orioles') & (df_travel['Team2']=='Seattle Mariners')].reset_index()['fare'][0])
#print(len(df_travel.loc[(df_travel['dists']<125) & (df_travel['dists']>0)]))

df_travel.to_csv('data/cost_df.csv')