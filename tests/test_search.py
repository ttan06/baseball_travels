"""
This module performs tests on the makeRoute.exhaustiveSearch package.

Class: TestSearch - Class where tests are defined and run

Functions:
    test_reduce_schedule - smoke test testing reduce_schedule function
    test_find - smoke test testing find_all_routes function
    test_reduce_route - smoke test testing reduce_routes function
    test_sort_games - smoke test testing sort_order function

    test_find_length - one shot test if find_all_routes outputs expected number
        of combinations
    test_dist_calc - One shot tests that tests accuracy of calculate_distance function
    test_cost_calc - One shot tests that tests accuracy of calculate_cost function
    test_final_result - One shot tests that tests accuracy of final output

    test_no_home_games - Edge test that tests if error is raised with no home games
    test_more_teams - Edge test that tests if error is raised with more teams than days
    test_too_many_teams - Edge test that tests if error is raised when more than 6 teams
    test_wrong_sort - Edge test that tests if error is raised with bad sort order
"""

import unittest
import pandas as pd
from make_route.exhaustive_search import reduce_routes, reduce_schedule, sort_order, find_all_routes
from make_route.exhaustive_search import calculate_distance, calculate_cost

class TestSearch(unittest.TestCase):
    """
    Class where all tests that are called will run and are defined
    Functions:
        test_reduce_schedule - smoke test testing reduce_schedule function
        test_find - smoke test testing find_all_routes function
        test_reduce_route - smoke test testing reduce_routes function
        test_sort_games - smoke test testing sort_order function

        test_find_length - one shot test if find_all_routes outputs expected number
            of combinations
        test_dist_calc - One shot tests that tests accuracy of calculate_distance function
        test_cost_calc - One shot tests that tests accuracy of calculate_cost function
        test_final_result - One shot tests that tests accuracy of final output

        test_no_home_games - Edge test that tests if error is raised with no home games
        test_more_teams - Edge test that tests if error is raised with more teams than days
        test_too_many_teams - Edge test that tests if error is raised when more than 6 teams
        test_wrong_sort - Edge test that tests if error is raised with bad sort order
    """

    # Smoke tests
    def test_reduce_schedule(self):
        """
        Smoke test that sees if the reduce schedule runs
        """
        mlb_schedule = pd.read_csv('data/final_mlb_schedule.csv')
        mlb_schedule['date'] = pd.to_datetime(mlb_schedule['date'])
        teamlist = ['Seattle Mariners', 'Kansas City Royals', 'Houston Astros', 'Boston Red Sox']
        start_dt = '2024-05-06'
        end_dt = '2024-08-02'
        reduce_schedule(mlb_schedule, teamlist, start_dt, end_dt)

    def test_find(self):
        """
        Smoke test that tests if find_all_routes functions runs
        """
        teamlist = ['Seattle Mariners', 'Kansas City Royals', 'Houston Astros', 'Boston Red Sox']
        find_all_routes(teamlist)

    def test_reduce_route(self):
        """
        Smoke test that tests if reduce_routes functions runs
        """
        mlb_schedule = pd.read_csv('data/final_mlb_schedule.csv')
        mlb_schedule['date'] = pd.to_datetime(mlb_schedule['date'])
        cost_dfx = pd.read_csv('data/cost_df.csv')
        teamlist = ['Seattle Mariners', 'Kansas City Royals', 'Boston Red Sox']
        start_dt = '2024-05-06'
        end_dt = '2024-08-02'
        short_sched = reduce_schedule(mlb_schedule, teamlist, start_dt, end_dt)
        rts = find_all_routes(teamlist)
        reduce_routes(rts, short_sched, cost_dfx)

    def test_sort_games(self):
        """
        Smoke test that tests if sort_order functions runs
        """
        mlb_schedule = pd.read_csv('data/final_mlb_schedule.csv')
        mlb_schedule['date'] = pd.to_datetime(mlb_schedule['date'])
        cost_dfx = pd.read_csv('data/cost_df.csv')
        teamlist = ['Seattle Mariners', 'Kansas City Royals', 'Boston Red Sox']
        start_dt = '2024-05-06'
        end_dt = '2024-08-02'
        short_sched = reduce_schedule(mlb_schedule, teamlist, start_dt, end_dt)
        rts = find_all_routes(teamlist)
        game_log = reduce_routes(rts, short_sched, cost_dfx)
        sort_order(game_log, 'distance')


    # One Shot Tests

    def test_find_length(self):
        """
        One shot tests that tests find all routes provides all routes. Length of result should
            be n! where n is the number of teams
        """
        teamlist = ['Seattle Mariners', 'Kansas City Royals', 'Houston Astros', 'Boston Red Sox']
        result = find_all_routes(teamlist)
        expected = 24
        self.assertAlmostEqual(expected, len(result))

    def test_dist_calc(self):
        """
        One shot tests that tests accuracy of calculate_distance function
        """
        mlb_schedule = pd.read_csv('data/final_mlb_schedule.csv')
        mlb_schedule['date'] = pd.to_datetime(mlb_schedule['date'])
        teamlist = ["Arizona D'Backs", "Atlanta Braves"]
        start_dt = '2024-05-06'
        end_dt = '2024-06-02'
        short_sched = reduce_schedule(mlb_schedule, teamlist, start_dt, end_dt)
        expected = 1589
        self.assertAlmostEqual(expected, calculate_distance(teamlist, short_sched))

    def test_cost_calc(self):
        """
        One shot tests that tests accuracy of calculate_cost function
        """
        mlb_schedule = pd.read_csv('data/final_mlb_schedule.csv')
        mlb_schedule['date'] = pd.to_datetime(mlb_schedule['date'])
        teamlist = ["Arizona D'Backs", "Atlanta Braves", "Seattle Mariners"]
        cost_dfx = pd.read_csv('data/cost_df.csv')
        expected = 270.21 + 322.49
        self.assertAlmostEqual(expected, calculate_cost(teamlist, cost_dfx))

    def test_final_result(self):
        """
        One shot tests that tests accuracy of final output
        """
        mlb_schedule = pd.read_csv('data/final_mlb_schedule.csv')
        mlb_schedule['date'] = pd.to_datetime(mlb_schedule['date'])
        cost_dfx = pd.read_csv('data/cost_df.csv')
        teamlist = ['Seattle Mariners', 'Kansas City Royals', 'Boston Red Sox']
        start_dt = '2024-05-06'
        end_dt = '2024-08-02'
        short_sched = reduce_schedule(mlb_schedule, teamlist, start_dt, end_dt)
        rts = find_all_routes(teamlist)
        game_log = reduce_routes(rts, short_sched, cost_dfx)
        sorted_route = sort_order(game_log, 'distance')
        sched = sorted_route['games'][0]
        sched = sched[['date', 'time', 'away team', 'home team']]
        sched['date'] = sched['date'].dt.strftime('%m-%d-%Y')
        expected = pd.DataFrame({'date':['05-10-2024', '05-17-2024', '05-24-2024'],
                                 'time':['9:40 pm', '7:40 pm', '7:10 pm'],
                                 'away team':['Oakland Athletics', 'Oakland Athletics',
                                              'Milwaukee Brewers'],
                                 'home team':['Seattle Mariners', 'Kansas City Royals',
                                              'Boston Red Sox']
                                 })
        differences = expected.compare(sched)
        self.assertAlmostEqual(0, len(differences))


    # Edge tests

    def test_no_home_games(self):
        """
        Edge test that tests if error is raised with no home games
        """
        with self.assertRaises(ValueError):
            mlb_schedule = pd.read_csv('data/final_mlb_schedule.csv')
            mlb_schedule['date'] = pd.to_datetime(mlb_schedule['date'])
            teamlist = ['Seattle Mariners', 'New York Yankees']
            start_dt = '2024-05-19'
            end_dt = '2024-05-25'
            reduce_schedule(mlb_schedule, teamlist, start_dt, end_dt)

    def test_more_teams(self):
        """
        Edge test that tests if error is raised with more teams than days
        """
        with self.assertRaises(ValueError):
            mlb_schedule = pd.read_csv('data/final_mlb_schedule.csv')
            mlb_schedule['date'] = pd.to_datetime(mlb_schedule['date'])
            teamlist = ['Seattle Mariners', 'New York Yankees', 'Boston Red Sox']
            start_dt = '2024-05-19'
            end_dt = '2024-05-20'
            reduce_schedule(mlb_schedule, teamlist, start_dt, end_dt)

    def test_too_many_teams(self):
        """
        Edge test that tests if error is raised when more than 6 teams
        """
        with self.assertRaises(ValueError):
            teamlist = ['Seattle Mariners', 'New York Yankees', 'Boston Red Sox',
                        'Baltimore Orioles', 'Texas Rangers', 'New York Mets',
                        'Atlanta Braves', 'Chicago Cubs']
            find_all_routes(teamlist)
    def test_wrong_sort(self):
        """
        Edge test that tests if error is raised with bad sort order
        """
        with self.assertRaises(ValueError):
            mlb_schedule = pd.read_csv('data/final_mlb_schedule.csv')
            mlb_schedule['date'] = pd.to_datetime(mlb_schedule['date'])
            cost_dfx = pd.read_csv('data/cost_df.csv')
            teamlist = ['Seattle Mariners', 'Kansas City Royals', 'Boston Red Sox']
            start_dt = '2024-05-06'
            end_dt = '2024-08-02'
            short_sched = reduce_schedule(mlb_schedule, teamlist, start_dt, end_dt)
            rts = find_all_routes(teamlist)
            game_log = reduce_routes(rts, short_sched, cost_dfx)
            sort_order(game_log, 'nothing at all')

if __name__ == '__main__':
    unittest.main()
