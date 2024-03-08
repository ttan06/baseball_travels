import numpy as np
import pandas as pd
from itertools import permutations
from python_tsp.distances import euclidean_distance_matrix
from python_tsp.distances import great_circle_distance_matrix
from python_tsp.exact import solve_tsp_dynamic_programming
from python_tsp.heuristics import solve_tsp_simulated_annealing
from distance import dist_matrix

def reduce_schedule(schedule, teams, start_date, end_date):
    sched_subset = schedule.loc[(schedule['date'] >= start_date) & (schedule['date'] <= end_date)]
    sched_subset = sched_subset.loc[schedule['home team'].isin(teams)]
    return sched_subset

def find_all_routes(teams):
    if len(teams) > 7:
        raise ValueError('Too many selections')
    else:
        pass
    routes = [list(route) for route in permutations(teams)]
    return routes

def build_dist_matrix(teams, schedule):
    teamCoords = schedule[['home team', 'Latitude', 'Longitude']]
    teamCoords = teamCoords.drop_duplicates()
    teamCoords = teamCoords.loc[(teamCoords['home team'].isin(teams))].reset_index()
    teamCoords['home team'] = teamCoords['home team'].astype('category')
    teamCoords['home team'] = teamCoords['home team'].cat.set_categories(teams)
    teamCoords = teamCoords.sort_values(by=['home team'], ascending = True)
    teamDict = {}
    coordDict = {}
    for i in range(len(teamCoords)):
        teamDict[i] = teamCoords['home team'][i]
        coordDict[teamCoords['home team'][i]] = (teamCoords['Latitude'][i],teamCoords['Longitude'][i])
    return teamDict, dist_matrix(teamCoords)

def game_finder(schedule, route):
    teamGames = {}
    for team in route:
        teamGames[team] = schedule.loc[(schedule['home team'] == team)].reset_index()
    return teamGames

def check_valid_route(route, schedule):
    teamGames = game_finder(schedule, route)
    first_Team = teamGames[route[0]].reset_index()
    col_names = first_Team.columns
    sched = []
    team1Earliest = first_Team.head(1)
    min_date = team1Earliest['date'][0]
    sched.append(team1Earliest.values.tolist())
    for team in route[1:]:
        games = teamGames[team].reset_index()
        gameOptions = games.loc[games['date'] > min_date].sort_values(by=['date'])
        min_game = gameOptions.head(1)
        sched.append(min_game.values.tolist())
        if (len(min_game['date']) == 0):
            # raise ValueError(str(team) + ' has no games after ' + str(min_date))
            return False
        min_date = list(min_game['date'])[0]
    # final_sched = []
    # for g in sched:
    #     final_sched.append(g[0])
    # final_sched = pd.DataFrame(final_sched, columns=col_names)
    return True

def reduce_routes(routes, schedule):
    reduced_routes = []
    for route in routes:
        valid_route = check_valid_route(route, schedule)
        if valid_route == True:
            reduced_routes.append(route)
    return reduced_routes

def schedule_builder(route, schedule):
    teamGames = game_finder(schedule, route)
    first_Team = teamGames[route[0]].reset_index()
    col_names = first_Team.columns
    sched = []
    team1Earliest = first_Team.head(1)
    min_date = team1Earliest['date'][0]
    sched.append(team1Earliest.values.tolist())
    for team in route[1:]:
        games = teamGames[team].reset_index()
        gameOptions = games.loc[games['date'] > min_date].sort_values(by=['date'])
        min_game = gameOptions.head(1)
        sched.append(min_game.values.tolist())
        if (len(min_game['date'])==0):
            raise ValueError(str(team)+' has no games after ' + str(min_date))
        min_date = list(min_game['date'])[0]
    final_sched = []
    for g in sched:
        final_sched.append(g[0])
    final_sched = pd.DataFrame(final_sched, columns=col_names)

    return final_sched[['date', 'time', 'away team', 'home team', 'Latitude', 'Longitude']]

def calculate_distance(route, schedule):
    team_dict, dist_matrix = build_dist_matrix(route, schedule)
    total_dist = 0
    print(route)
    print(dist_matrix)
    for i in range(len(route)):
        if i+1 < len(route):
            total_dist += dist_matrix[i][i+1]
    return total_dist

def sort_distance(routes, schedule):
    """

    :param routes:
    :param schedule:
    :return: pandas data frame of route, distance
    """
    distances = []
    for route in routes:
        distances.append(calculate_distance(route, schedule))
    route_df = pd.DataFrame({'route': routes, 'dist': distances})
    route_df = route_df.sort_values(by=['dist'], ascending = True)
    route_df = route_df.reset_index()

    return route_df[['route', 'dist']]



# schedule = pd.read_csv('final_mlb_schedule.csv')
# schedule['date'] = pd.to_datetime(schedule['date'])
# teamlist = ['Texas Rangers','Colorado Rockies', 'Baltimore Orioles', 'Seattle Mariners']#, 'Miami Marlins', 'Los Angeles Angels']
#
#
# short_sched = reduce_schedule(schedule, teamlist, '05-10-2024', '06-30-2024')
# routes = find_all_routes(teamlist)
# routes = reduce_routes(routes, short_sched)




