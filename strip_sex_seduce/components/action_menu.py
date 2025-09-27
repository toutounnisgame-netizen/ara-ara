"""
ActionMenu Component V2.0 - Gestion menus contextuels et navigation
"""
from core.component import Component
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class MenuAction:
    """Action disponible dans un menu"""
    action_id: str
    display_name: str
    description: str
    category: str  # dialogue, physical, clothing, item, timing
    requirements: Dict[str, Any] = field(default_factory=dict)
    effects: Dict[str, int] = field(default_factory=dict)
    unlock_condition: str = ""
    energy_cost: int = 2
    arousal_impact: int = 5
    confidence_impact: int = 1
    availability_context: List[str] = field(default_factory=list)

@dataclass
class ActionMenuComponent(Component):
    """Component pour gestion menus actions contextuelles"""

    # Actions disponibles selon contexte
    available_actions: List[str] = field(default_factory=list)

    # État menu actuellement ouvert
    menu_state: str = "main"  # main, dialogue, physical, clothing, items, etc.

    # Historique sélections pour analytics
    selection_history: List[Dict[str, Any]] = field(default_factory=list)

    # Actions récemment utilisées (pour optimisation affichage)
    recent_actions: List[str] = field(default_factory=list)

    # Actions favorites du joueur (analytics)
    favorite_actions: Dict[str, int] = field(default_factory=dict)

    # Context actuel pour filtrage actions
    current_context: Dict[str, Any] = field(default_factory=dict)

    # Navigation stack pour retour menus
    menu_stack: List[str] = field(default_factory=list)

    def set_menu_state(self, new_state: str, push_to_stack: bool = True) -> None:
        """Change l'état du menu"""
        if push_to_stack and self.menu_state != "main":
            self.menu_stack.append(self.menu_state)

        self.menu_state = new_state
        self.mark_dirty()

    def go_back(self) -> str:
        """Retourne au menu précédent"""
        if self.menu_stack:
            previous_state = self.menu_stack.pop()
            self.menu_state = previous_state
        else:
            self.menu_state = "main"

        self.mark_dirty()
        return self.menu_state

    def update_available_actions(self, actions: List[str], context: Dict[str, Any]) -> None:
        """Met à jour les actions disponibles selon contexte"""
        self.available_actions = actions.copy()
        self.current_context = context.copy()
        self.mark_dirty()

    def record_action_selection(self, action_id: str, context: Dict[str, Any]) -> None:
        """Enregistre sélection action pour analytics"""
        # Historique complet
        self.selection_history.append({
            "action_id": action_id,
            "menu_state": self.menu_state,
            "timestamp": datetime.now().isoformat(),
            "context": context.copy()
        })

        # Actions récentes (max 10)
        if action_id in self.recent_actions:
            self.recent_actions.remove(action_id)
        self.recent_actions.insert(0, action_id)
        if len(self.recent_actions) > 10:
            self.recent_actions = self.recent_actions[:10]

        # Compteur favoris
        if action_id not in self.favorite_actions:
            self.favorite_actions[action_id] = 0
        self.favorite_actions[action_id] += 1

        # Limite historique pour performance
        if len(self.selection_history) > 100:
            self.selection_history = self.selection_history[-50:]

        self.mark_dirty()

    def get_favorite_actions(self, limit: int = 5) -> List[tuple]:
        """Retourne actions préférées du joueur"""
        sorted_favorites = sorted(
            self.favorite_actions.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return sorted_favorites[:limit]

    def get_menu_breadcrumb(self) -> str:
        """Retourne chemin navigation actuel"""
        if not self.menu_stack:
            return self.menu_state
        return " → ".join(self.menu_stack + [self.menu_state])

    def is_action_available(self, action_id: str) -> bool:
        """Vérifie si action est disponible"""
        return action_id in self.available_actions

    def get_actions_by_category(self, category: str) -> List[str]:
        """Filtre actions par catégorie"""
        # Nécessite accès au catalog d'actions (sera géré par le system)
        return [action for action in self.available_actions if action.startswith(category)]

    def reset_session(self) -> None:
        """Reset données session"""
        self.menu_state = "main"
        self.menu_stack.clear()
        self.available_actions.clear()
        self.current_context.clear()
        self.mark_dirty()

    def get_analytics_summary(self) -> Dict[str, Any]:
        """Retourne résumé analytics pour debug"""
        return {
            "total_selections": len(self.selection_history),
            "unique_actions_used": len(self.favorite_actions),
            "most_used_action": max(self.favorite_actions.items(), key=lambda x: x[1])[0] if self.favorite_actions else None,
            "current_menu": self.menu_state,
            "recent_actions": self.recent_actions[:5]
        }

    def to_dict(self) -> Dict[str, Any]:
        """Sérialisation pour sauvegarde"""
        return {
            "menu_state": self.menu_state,
            "available_actions_count": len(self.available_actions),
            "selection_count": len(self.selection_history),
            "favorite_actions": dict(list(self.favorite_actions.items())[:10]),
            "recent_actions": self.recent_actions[:5]
        }

    def __repr__(self) -> str:
        return f"ActionMenuComponent(state={self.menu_state}, actions={len(self.available_actions)})"
