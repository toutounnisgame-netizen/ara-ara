"""
AISystem - IA adaptative NPC selon résistance joueur
Intelligence artificielle comportementale évolutive
"""

from core.system import System
from core.entity import Entity
from components.personality import PersonalityComponent
from entities.npc import NPCMale
from typing import List, Dict, Any

class AISystem(System):
    """System IA adaptative pour NPC"""

    def __init__(self):
        super().__init__("AISystem")

    def update(self, entities: List[Entity], delta_time: float = 0.0, **kwargs):
        """Update comportement NPC selon contexte"""

        player = kwargs.get("player")
        environment = kwargs.get("environment")

        # Filtrage NPCs
        for entity in entities:
            if isinstance(entity, NPCMale):
                personality = entity.get_component_of_type(PersonalityComponent)

                if personality and player:
                    # Adaptation continue selon résistance joueur
                    resistance = player.get_resistance_level()
                    personality.adapt_to_resistance(resistance)
