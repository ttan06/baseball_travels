"""
This module implements various functions to build a route of games for a user to travel through.

Functions:
home_game_exists(schedule, team): Function that takes in a team and a schedule and
    finds if the team has a game in that schedule
reduce_schedule(schedule, teams, start_date, end_date): function that creates a subset
    of the MLB schedule
find_all_routes(teams): Function that provides all route combinations for teams.
build_dist_matrix(teams, schedule):  Function that builds the distance matrix for the
    given teams and schedule
game_finder(schedule, route): Function that creates a dictionary with team as the key and
    the list of home games as the value.
check_valid_route(route, schedule): Function that checks if the route is valid and creates
    schedule of games based on route if so.
reduce_routes(routes, schedule, cost_df):Function that iterates through all possible routes,
    checks the validity, creates a schedule, calculates the distance, cost, and trip length.
calculate_distance(route, schedule): Function that calculates total distance of the route.
calculate_cost(route, cost_df): Function that calculates the cost of the route.
sort_order(route_df, method='distance'): Function that sorts the routes by the desired method

It requires the packages itertools, distance, and pandas to run.
"""

from itertools import permutations
import pandas as pd
from .distance import dist_matrix

def home_game_exists(schedule, team):
    """
    Function that takes in a team and a schedule and finds if the team has a game in
        that schedule
    :param schedule: pandas data frame - contains every game for the MLB season
        with teams, location, etc.
    :param team: string - team name
    :return: boolean - returns true if home team has a game in the schedule
    """
    for home_team in schedule["home team"]:
        if home_team == team:
            return True
    return False

def reduce_schedule(schedule, teams, start_date, end_date):
    """
    Function that takes in teams and a date range to create a subset of the MLB schedule
    :param schedule: pandas data frame - contains every game for the MLB season
        with teams, location, etc.
    :param teams: list - list of desired teams to filter schedule by
    :param start_date: datetime - earliest date to filter schedule by
    :param end_date: datetime - latest date to filter schedule by
    :return: sched_subset: data frame - filtered subset of MLB schedule for
        specific teams and between dates
    """
    if (pd.to_datetime(end_date) - pd.to_datetime(start_date)).days + 1 < len(teams):
        raise ValueError('More teams than days')
    sched_subset = schedule.loc[(schedule['date'] >= start_date) & (schedule['date'] <= end_date)]
    for team_ in teams:
        if home_game_exists(sched_subset, team_) is False:
            raise ValueError(team_ + ' do not have a home game in this time frame')
    sched_subset = sched_subset.loc[schedule['home team'].isin(teams)]
    return sched_subset

def find_all_routes(teams):
    """
    Function that provides all route combinations for teams. Raises an error if there are more
        than 6 teams, to reduce runtime
    :param teams: list - list of teams
    :return: list: list of routes, where a route is a list of teams in a specific order
    """
    if len(teams) > 6:
        raise ValueError('Too many selections')
    routes = [list(route) for route in permutations(teams)]
    return routes

def build_dist_matrix(teams, schedule):
    """
    Function that builds the distance matrix for the given teams and schedule using the dist_matrix
        function from the distance package.
    :param teams: list - list of teams
    :param schedule: pandas data frame - contains every game for the MLB season
        with teams, location, etc.
    :return:
        team_dict - dictionary for indexes with teams as the key.
            Preserves the order of the matrix.
        distance matrix - (n,n) numpy array of distances between rows and columns.
            Ordered by team in route.
    """
    team_coords = schedule[['home team', 'Latitude', 'Longitude']]
    team_coords = team_coords.drop_duplicates()
    team_coords = team_coords.loc[(team_coords['home team'].isin(teams))].reset_index()
    team_coords['home team'] = team_coords['home team'].astype('category')
    team_coords['home team'] = team_coords['home team'].cat.set_categories(teams)
    team_coords = team_coords.sort_values(by=['home team'], ascending = True)
    team_dict = {}
    coord_dict = {}
    for i in range(len(team_coords)):
        team_dict[i] = team_coords['home team'][i]
        coord_dict[team_coords['home team'][i]] = \
            (team_coords['Latitude'][i],team_coords['Longitude'][i])
    return team_dict, dist_matrix(team_coords)

def game_finder(schedule, route):
    """
    Function that creates a dictionary with team as the key and
        the list of home games as the value.
    :param schedule: pandas data frame - contains every game for the MLB season
        with teams, location, etc.
    :param route: list - list of teams in order of visit.
    :return: team_games: dictionary of teams with home games as the value.
    """
    team_games = {}
    for team in route:
        team_games[team] = schedule.loc[(schedule['home team'] == team)].reset_index()
    return team_games

