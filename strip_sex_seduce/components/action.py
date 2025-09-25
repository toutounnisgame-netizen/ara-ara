"""
ActionComponent - Gestion actions disponibles et contraintes
Component simple pour les actions contextuelles
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from core.component import Component

@dataclass
class ActionComponent(Component):
    """
    Component gérant les actions disponibles selon contexte
    """

    # Actions possibles actuellement
    possible_actions: List[str] = field(default_factory=list)

    # Actions interdites selon contexte
    forbidden_actions: List[str] = field(default_factory=list)

    # Coûts en stats par action
    action_costs: Dict[str, Dict[str, int]] = field(default_factory=dict)

    # Taux de succès par action selon stats
    success_rates: Dict[str, float] = field(default_factory=dict)

    # Niveau d'escalation autorisé (1-5)
    escalation_level: int = 1

    def __post_init__(self):
        super().__init__()

    def add_action(self, action: str, cost: Dict[str, int] = None, success_rate: float = 1.0):
        """Ajoute une action disponible"""
        if action not in self.possible_actions:
            self.possible_actions.append(action)

        if cost:
            self.action_costs[action] = cost

        self.success_rates[action] = success_rate
        self.mark_dirty()

    def remove_action(self, action: str):
        """Supprime une action"""
        if action in self.possible_actions:
            self.possible_actions.remove(action)
        if action in self.action_costs:
            del self.action_costs[action]
        if action in self.success_rates:
            del self.success_rates[action]
        self.mark_dirty()

    def is_action_available(self, action: str) -> bool:
        """Vérifie si une action est disponible"""
        return (action in self.possible_actions and 
                action not in self.forbidden_actions)

    def get_action_cost(self, action: str) -> Dict[str, int]:
        """Retourne le coût d'une action"""
        return self.action_costs.get(action, {})

    def to_dict(self) -> Dict[str, Any]:
        base_dict = super().to_dict()
        base_dict.update({
            "actions_count": len(self.possible_actions),
            "forbidden_count": len(self.forbidden_actions),
            "escalation_level": self.escalation_level
        })
        return base_dict
