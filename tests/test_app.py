import sys

sys.path.append("..")

import unittest

import numpy as np
import plotly.graph_objects as go

import app


class TestAppUI(unittest.TestCase):
    """
    Class where all tests that are called will run and are defined

    """

    def create_data(self):
        """
        Constructor that creates all of the data needed for the tests

        """

        # data for dropdown tests
        self.dropdown_selected_teams = ["A", "B", "C"]
        self.six_teams = ["A", "B", "C", "D", "E", "F"]
        self.remaining_teams = ["A", "B", "C", "D", "E", "F", "G"]

        # data for graph tests
        self.bad_graph = ["A", "B"]
        self.start_date = []
        self.end_date = []
        self.hovertext = [
            f"Minnesota Twins at New York Yankees on 06-04-2024 at 7:05 pm",
            "Atlanta Braves at Boston Red Sox on 06-05-2024 at 1:35 pm",
        ]
        self.good_teams = ["New York Yankees", "Boston Red Sox"]
        self.graph_result_expected = go.Figure(
            go.Scattermapbox(
                mode="markers+lines+text",
                lon=[-73.92638889, -71.0975],
                lat=[40.82916667, 42.34638889],
                hovertext=self.hovertext,
                hoverinfo="text",
                text=[1, 2],
                textposition="top center",
                marker={"size": 10},
            )
        )

        self.graph_result_expected.update_layout(
            margin={"l": 0, "t": 0, "b": 0, "r": 0},
            mapbox={
                "center": {"lat": 37.0902, "lon": -95.7129},
                "style": "open-street-map",
                "zoom": 3,
            },
            font={
                "family": "Courier New, monospace",
                "size": 25,  # Set the font size here
                "color": "blue",
            },
        )

    def test_dropdown_normal(self):
        """
        Test example where there less than 6 selected teams for the dropdown

        """
        self.create_data()

        self.assertEqual(
            (self.remaining_teams, self.remaining_teams),
            app.update_dropdown(self.dropdown_selected_teams, self.remaining_teams),
        )

    def test_dropdown_6_teams(self):
        """
        Test example where there 6 selected teams for the dropdown so no options should show

        """
        self.create_data()

        self.assertEqual(
            (self.six_teams, self.remaining_teams),
            app.update_dropdown(self.six_teams, self.remaining_teams),
        )

    def test_update_graph_no_home_games(self):
        """
        Test example that tests the graph update code fails and raises value error when no games exist

        """
        self.create_data()

        with self.assertRaises(ValueError):
            app.update_graph(self.bad_graph, "May 30,  2024", "June 30,  2024", "cost")

    def test_update_graph_yankees_red(self):
        """
        Test example that tests the graph update code

        """
        self.create_data()

        self.assertEqual(
            self.graph_result_expected,
            app.update_graph(
                self.good_teams, "May 30,  2024", "June 30,  2024", "cost"
            ),
        )
