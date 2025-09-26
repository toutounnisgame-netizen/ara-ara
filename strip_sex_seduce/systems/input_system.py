"""
InputSystem - Gestion input console optimisé
"""

from core.system import System
from core.entity import Entity
from typing import List, Dict, Any

class InputSystem(System):
    def __init__(self):
        super().__init__("InputSystem")

        self.command_aliases = {
            'r': 'resist',
            'a': 'allow',
            'f': 'flee',
            'l': 'look'
        }

    def update(self, entities: List[Entity], delta_time: float = 0.0, **kwargs):
        """Update input state"""
        pass

    def parse_input(self, raw_input: str) -> Dict[str, Any]:
        """Parse et valide input utilisateur"""

        raw_input = raw_input.strip().lower()

        # Commandes rapides
        if raw_input in self.command_aliases:
            command = self.command_aliases[raw_input]
            return {"type": "command", "value": command}

        # Commandes quit
        if raw_input in ["quit", "q", "exit"]:
            return {"type": "quit", "value": "quit"}

        # Choix numériques
        if raw_input.isdigit():
            return {"type": "choice", "value": int(raw_input)}

        # Commandes texte
        valid_commands = [
            'regarder', 'résister', 'permettre', 'fuir',
            'resist', 'allow', 'flee', 'look', 'aide', 'help', 'stats'
        ]

        if raw_input in valid_commands:
            return {"type": "command", "value": raw_input}

        return {"type": "invalid", "value": raw_input}
