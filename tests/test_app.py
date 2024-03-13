import sys
sys.path.append("..")

import unittest

import numpy as np

import app

class TestAppUI(unittest.TestCase):
    """
    Class where all tests that are called will run and are defined
    
    """

    def create_data(self):
        """
        Constructor that creates all of the data needed for the tests
        
        """

        # data
        self.dropdown_selected_teams = ['A','B','C']
        self.six_teams = ['A','B','C','D','E','F']
        self.remaining_teams = ['A','B','C','D','E','F','G']
        self.team = []
        self.start_date = []
        self.end_date = []

    def test_dropdown_normal(self) :
        """
        Test example where there less than 6 selected teams for the dropdown

        """
        self.create_data()

        self.assertEqual(
            (self.remaining_teams,self.remaining_teams),
            app.update_dropdown(self.dropdown_selected_teams, self.remaining_teams),
        )

    def test_dropdown_6_teams(self) :
        """
        Test example where there 6 selected teams for the dropdown so no options should show

        """
        self.create_data()

        self.assertEqual(
            (self.six_teams,self.remaining_teams),
            app.update_dropdown(self.six_teams, self.remaining_teams),
        )