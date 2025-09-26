"""Tests StatsComponent"""

import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from components.stats import StatsComponent

class TestStatsComponent(unittest.TestCase):

    def setUp(self):
        self.stats = StatsComponent()

    def test_initial_values(self):
        self.assertEqual(self.stats.volonte, 100)
        self.assertEqual(self.stats.excitation, 0)

    def test_apply_modifier(self):
        result = self.stats.apply_modifier("volonte", -10)

        self.assertEqual(self.stats.volonte, 90)
        self.assertIn("old", result)
        self.assertIn("new", result)

    def test_bounds_checking(self):
        # Test limite basse
        self.stats.apply_modifier("volonte", -150)
        self.assertEqual(self.stats.volonte, 0)

        # Test limite haute
        self.stats.apply_modifier("excitation", 150)
        self.assertEqual(self.stats.excitation, 100)

    def test_resistance_level(self):
        self.assertEqual(self.stats.get_resistance_level(), 1.0)

        self.stats.apply_modifier("volonte", -50)
        self.assertEqual(self.stats.get_resistance_level(), 0.5)

if __name__ == '__main__':
    unittest.main()
