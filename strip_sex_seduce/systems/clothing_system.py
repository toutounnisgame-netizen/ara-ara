"""
ClothingSystem - Gestion vêtements sans memory leaks
"""

from core.system import System
from core.entity import Entity
from components.clothing import ClothingComponent
from typing import List

class ClothingSystem(System):
    def __init__(self):
        super().__init__("ClothingSystem")

    def update(self, entities: List[Entity], delta_time: float = 0.0, **kwargs):
        """Update états vêtements"""

        clothing_entities = self.filter_entities(entities, [])
        for entity in clothing_entities:
            clothing = entity.get_component_of_type(ClothingComponent)
            if clothing:
                clothing._update_derived_stats()
