"""
ProgressionSystem V2.0 - Gestion unlocks, achievements et progression
"""
from core.system import System
from core.entity import Entity
from components.progression import ProgressionComponent, Achievement, UnlockRequirement
from components.seduction import SeductionComponent
from components.stats import StatsComponent
from typing import List, Dict, Any, Optional
import json
from datetime import datetime

class ProgressionSystem(System):
    """System pour gestion progression, unlocks et achievements"""

    def __init__(self):
        super().__init__("ProgressionSystem")
        self.unlock_conditions = {}
        self.achievement_definitions = {}
        self._load_progression_config()

    def _load_progression_config(self):
        """Charge configuration progression"""
        try:
            with open("assets/config/progression_config.json", 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.unlock_conditions = config.get("unlock_conditions", {})
                self.achievement_definitions = config.get("achievements", {})
        except FileNotFoundError:
            # Configuration par défaut
            self.unlock_conditions = self._get_default_unlock_conditions()
            self.achievement_definitions = self._get_default_achievements()

    def update(self, entities: List[Entity], delta_time: float = 0.0, **kwargs):
        """Update système progression"""
        player = kwargs.get("player")
        game_state = kwargs.get("game_state")

        if not player:
            return

        progression_comp = player.get_component_of_type(ProgressionComponent)
        if not progression_comp:
            return

        # Mise à jour métriques depuis autres components
        self._update_metrics_from_components(player, progression_comp, game_state)

        # Vérification nouveaux unlocks
        new_unlocks = self._check_all_unlock_conditions(progression_comp)
        if new_unlocks:
            self._process_new_unlocks(player, progression_comp, new_unlocks)

        # Vérification achievements
        new_achievements = self._check_achievement_conditions(player, progression_comp)
        if new_achievements:
            self._process_new_achievements(progression_comp, new_achievements)

    def _update_metrics_from_components(self, player: Entity, progression_comp: ProgressionComponent, game_state):
        """Met à jour métriques depuis autres components"""
        # Stats depuis SeductionComponent
        seduction_comp = player.get_component_of_type(SeductionComponent)
        if seduction_comp:
            progression_comp.update_metric("seduction_level", seduction_comp.seduction_level)
            progression_comp.update_metric("techniques_mastered", len(seduction_comp.mastered_techniques))
            progression_comp.update_metric("success_rate", seduction_comp.success_rate)

        # Stats depuis StatsComponent
        stats_comp = player.get_component_of_type(StatsComponent)
        if stats_comp:
            current_arousal = getattr(stats_comp, 'excitation', 0)
            current_resistance = getattr(stats_comp, 'volonte', 100)

            progression_comp.update_metric("max_arousal_reached", current_arousal, "max")
            progression_comp.update_metric("min_resistance_reached", current_resistance, "min")

        # Stats depuis GameState
        if game_state:
            current_location = getattr(game_state, 'current_location', 'bar')
            progression_comp.update_metric("locations_visited", current_location, "add_to_set")
            progression_comp.update_metric("session_count", 1, "add")  # Incrementé chaque session

    def _check_all_unlock_conditions(self, progression_comp: ProgressionComponent) -> List[str]:
        """Vérifie toutes conditions unlock et retourne nouveaux unlocks"""
        return progression_comp.check_unlock_conditions(self.unlock_conditions)

    def _process_new_unlocks(self, player: Entity, progression_comp: ProgressionComponent, new_unlocks: List[str]):
        """Traite nouveaux unlocks"""
        for unlock_id in new_unlocks:
            unlock_data = self.unlock_conditions.get(unlock_id, {})
            unlock_type = unlock_data.get("type", "action")

            # Notification unlock
            print(f"🔓 NOUVEAU DÉBLOQUÉ: {unlock_id} ({unlock_type})")

            # Rewards bonus si applicable
            reward_points = unlock_data.get("reward_points", 5)
            progression_comp.progression_points += reward_points

    def _check_achievement_conditions(self, player: Entity, progression_comp: ProgressionComponent) -> List[str]:
        """Vérifie conditions achievements"""
        new_achievements = []

        for achievement_id, achievement_data in self.achievement_definitions.items():
            # Skip si déjà obtenu
            if achievement_id in progression_comp.achievements:
                continue

            # Vérification conditions
            if self._is_achievement_unlocked(achievement_data, progression_comp, player):
                new_achievements.append(achievement_id)

        return new_achievements

    def _is_achievement_unlocked(self, achievement_data: Dict[str, Any], progression_comp: ProgressionComponent, player: Entity) -> bool:
        """Vérifie si achievement est débloqué"""
        requirements = achievement_data.get("requirements", {})

        for req_type, req_value in requirements.items():
            if req_type == "seduction_level":
                if progression_comp.metrics.get("seduction_level", 0) < req_value:
                    return False
            elif req_type == "max_arousal_reached":
                if progression_comp.metrics.get("max_arousal_reached", 0) < req_value:
                    return False
            elif req_type == "locations_visited_count":
                visited = progression_comp.metrics.get("locations_visited", set())
                if len(visited) < req_value:
                    return False
            elif req_type == "total_unlocks":
                total_unlocks = (len(progression_comp.unlocked_actions) + 
                               len(progression_comp.unlocked_locations) + 
                               len(progression_comp.unlocked_items) + 
                               len(progression_comp.unlocked_techniques))
                if total_unlocks < req_value:
                    return False
            elif req_type == "progression_points":
                if progression_comp.progression_points < req_value:
                    return False
            elif req_type == "success_rate":
                if progression_comp.metrics.get("success_rate", 0.5) < req_value:
                    return False
            elif req_type == "techniques_mastered":
                if progression_comp.metrics.get("techniques_mastered", 0) < req_value:
                    return False
            elif req_type == "session_count":
                if progression_comp.metrics.get("session_count", 0) < req_value:
                    return False

        return True

    def _process_new_achievements(self, progression_comp: ProgressionComponent, new_achievements: List[str]):
        """Traite nouveaux achievements"""
        for achievement_id in new_achievements:
            achievement_data = self.achievement_definitions.get(achievement_id, {})

            # Création achievement
            achievement = Achievement(
                achievement_id=achievement_id,
                name=achievement_data.get("name", achievement_id),
                description=achievement_data.get("description", ""),
                category=achievement_data.get("category", "general"),
                requirements=achievement_data.get("requirements", {}),
                reward_type=achievement_data.get("reward_type", "points"),
                reward_data=achievement_data.get("reward_data", 10),
                is_secret=achievement_data.get("is_secret", False)
            )

            # Unlock achievement
            progression_comp.unlock_achievement(achievement)

            # Notification
            if not achievement.is_secret:
                print(f"🏆 ACHIEVEMENT DÉBLOQUÉ: {achievement.name}")
                print(f"   {achievement.description}")

    def calculate_next_unlock_requirements(self, player: Entity) -> List[Dict[str, Any]]:
        """Calcule requirements pour prochains unlocks"""
        progression_comp = player.get_component_of_type(ProgressionComponent)
        if not progression_comp:
            return []

        return progression_comp.get_next_unlock_hints(self.unlock_conditions, limit=5)

    def get_progression_overview(self, player: Entity) -> Dict[str, Any]:
        """Vue d'ensemble progression joueur"""
        progression_comp = player.get_component_of_type(ProgressionComponent)
        seduction_comp = player.get_component_of_type(SeductionComponent)

        if not progression_comp:
            return {"error": "Pas de component progression"}

        # Calcul pourcentages
        total_actions_available = 50  # Supposé maximum
        total_locations_available = 4  # bar, voiture, salon, chambre
        total_techniques_available = 10  # Maximum supposé
        total_achievements_available = len(self.achievement_definitions)

        actions_percentage = (len(progression_comp.unlocked_actions) / total_actions_available) * 100
        locations_percentage = (len(progression_comp.unlocked_locations) / total_locations_available) * 100
        techniques_percentage = (len(progression_comp.unlocked_techniques) / total_techniques_available) * 100
        achievements_percentage = (len(progression_comp.achievements) / total_achievements_available) * 100 if total_achievements_available > 0 else 0

        # Progression générale
        overall_percentage = (actions_percentage + locations_percentage + techniques_percentage + achievements_percentage) / 4

        return {
            "progression_points": progression_comp.progression_points,
            "overall_percentage": round(overall_percentage, 1),
            "categories": {
                "actions": {
                    "unlocked": len(progression_comp.unlocked_actions),
                    "total": total_actions_available,
                    "percentage": round(actions_percentage, 1)
                },
                "locations": {
                    "unlocked": len(progression_comp.unlocked_locations),
                    "total": total_locations_available,
                    "percentage": round(locations_percentage, 1)
                },
                "techniques": {
                    "unlocked": len(progression_comp.unlocked_techniques),
                    "total": total_techniques_available,
                    "percentage": round(techniques_percentage, 1)
                },
                "achievements": {
                    "unlocked": len(progression_comp.achievements),
                    "total": total_achievements_available,
                    "percentage": round(achievements_percentage, 1)
                }
            },
            "seduction_summary": {
                "level": seduction_comp.seduction_level if seduction_comp else 0,
                "style": seduction_comp.seduction_style if seduction_comp else "balanced",
                "success_rate": f"{(seduction_comp.success_rate * 100):.1f}%" if seduction_comp else "50.0%"
            },
            "metrics": {
                "max_arousal": progression_comp.metrics.get("max_arousal_reached", 0),
                "locations_visited": len(progression_comp.metrics.get("locations_visited", set())),
                "sessions_played": progression_comp.metrics.get("session_count", 0)
            }
        }

    def force_unlock_for_testing(self, player: Entity, unlock_type: str, unlock_id: str) -> bool:
        """Force unlock pour testing (debug seulement)"""
        progression_comp = player.get_component_of_type(ProgressionComponent)
        if not progression_comp:
            return False

        if unlock_type == "action":
            return progression_comp.unlock_action(unlock_id, "debug_force")
        elif unlock_type == "location":
            return progression_comp.unlock_location(unlock_id, "debug_force")
        elif unlock_type == "item":
            return progression_comp.unlock_item(unlock_id, "debug_force")
        elif unlock_type == "technique":
            return progression_comp.unlock_technique(unlock_id, "debug_force")

        return False

    def _get_default_unlock_conditions(self) -> Dict[str, Any]:
        """Conditions unlock par défaut"""
        return {
            # Actions séduction base
            "contact_epaule": {
                "type": "action",
                "requirements": {
                    "seduction_level": 1,
                    "max_arousal_reached": 20
                },
                "reward_points": 5
            },
            "rapprochement_physique": {
                "type": "action", 
                "requirements": {
                    "seduction_level": 2,
                    "max_arousal_reached": 30
                },
                "reward_points": 5
            },
            "main_cuisse": {
                "type": "action",
                "requirements": {
                    "seduction_level": 3,
                    "max_arousal_reached": 50,
                    "locations_visited": 2
                },
                "reward_points": 8
            },
            "caresses_douces": {
                "type": "action",
                "requirements": {
                    "seduction_level": 3,
                    "max_arousal_reached": 50
                },
                "reward_points": 8
            },
            "caresses_intimes": {
                "type": "action",
                "requirements": {
                    "seduction_level": 5,
                    "max_arousal_reached": 70,
                    "locations_visited": 3
                },
                "reward_points": 12
            },
            "baiser_leger": {
                "type": "action",
                "requirements": {
                    "seduction_level": 4,
                    "max_arousal_reached": 60
                },
                "reward_points": 10
            },
            "baiser_profond": {
                "type": "action",
                "requirements": {
                    "seduction_level": 6,
                    "max_arousal_reached": 80
                },
                "reward_points": 15
            },
            "removal_vetement": {
                "type": "action",
                "requirements": {
                    "seduction_level": 7,
                    "max_arousal_reached": 85,
                    "locations_visited": 4
                },
                "reward_points": 20
            },
            "simulation_sexuelle": {
                "type": "action",
                "requirements": {
                    "seduction_level": 8,
                    "max_arousal_reached": 90,
                    "techniques_mastered": 3
                },
                "reward_points": 25
            },

            # Unlocks lieux
            "voiture": {
                "type": "location",
                "requirements": {
                    "max_arousal_reached": 35,
                    "total_unlocks": 3
                },
                "reward_points": 15
            },
            "salon": {
                "type": "location", 
                "requirements": {
                    "max_arousal_reached": 65,
                    "seduction_level": 4,
                    "locations_visited": 2
                },
                "reward_points": 20
            },
            "chambre": {
                "type": "location",
                "requirements": {
                    "max_arousal_reached": 85,
                    "seduction_level": 6,
                    "locations_visited": 3
                },
                "reward_points": 30
            },

            # Unlocks items
            "champagne": {
                "type": "item",
                "requirements": {
                    "seduction_level": 2,
                    "progression_points": 20
                },
                "reward_points": 5
            },
            "vibrator_discret": {
                "type": "item",
                "requirements": {
                    "seduction_level": 5,
                    "max_arousal_reached": 70,
                    "locations_visited": 3
                },
                "reward_points": 15
            },
            "preservatifs": {
                "type": "item",
                "requirements": {
                    "seduction_level": 6,
                    "max_arousal_reached": 80
                },
                "reward_points": 10
            },

            # Unlocks techniques
            "technique_tease": {
                "type": "technique",
                "requirements": {
                    "seduction_level": 3,
                    "success_rate": 0.6
                },
                "reward_points": 10
            },
            "technique_physical_escalation": {
                "type": "technique",
                "requirements": {
                    "seduction_level": 5,
                    "max_arousal_reached": 70
                },
                "reward_points": 15
            },
            "technique_master_seduction": {
                "type": "technique",
                "requirements": {
                    "seduction_level": 10,
                    "success_rate": 0.8,
                    "techniques_mastered": 5
                },
                "reward_points": 30
            }
        }

    def _get_default_achievements(self) -> Dict[str, Any]:
        """Achievements par défaut"""
        return {
            "first_seduction": {
                "name": "Première Séduction",
                "description": "Réussir ta première action de séduction",
                "category": "progression",
                "requirements": {"success_rate": 0.1},
                "reward_type": "points",
                "reward_data": 10,
                "is_secret": False
            },
            "seductress_novice": {
                "name": "Séductrice Novice",
                "description": "Atteindre le niveau 3 en séduction",
                "category": "progression",
                "requirements": {"seduction_level": 3},
                "reward_type": "technique",
                "reward_data": "technique_confidence_boost",
                "is_secret": False
            },
            "explorer": {
                "name": "Exploratrice",
                "description": "Visiter tous les lieux disponibles",
                "category": "exploration",
                "requirements": {"locations_visited_count": 4},
                "reward_type": "points", 
                "reward_data": 25,
                "is_secret": False
            },
            "arousal_master": {
                "name": "Maîtresse de l'Excitation",
                "description": "Exciter un homme à 100%",
                "category": "seduction",
                "requirements": {"max_arousal_reached": 100},
                "reward_type": "action",
                "reward_data": "ultimate_seduction",
                "is_secret": False
            },
            "technique_collector": {
                "name": "Collectionneuse de Techniques",
                "description": "Maîtriser 5 techniques de séduction",
                "category": "mastery",
                "requirements": {"techniques_mastered": 5},
                "reward_type": "points",
                "reward_data": 50,
                "is_secret": False
            },
            "seduction_goddess": {
                "name": "Déesse de la Séduction",
                "description": "Atteindre 90% de taux de succès",
                "category": "mastery",
                "requirements": {"success_rate": 0.9, "seduction_level": 8},
                "reward_type": "technique",
                "reward_data": "technique_irresistible",
                "is_secret": False
            },
            "marathon_player": {
                "name": "Joueuse Marathon",
                "description": "Jouer 10 sessions",
                "category": "dedication",
                "requirements": {"session_count": 10},
                "reward_type": "points",
                "reward_data": 100,
                "is_secret": False
            },
            "perfectionist": {
                "name": "Perfectionniste",
                "description": "Débloquer 80% du contenu",
                "category": "completion",
                "requirements": {"total_unlocks": 40, "progression_points": 500},
                "reward_type": "points",
                "reward_data": 200,
                "is_secret": True
            }
        }

    def get_system_stats(self) -> Dict[str, Any]:
        """Statistiques système"""
        return {
            "system_name": self.name,
            "unlock_conditions": len(self.unlock_conditions),
            "achievements_defined": len(self.achievement_definitions)
        }
