"""Tests Entity ECS"""

import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.entity import Entity
from components.stats import StatsComponent

class TestEntity(unittest.TestCase):

    def setUp(self):
        self.entity = Entity("test_entity")

    def test_entity_creation(self):
        self.assertEqual(self.entity.id, "test_entity")
        self.assertEqual(len(self.entity.get_all_components()), 0)

    def test_add_component(self):
        stats = StatsComponent()
        self.entity.add_component(stats)

        self.assertEqual(len(self.entity.get_all_components()), 1)
        self.assertEqual(stats.entity_id, "test_entity")

    def test_get_component(self):
        stats = StatsComponent()
        self.entity.add_component(stats)

        retrieved = self.entity.get_component_of_type(StatsComponent)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved, stats)

if __name__ == '__main__':
    unittest.main()