def check_valid_route(route, schedule):
    """
    Function that checks if the route is valid, i.e. games can be found between the dates in the
        given order. If valid, function creates schedule of games based on route, using the
        soonest game of the next team at least one day apart.
    :param route: list - list of teams in desired order.
    :param schedule: pandas data frame - contains every game for the MLB season
        with teams, location, etc.
    :return:
        validity: boolean - false if route is not valid, true if it is.
        final_sched: pandas data frame - empty if route not valid. each row is a game,
            same order as route.
        total_days: int - number of days route takes.
    """
    team_games = game_finder(schedule, route)
    first_team = team_games[route[0]].reset_index()
    col_names = first_team.columns
    sched = []
    team1_earliest = first_team.head(1)
    min_date = team1_earliest['date'][0]
    sched.append(team1_earliest.values.tolist())
    for team in route[1:]:
        games = team_games[team].reset_index()
        game_options = games.loc[games['date'] > min_date].sort_values(by=['date'])
        min_game = game_options.head(1)
        sched.append(min_game.values.tolist())
        if len(min_game['date']) == 0:
            return False, pd.DataFrame, 0
        min_date = list(min_game['date'])[0]
    final_sched = []
    for game in sched:
        final_sched.append(game[0])
    final_sched = pd.DataFrame(final_sched, columns=col_names)
    total_days = (list(final_sched['date'])[-1] - final_sched['date'][0]).days + 1
    if len(final_sched) == 0:
        raise ValueError('No Possible Games')
    return True, \
        final_sched[['date', 'time', 'away team', 'home team', 'Latitude', 'Longitude']], \
        total_days

def reduce_routes(routes, schedule, cost_df):
    """
    Function that iterates through all possible routes, checks the validity, creates a schedule,
        calculates the distance, cost, and trip length. Results in a data frame of the route,
        the games on the schedule, the total trip length, distance, and cost.
    :param routes: list - list of routes, route is a list of teams in desired order.
    :param schedule: pandas data frame - contains every game for the MLB season
        with teams, location, etc.
    :param cost_df: pandas data frame - 900 rows - all edges between two team stadiums with
        the coordinates, and the cost of the path.
    :return: all_route_options: data frame - of the route, the games on the schedule,
        the total trip length, distance, and cost.
    """
    reduced_routes = []
    game_order = []
    trip_length = []
    distances = []
    costs = []
    for route in routes:
        validity, valid_route, total_days = check_valid_route(route, schedule)
        distance = calculate_distance(route, schedule)
        cost = calculate_cost(route, cost_df)
        if validity is not False:
            reduced_routes.append(route)
            game_order.append(valid_route)
            trip_length.append(total_days)
            distances.append(distance)
            costs.append(cost)
    all_route_options = pd.DataFrame({'route': reduced_routes,
                                      'games': game_order,
                                      'time': trip_length,
                                      'distance': distances,
                                      'cost': costs})
    return all_route_options

def calculate_distance(route, schedule):
    """
    Function that calculates total distance of the route using the
        build_dist_matrix function and resulting distance matrix. Assumes distance matrix is in
        order of travel, such the needed distance is one entry to the right of the diagonal.
    :param route: list - list of teams in desired order.
    :param schedule: pandas data frame - contains every game for the MLB season
        with teams, location, etc.
    :return: total_dist: float - distance in miles of the route.
    """
    distance_matrix = build_dist_matrix(route, schedule)[1]
    total_dist = 0
    for i in range(len(route)):
        if i+1 < len(route):
            total_dist += distance_matrix[i][i+1]
    return round(total_dist)

def calculate_cost(route, cost_df):
    """
    Function that calculates the cost of the route using the cost data frame.
    :param route: list - list of teams in desired order.
    :param cost_df: pandas data frame - 900 rows - all edges between two team stadiums with
        the coordinates, and the cost of the path.
    :return: total_cost: float - cost in USD of the route.
    """
    total_cost = 0
    num_teams = len(route)
    for i in range(num_teams):
        if i+1 < len(route):
            cost = cost_df.loc[
                (cost_df['Team1'] == route[i])
                & (cost_df['Team2'] == route[i+1])].reset_index()['fare'][0]
            total_cost += cost
    return round(total_cost, 2)

def sort_order(route_df, method='distance'):
    """
    Function that sorts the routes by the desired method, either distance, cost or time.
    :param route_df: data frame - each row is a route and the distance, cost, and length of time.
    :param method: string - method of sorting. Should be either time, distance, or cost.
    :return: sorted_route_df: data frame - sorted version of route_df
    """
    method = str(method).lower()
    if method == 'time':
        sorted_route_df = route_df.sort_values(by=[method, 'cost', 'distance'], ascending=True)
        sorted_route_df = sorted_route_df.reset_index()
        sorted_route_df = sorted_route_df.drop(columns = ['index'])
        return sorted_route_df
    if method == 'cost':
        sorted_route_df = route_df.sort_values(by=[method, 'time', 'distance'], ascending=True)
        sorted_route_df = sorted_route_df.reset_index()
        sorted_route_df = sorted_route_df.drop(columns=['index'])
        return sorted_route_df
    if method == 'distance':
        sorted_route_df = route_df.sort_values(by=[method, 'time', 'cost'], ascending=True)
        sorted_route_df = sorted_route_df.reset_index()
        sorted_route_df = sorted_route_df.drop(columns=['index'])
        return sorted_route_df
    raise ValueError('Invalid Sort')
