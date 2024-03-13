"""
This module performs tests on the makeRoute.distance package.

Class: Test Distance - Class where tests are defined and run

Functions:
    test_dist - smoke test testing dist function
    test_dist_matrix - smoke test testing dist_matrix function
    test_dist2n - one shot test dist function accuracy
    test_dist_mat2n - one shot test - dist_mat accuracy
    test_dist_shape - edge test - check shape of coordinate tuples
    test_dist_mat_col - edge test - check input has lat/long columns
    test_dist_mat_col2 - edge test - check input has home team column

"""

import unittest
import pandas as pd
import numpy as np
import numpy.testing as npt
from makeRoute.distance import dist, dist_matrix


class TestDistance(unittest.TestCase):
    """
    Class where all tests that are called will run and are defined
    Functions:
        test_dist - smoke test testing dist function
        test_dist_matrix - smoke test testing dist_matrix function
        test_dist2n - one shot test dist function accuracy
        test_dist_mat2n - one shot test - dist_mat accuracy
        test_dist_shape - edge test - check shape of coordinate tuples
        test_dist_mat_col - edge test - check input has lat/long columns
        test_dist_mat_col2 - edge test - check input has home team column
    """

    # Smoke tests
    def test_dist(self):
        """
        Smoke test that sees if the dist runs with simple inputs
        """
        point1 = (77, 35)
        point2 = (100, 12)
        dist(point1, point2)

    def test_dist_matrix(self):
        """
        Smoke test that tests if dist_matrix functions runs
        """
        df = pd.DataFrame({"Latitude": [77], "Longitude": [77], "home team": ["test"]})
        dist_matrix(df)

    # One Shot Tests

    def test_dist2n(self):
        """
        One shot tests that tests accuracy of dist function
        """
        point1 = (77, 35)
        point2 = (100, 12)
        expected = 1557.8733
        self.assertAlmostEqual(expected, dist(point1, point2))

    def test_dist_mat2n(self):
        """
        One shot tests that tests accuracy of dist function
        """
        df = pd.DataFrame(
            {
                "Latitude": [77, 100],
                "Longitude": [35, 12],
                "home team": ["test1", "test2"],
            }
        )
        expected = 1557.8733
        exp_mat = np.array([[0, expected], [expected, 0]])
        npt.assert_array_almost_equal(exp_mat, dist_matrix(df))

    # Edge tests

    def test_dist_shape(self):
        """
        Edge test that tests if inputted tuples have latitude and longitude
        """
        with self.assertRaises(TypeError):
            point1 = (77, 71, 3)
            point2 = (100, 12)
            dist(point1, point2)

    def test_dist_mat_col(self):
        """
        Edge test that tests if data frame raises an error if no latitude or longitude
        """
        with self.assertRaises(ValueError):
            df = pd.DataFrame({"Latitude": [77, 100], "home team": ["test1", "test2"]})
            dist_matrix(df)

    def test_dist_mat_col2(self):
        """
        Edge test that tests if data frame raises an error if no home team
        """
        with self.assertRaises(ValueError):
            df = pd.DataFrame({"Latitude": [77, 100], "Longitude": [35, 12]})
            dist_matrix(df)


if __name__ == "__main__":
    unittest.main()
