import numpy as np
import pandas as pd
from itertools import permutations
from python_tsp.distances import euclidean_distance_matrix
from python_tsp.distances import great_circle_distance_matrix
from python_tsp.exact import solve_tsp_dynamic_programming
from python_tsp.heuristics import solve_tsp_simulated_annealing
from .distance import dist_matrix

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
            return False, pd.DataFrame, 0
        min_date = list(min_game['date'])[0]
    final_sched = []
    for g in sched:
        final_sched.append(g[0])
    final_sched = pd.DataFrame(final_sched, columns=col_names)
    total_days = (list(final_sched['date'])[-1] - final_sched['date'][0]).days + 1
    if len(final_sched) == 0:
        raise ValueError('No Possible Games')
    return True, final_sched[['date', 'time', 'away team', 'home team', 'Latitude', 'Longitude']], total_days

def reduce_routes(routes, schedule, cost_df):
    reduced_routes = []
    game_order = []
    trip_length = []
    distances = []
    costs = []
    for route in routes:
        validity, valid_route, total_days = check_valid_route(route, schedule)
        distance = calculate_distance(route, schedule)
        cost = calculate_cost(route, cost_df)
        if validity != False:
            reduced_routes.append(route)
            game_order.append(valid_route)
            trip_length.append(total_days)
            distances.append(distance)
            costs.append(cost)
    all_route_options = pd.DataFrame({'route':reduced_routes, 'games':game_order, 'time':trip_length, 'distance': distances, 'cost':costs})
    return all_route_options

# def schedule_builder(route, schedule):
#     teamGames = game_finder(schedule, route)
#     first_Team = teamGames[route[0]].reset_index()
#     col_names = first_Team.columns
#     sched = []
#     team1Earliest = first_Team.head(1)
#     min_date = team1Earliest['date'][0]
#     sched.append(team1Earliest.values.tolist())
#     for team in route[1:]:
#         games = teamGames[team].reset_index()
#         gameOptions = games.loc[games['date'] > min_date].sort_values(by=['date'])
#         min_game = gameOptions.head(1)
#         sched.append(min_game.values.tolist())
#         if (len(min_game['date'])==0):
#             raise ValueError(str(team)+' has no games after ' + str(min_date))
#         min_date = list(min_game['date'])[0]
#     final_sched = []
#     for g in sched:
#         final_sched.append(g[0])
#     final_sched = pd.DataFrame(final_sched, columns=col_names)
#
#     return final_sched[['date', 'time', 'away team', 'home team', 'Latitude', 'Longitude']]

def calculate_distance(route, schedule):
    team_dict, dist_matrix = build_dist_matrix(route, schedule)
    total_dist = 0
    for i in range(len(route)):
        if i+1 < len(route):
            total_dist += dist_matrix[i][i+1]
    return round(total_dist)

def calculate_cost(route, cost_df):
    total_cost = 0
    for i in range(len(route)):
        if i+1 < len(route):
            cost = cost_df.loc[
                (cost_df['Team1'] == route[i]) & (cost_df['Team2'] == route[i+1])].reset_index()['fare'][0]
            total_cost += cost
    return round(total_cost, 2)


# def sort_distance(routes, schedule, games):
#     """
#
#     :param routes:
#     :param schedule:
#     :return: pandas data frame of route, distance
#     """
#     distances = []
#     for route in routes:
#         distances.append(calculate_distance(route, schedule))
#     route_df = pd.DataFrame({'route': routes, 'dist': distances})
#     route_df = route_df.sort_values(by=['dist'], ascending = True)
#     route_df = route_df.reset_index()
#
#     return route_df[['route', 'dist']]

def sort_order(route_df, method = 'distance'):
    method = str(method).lower()
    if method == 'time':
        sorted_route_df = route_df.sort_values(by=[method, 'cost', 'distance'], ascending = True)
        sorted_route_df = sorted_route_df.reset_index()
        sorted_route_df = sorted_route_df.drop(columns = ['index'])
        return sorted_route_df
    elif method == 'cost':
        sorted_route_df = route_df.sort_values(by=[method, 'time', 'distance'], ascending=True)
        sorted_route_df = sorted_route_df.reset_index()
        sorted_route_df = sorted_route_df.drop(columns=['index'])
        return sorted_route_df
    elif method == 'distance':
        sorted_route_df = route_df.sort_values(by=[method, 'time', 'cost'], ascending=True)
        sorted_route_df = sorted_route_df.reset_index()
        sorted_route_df = sorted_route_df.drop(columns=['index'])
        return sorted_route_df
    else:
        raise ValueError('Invalid Sort')

# schedulee = pd.read_csv('data/final_mlb_schedule.csv')
# schedulee['date'] = pd.to_datetime(schedulee['date'])
# teamlist = ['Texas Rangers', 'Colorado Rockies', 'Baltimore Orioles', 'Seattle Mariners']#, 'Miami Marlins', 'Los Angeles Angels']
# cost_dfx = pd.read_csv('data/cost_df.csv')
#
# # x=schedule['date'][0]
# # y=schedule['date'][1000]
# # dif = y-x
# # print(x)
# # print(y)
# # print(dif.days)
#
# short_sched = reduce_schedule(schedulee, teamlist, '05-10-2024', '06-30-2024')
# routes = find_all_routes(teamlist)
# route_df = reduce_routes(routes, short_sched, cost_dfx)
# sorted_route = sort_order(route_df, 'distance')
# print(sorted_route)
#
# print(game_finder(short_sched, routes['route'][0]))


