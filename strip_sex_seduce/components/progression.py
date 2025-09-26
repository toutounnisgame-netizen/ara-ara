"""
Progression Component V2.0 - Système unlocks et achievements
"""
from core.component import Component
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Achievement:
    """Achievement du jeu"""
    achievement_id: str
    name: str
    description: str
    category: str  # exploration, seduction, interaction, completion
    requirements: Dict[str, Any]
    reward_type: str  # action, item, location, technique
    reward_data: Any
    is_secret: bool = False
    unlock_date: Optional[str] = None

@dataclass
class UnlockRequirement:
    """Condition de déblocage"""
    requirement_type: str  # stat, action_count, location, achievement
    target_value: Any
    current_value: Any = 0
    is_met: bool = False

@dataclass
class ProgressionComponent(Component):
    """Component progression avec unlocks et achievements"""

    # Actions débloquées
    unlocked_actions: Set[str] = field(default_factory=set)

    # Lieux accessibles
    unlocked_locations: Set[str] = field(default_factory=lambda: {"bar"})  # Bar par défaut

    # Items disponibles pour achat/trouvaille
    unlocked_items: Set[str] = field(default_factory=set)

    # Techniques de séduction apprises
    unlocked_techniques: Set[str] = field(default_factory=set)

    # Achievements obtenus
    achievements: Dict[str, Achievement] = field(default_factory=dict)

    # Points de progression totaux
    progression_points: int = 0

    # Métriques pour conditions unlock
    metrics: Dict[str, Any] = field(default_factory=lambda: {
        "total_seduction_actions": 0,
        "total_resistance_actions": 0,
        "locations_visited": set(["bar"]),
        "max_arousal_reached": 0,
        "min_resistance_reached": 100,
        "items_used": 0,
        "techniques_mastered": 0,
        "session_count": 0,
        "total_play_time": 0
    })

    # Conditions unlock en cours
    pending_unlocks: Dict[str, UnlockRequirement] = field(default_factory=dict)

    # Historique unlocks
    unlock_history: List[Dict[str, Any]] = field(default_factory=list)

    def unlock_action(self, action_id: str, source: str = "progression") -> bool:
        """Débloque nouvelle action"""
        if action_id in self.unlocked_actions:
            return False  # Déjà débloquée

        self.unlocked_actions.add(action_id)
        self._record_unlock("action", action_id, source)
        self.mark_dirty()
        return True

    def unlock_location(self, location_id: str, source: str = "progression") -> bool:
        """Débloque nouveau lieu"""
        if location_id in self.unlocked_locations:
            return False

        self.unlocked_locations.add(location_id)
        self._record_unlock("location", location_id, source)
        self.mark_dirty()
        return True

    def unlock_item(self, item_id: str, source: str = "progression") -> bool:
        """Débloque nouvel item"""
        if item_id in self.unlocked_items:
            return False

        self.unlocked_items.add(item_id)
        self._record_unlock("item", item_id, source)
        self.mark_dirty()
        return True

    def unlock_technique(self, technique_id: str, source: str = "progression") -> bool:
        """Débloque nouvelle technique"""
        if technique_id in self.unlocked_techniques:
            return False

        self.unlocked_techniques.add(technique_id)
        self._record_unlock("technique", technique_id, source)
        self.mark_dirty()
        return True

    def unlock_achievement(self, achievement: Achievement) -> bool:
        """Débloque achievement"""
        if achievement.achievement_id in self.achievements:
            return False

        achievement.unlock_date = datetime.now().isoformat()
        self.achievements[achievement.achievement_id] = achievement

        # Application récompense
        self._apply_achievement_reward(achievement)

        self._record_unlock("achievement", achievement.achievement_id, "achievement_system")
        self.progression_points += 10  # Bonus achievement
        self.mark_dirty()
        return True

    def _apply_achievement_reward(self, achievement: Achievement) -> None:
        """Applique récompense achievement"""
        if achievement.reward_type == "action":
            self.unlock_action(achievement.reward_data, "achievement_reward")
        elif achievement.reward_type == "item":
            self.unlock_item(achievement.reward_data, "achievement_reward")
        elif achievement.reward_type == "location":
            self.unlock_location(achievement.reward_data, "achievement_reward")
        elif achievement.reward_type == "technique":
            self.unlock_technique(achievement.reward_data, "achievement_reward")
        elif achievement.reward_type == "points":
            self.progression_points += achievement.reward_data

    def _record_unlock(self, unlock_type: str, unlock_id: str, source: str) -> None:
        """Enregistre unlock dans historique"""
        self.unlock_history.append({
            "type": unlock_type,
            "id": unlock_id,
            "source": source,
            "timestamp": datetime.now().isoformat(),
            "progression_points": self.progression_points
        })

        # Limite historique
        if len(self.unlock_history) > 200:
            self.unlock_history = self.unlock_history[-100:]

    def update_metric(self, metric_name: str, value: Any, operation: str = "set") -> None:
        """Met à jour métrique progression"""
        if operation == "set":
            self.metrics[metric_name] = value
        elif operation == "add":
            if metric_name not in self.metrics:
                self.metrics[metric_name] = 0
            self.metrics[metric_name] += value
        elif operation == "max":
            if metric_name not in self.metrics:
                self.metrics[metric_name] = value
            else:
                self.metrics[metric_name] = max(self.metrics[metric_name], value)
        elif operation == "min":
            if metric_name not in self.metrics:
                self.metrics[metric_name] = value
            else:
                self.metrics[metric_name] = min(self.metrics[metric_name], value)
        elif operation == "add_to_set":
            if metric_name not in self.metrics:
                self.metrics[metric_name] = set()
            if isinstance(self.metrics[metric_name], set):
                self.metrics[metric_name].add(value)

        self.mark_dirty()

    def check_unlock_conditions(self, unlock_conditions: Dict[str, Dict[str, Any]]) -> List[str]:
        """Vérifie conditions unlock et retourne nouveaux unlocks"""
        new_unlocks = []

        for unlock_id, conditions in unlock_conditions.items():
            # Skip si déjà débloqué
            if self._is_already_unlocked(unlock_id, conditions.get("type", "action")):
                continue

            # Vérification conditions
            if self._check_conditions_met(conditions.get("requirements", {})):
                unlock_type = conditions.get("type", "action")
                if unlock_type == "action" and self.unlock_action(unlock_id, "condition_check"):
                    new_unlocks.append(unlock_id)
                elif unlock_type == "location" and self.unlock_location(unlock_id, "condition_check"):
                    new_unlocks.append(unlock_id)
                elif unlock_type == "item" and self.unlock_item(unlock_id, "condition_check"):
                    new_unlocks.append(unlock_id)
                elif unlock_type == "technique" and self.unlock_technique(unlock_id, "condition_check"):
                    new_unlocks.append(unlock_id)

        return new_unlocks

    def _is_already_unlocked(self, unlock_id: str, unlock_type: str) -> bool:
        """Vérifie si déjà débloqué"""
        if unlock_type == "action":
            return unlock_id in self.unlocked_actions
        elif unlock_type == "location":
            return unlock_id in self.unlocked_locations
        elif unlock_type == "item":
            return unlock_id in self.unlocked_items
        elif unlock_type == "technique":
            return unlock_id in self.unlocked_techniques
        return False

    def _check_conditions_met(self, requirements: Dict[str, Any]) -> bool:
        """Vérifie si conditions sont remplies"""
        for req_type, req_value in requirements.items():
            if req_type == "seduction_level" and self.metrics.get("seduction_level", 0) < req_value:
                return False
            elif req_type == "arousal_level" and self.metrics.get("max_arousal_reached", 0) < req_value:
                return False
            elif req_type == "actions_count" and self.metrics.get("total_seduction_actions", 0) < req_value:
                return False
            elif req_type == "locations_visited" and len(self.metrics.get("locations_visited", set())) < req_value:
                return False
            elif req_type == "achievements_count" and len(self.achievements) < req_value:
                return False
            elif req_type == "progression_points" and self.progression_points < req_value:
                return False

        return True

    def get_progression_summary(self) -> Dict[str, Any]:
        """Résumé progression pour affichage"""
        total_unlocks = (len(self.unlocked_actions) + 
                        len(self.unlocked_locations) + 
                        len(self.unlocked_items) + 
                        len(self.unlocked_techniques))

        return {
            "progression_points": self.progression_points,
            "total_unlocks": total_unlocks,
            "unlocked_actions": len(self.unlocked_actions),
            "unlocked_locations": len(self.unlocked_locations), 
            "unlocked_items": len(self.unlocked_items),
            "unlocked_techniques": len(self.unlocked_techniques),
            "achievements_earned": len(self.achievements),
            "locations_visited": len(self.metrics.get("locations_visited", set())),
            "session_count": self.metrics.get("session_count", 0)
        }

    def get_next_unlock_hints(self, unlock_conditions: Dict[str, Dict[str, Any]], limit: int = 3) -> List[Dict[str, Any]]:
        """Retourne hints pour prochains unlocks"""
        hints = []

        for unlock_id, conditions in unlock_conditions.items():
            if self._is_already_unlocked(unlock_id, conditions.get("type", "action")):
                continue

            requirements = conditions.get("requirements", {})
            missing_requirements = []

            for req_type, req_value in requirements.items():
                current_value = self.metrics.get(req_type.replace("_level", "").replace("_count", ""), 0)
                if req_type == "locations_visited":
                    current_value = len(self.metrics.get("locations_visited", set()))
                elif req_type == "achievements_count":
                    current_value = len(self.achievements)
                elif req_type == "progression_points":
                    current_value = self.progression_points

                if current_value < req_value:
                    missing_requirements.append({
                        "requirement": req_type,
                        "needed": req_value,
                        "current": current_value,
                        "progress": current_value / req_value if req_value > 0 else 0
                    })

            if missing_requirements:
                hints.append({
                    "unlock_id": unlock_id,
                    "unlock_type": conditions.get("type", "action"),
                    "missing_requirements": missing_requirements
                })

        # Trier par facilité d'obtention (moins de requirements manquants)
        hints.sort(key=lambda x: len(x["missing_requirements"]))
        return hints[:limit]

    def to_dict(self) -> Dict[str, Any]:
        """Sérialisation pour sauvegarde"""
        return {
            "progression_points": self.progression_points,
            "unlocked_actions": list(self.unlocked_actions),
            "unlocked_locations": list(self.unlocked_locations),
            "unlocked_items": list(self.unlocked_items),
            "unlocked_techniques": list(self.unlocked_techniques),
            "achievements_count": len(self.achievements),
            "metrics": {k: list(v) if isinstance(v, set) else v for k, v in self.metrics.items()},
            "unlock_history_count": len(self.unlock_history)
        }

    def __repr__(self) -> str:
        total_unlocks = len(self.unlocked_actions) + len(self.unlocked_locations) + len(self.unlocked_items) + len(self.unlocked_techniques)
        return f"ProgressionComponent(points={self.progression_points}, unlocks={total_unlocks}, achievements={len(self.achievements)})"
