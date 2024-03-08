import unittest
import numpy as np

from makeRoute.makeRoute import home_game_exists


class TestMakeRoute(unittest.TestCase):
    """
    Class where all tests that are called will run and are defined
    
    """

    def create_data(self):
        """
        Constructor that creates all of the data needed for the tests
        
        """

        # smoke data
        self.schedule = []
        self.team = []
        self.start_date = []
        self.end_date = []



    # Smoke test
    def test_makeRoute_homeGameExists(self):
        """
        Smoke test that sees if the makeRoute runs with simple inputs

        """
        self.create_data()

        self.assertAlmostEqual(
            True,
            home_game_exists(self.schedule,  # pandas data frame
                     self.team,  # string
                     self.start_date,  # datetime
                     self.end_date),
        )