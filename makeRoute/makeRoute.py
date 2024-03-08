"""
The makeRoute module contains methods that determines the route based on user parameters and builds a schedule

that is then passed to app.py 

"""

import numpy as np
import pandas as pd
from python_tsp.distances import euclidean_distance_matrix
from python_tsp.distances import great_circle_distance_matrix
from python_tsp.exact import solve_tsp_dynamic_programming
from python_tsp.heuristics import solve_tsp_simulated_annealing


def home_game_exists(
    schedule,  # pandas data frame
    team,  # string
    start_date,  # datetime
    end_date,  # datetime
):
    sched_subset = schedule.loc[
        (schedule["date"] >= start_date) & (schedule["date"] <= end_date)
    ]
    for home_team in sched_subset["home team"]:
        if home_team == team:
            return True
    return False


def build_dist_matrix(teams, schedule):
    team_cords = schedule[["home team", "Latitude", "Longitude"]]
    team_cords = team_cords.drop_duplicates()
    team_cords = team_cords.loc[(team_cords["home team"].isin(teams))].reset_index()
    team_dict = {}
    cord_dict = {}
    for i in range(len(team_cords)):
        team_dict[i] = team_cords["home team"][i]
        cord_dict[team_cords["home team"][i]] = (
            team_cords["Latitude"][i],
            team_cords["Longitude"][i],
        )
    return team_dict, great_circle_distance_matrix(np.array(list(cord_dict.values())))


def route_creator(schedule, teams, start_dt, end_dt, num_routes=1):
    routes = []
    dists = []
    # Home Game Exists
    for team in teams:
        if home_game_exists(schedule, team, start_dt, end_dt) == False:
            raise ValueError(str(team) + " do not have a home game")
    # Compute Distance Matrix
    teamDict, distMat = build_dist_matrix(teams, schedule)

    permutation, distance = solve_tsp_simulated_annealing(distMat)
    perm_cities = []
    for i in permutation:
        perm_cities.append(teamDict[i])

    routes.append(perm_cities)
    dists.append(distance)

    return routes


def game_finder(schedule, route, start_dt, end_dt):
    # sched_list = []
    games = schedule.loc[(schedule["date"] >= start_dt) & (schedule["date"] <= end_dt)]
    teamGames = {}
    for team in route:
        teamGames[team] = games.loc[(games["home team"] == team)].reset_index()
    return teamGames


def schedule_builder(teamGames, route):
    first_Team = teamGames[route[0]].reset_index()
    col_names = first_Team.columns
    sched = []
    team1Earliest = first_Team.head(1)
    min_date = team1Earliest["date"][0]
    sched.append(team1Earliest.values.tolist())
    for team in route[1:]:
        games = teamGames[team].reset_index()
        gameOptions = games.loc[games["date"] > min_date].sort_values(by=["date"])
        min_game = gameOptions.head(1)
        sched.append(min_game.values.tolist())
        min_date = list(min_game["date"])[0]
    final_sched = []
    for g in sched:
        final_sched.append(g[0])
    final_sched = pd.DataFrame(final_sched, columns=col_names)

    return final_sched[['date', 'time', 'away team', 'home team', 'Latitude', 'Longitude']]


