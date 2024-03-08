import numpy as np
import pandas as pd
from python_tsp.distances import euclidean_distance_matrix
from python_tsp.distances import great_circle_distance_matrix
from python_tsp.exact import solve_tsp_dynamic_programming
from python_tsp.heuristics import solve_tsp_simulated_annealing

def reduce_schedule(schedule, teams, start_date, end_date):
    sched_subset = schedule.loc[(schedule['date'] >= start_date) & (schedule['date'] <= end_date)]
    sched_subset = sched_subset.loc[schedule['home team'].isin(teams)]
    return sched_subset

def home_game_exists(schedule,  # pandas data frame
                     team,  # string
                     start_date,  # datetime
                     end_date  # datetime
                     ):
    sched_subset = schedule.loc[(schedule['date'] >= start_date) & (schedule['date'] <= end_date)]
    for home_team in sched_subset['home team']:
        if home_team == team:
            return True
    return False

def build_dist_matrix(teams, schedule):
    teamCoords = schedule[['home team', 'Latitude', 'Longitude']]
    teamCoords = teamCoords.drop_duplicates()
    teamCoords = teamCoords.loc[(teamCoords['home team'].isin(teams))].reset_index()
    teamDict = {}
    coordDict = {}
    for i in range(len(teamCoords)):
        teamDict[i] = teamCoords['home team'][i]
        coordDict[teamCoords['home team'][i]] = (teamCoords['Latitude'][i],teamCoords['Longitude'][i])
    return teamDict, great_circle_distance_matrix(np.array(list(coordDict.values())))


def route_creator(schedule, teams, start_dt, end_dt, num_routes=1):
    routes = []
    dists = []
    # Home Game Exists
    for team in teams:
        if (home_game_exists(schedule, team, start_dt, end_dt) == False):
            raise ValueError(str(team) + ' do not have a home game')
    # Compute Distance Matrix
    teamDict, distMat = build_dist_matrix(teams, schedule)

    permutation, distance = solve_tsp_simulated_annealing(distMat)
    perm_cities = []
    for i in permutation:
        perm_cities.append(teamDict[i])

    routes.append(perm_cities)
    dists.append(distance)

    return routes

def route_creator_exahustive(schedule, teams, start_dt, end_dt, num_routes=1):
    return None

def game_finder(schedule, route, start_dt, end_dt):
    # sched_list = []
    games = schedule.loc[(schedule['date'] >= start_dt) & (schedule['date'] <= end_dt)]
    teamGames = {}
    for team in route:
        teamGames[team] = games.loc[(games['home team'] == team)].reset_index()
    return teamGames


def schedule_builder(teamGames, route):
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

schedule = pd.read_csv('final_mlb_schedule.csv')
schedule['date'] = pd.to_datetime(schedule['date'])
teamlist = ['Texas Rangers','Colorado Rockies', 'Baltimore Orioles','Detroit Tigers','Minnesota Twins', 'St. Louis Cardinals', 'Tampa Bay Rays']

print(reduce_schedule(schedule, teamlist, '05-10-2024', '06-30-2024'))

# r1 = route_creator(schedule, teamlist, '05-10-2024', '06-30-2024', 1)
# g1 = game_finder(schedule, r1[0], '05-10-2024', '06-30-2024')
# print(schedule_builder(g1, r1[0]))


