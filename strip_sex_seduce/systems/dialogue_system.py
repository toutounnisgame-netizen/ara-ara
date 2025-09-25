"""
DialogueSystem - Génération dialogues adaptatifs
"""

from core.system import System
from core.entity import Entity
from components.dialogue import DialogueComponent
from typing import List
import random

class DialogueSystem(System):
    def __init__(self):
        super().__init__("DialogueSystem")

        # Cache dialogues de base
        self.dialogue_templates = {
            "compliment": [
                "Il te sourit chaleureusement : 'Tu es vraiment magnifique ce soir...'",
                "Son regard s'attarde sur toi : 'Cette robe te va à merveille.'"
            ],
            "contact_epaule": [
                "Sa main se pose doucement sur ton épaule nue...",
                "Il se rapproche, sa main chaude sur ton épaule..."
            ]
        }

    def update(self, entities: List[Entity], delta_time: float = 0.0, **kwargs):
        """Update dialogues contextuels"""
        pass

    def generate_npc_action_text(self, action: str, player: Entity, 
                                environment: Entity) -> str:
        """Génère texte pour action NPC"""

        templates = self.dialogue_templates.get(action, [f"Il {action}."])
        return random.choice(templates)
