"""
GameState Entity - État global du jeu
Gestion progression, achievements et métadonnées session
"""

from core.entity import Entity
from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid

class GameState(Entity):
    """
    Entity gérant l'état global du jeu
    Centralise progression, achievements et état session
    """

    def __init__(self):
        super().__init__("game_state")

        # Progression narrative
        self.current_location = "bar"
        self.turn_count = 0
        self.game_phase = "introduction"  # introduction/seduction/escalation/resolution

        # Flags et événements
        self.story_flags = []
        self.location_history = []
        self.major_events = []

        # Informations session
        self.session_id = str(uuid.uuid4())
        self.session_start = datetime.now()
        self.session_duration = 0

        # Configuration session
        self.npc_personality_seed = 0
        self.difficulty_level = "normal"  # easy/normal/hard
        self.content_level = "full"       # light/medium/full

        # Achievements système
        self.achievements = {
            "first_resistance": False,      # Première résistance
            "first_submission": False,      # Première soumission
            "location_reached": {},         # Lieux atteints
            "personality_adapted": False,   # NPC s'est adapté
            "escape_attempted": False,      # Tentative fuite
            "full_submission": False,       # Soumission complète
            "resistance_victory": False,    # Victoire par résistance
            "all_locations": False,         # Tous lieux visités
            "master_seducer": False,        # NPC très efficace
            "iron_will": False              # Résistance maintenue longtemps
        }

        # Statistiques détaillées
        self.stats = {
            "total_actions": 0,
            "player_resistances": 0,
            "player_submissions": 0,
            "npc_successes": 0,
            "npc_failures": 0,
            "location_changes": 0,
            "escalation_attempts": 0,
            "max_volonte": 100,
            "min_volonte": 100,
            "max_excitation": 0,
            "peak_exposure": 0
        }

        # Debug et monitoring
        self.debug_info = {
            "memory_usage": 0,
            "performance_ms": [],
            "error_count": 0,
            "warning_count": 0,
            "system_calls": 0
        }

    def advance_turn(self):
        """Avance d'un tour de jeu"""
        self.turn_count += 1
        self.stats["total_actions"] += 1

        # Mise à jour durée session
        self.session_duration = int((datetime.now() - self.session_start).total_seconds())

        # Check achievements liés aux tours
        self._check_turn_based_achievements()

    def change_location(self, new_location: str) -> bool:
        """
        Change le lieu actuel

        Args:
            new_location: Nouveau lieu

        Returns:
            True si changement réussi
        """
        if new_location != self.current_location:
            # Historique
            self.location_history.append({
                "from": self.current_location,
                "to": new_location,
                "turn": self.turn_count
            })

            self.current_location = new_location
            self.stats["location_changes"] += 1

            # Achievement lieux atteints
            self.achievements["location_reached"][new_location] = True

            # Check si tous lieux visités
            all_locations = {"bar", "voiture", "salon", "chambre"}
            visited = set(self.achievements["location_reached"].keys())
            if visited >= all_locations:
                self.unlock_achievement("all_locations")

            return True
        return False

    def add_story_flag(self, flag: str, context: Dict[str, Any] = None):
        """Ajoute un flag narratif"""
        if flag not in self.story_flags:
            self.story_flags.append(flag)

            # Événement majeur si spécifié
            if context and context.get("major", False):
                self.major_events.append({
                    "flag": flag,
                    "turn": self.turn_count,
                    "context": context
                })

    def has_story_flag(self, flag: str) -> bool:
        """Vérifie la présence d'un flag narratif"""
        return flag in self.story_flags

    def update_game_phase(self, new_phase: str):
        """Met à jour la phase de jeu"""
        if new_phase != self.game_phase:
            self.add_story_flag(f"phase_{new_phase}_entered", {"major": True})
            self.game_phase = new_phase

    def record_player_action(self, action_type: str, success: bool, 
                           stats_before: Dict, stats_after: Dict):
        """
        Enregistre une action joueur pour analytics

        Args:
            action_type: Type d'action ("resist", "allow", etc.)
            success: Si l'action a atteint son objectif
            stats_before/after: Stats avant et après l'action
        """
        if action_type in ["resist", "resist_soft", "resist_firm"]:
            self.stats["player_resistances"] += 1

            if not self.achievements["first_resistance"]:
                self.unlock_achievement("first_resistance")

        elif action_type in ["allow", "encourage", "submit"]:
            self.stats["player_submissions"] += 1

            if not self.achievements["first_submission"]:
                self.unlock_achievement("first_submission")

        # Mise à jour extremes stats
        volonte_after = stats_after.get("volonte", 100)
        excitation_after = stats_after.get("excitation", 0)

        self.stats["min_volonte"] = min(self.stats["min_volonte"], volonte_after)
        self.stats["max_excitation"] = max(self.stats["max_excitation"], excitation_after)

    def record_npc_action(self, action: str, success: bool, 
                         escalation_level: int = 1):
        """
        Enregistre une action NPC pour analytics

        Args:
            action: Action NPC
            success: Efficacité de l'action
            escalation_level: Niveau d'escalation (1-5)
        """
        if success:
            self.stats["npc_successes"] += 1
        else:
            self.stats["npc_failures"] += 1

        if escalation_level >= 3:
            self.stats["escalation_attempts"] += 1

    def record_clothing_change(self, exposure_level: int):
        """Enregistre changement vêtements"""
        self.stats["peak_exposure"] = max(self.stats["peak_exposure"], exposure_level)

    def unlock_achievement(self, achievement_name: str) -> bool:
        """
        Débloque un achievement

        Args:
            achievement_name: Nom de l'achievement

        Returns:
            True si nouvel achievement débloqué
        """
        if achievement_name in self.achievements:
            if not self.achievements[achievement_name]:
                self.achievements[achievement_name] = True
                self.add_story_flag(f"achievement_{achievement_name}", {"major": True})
                return True
        return False

    def _check_turn_based_achievements(self):
        """Vérifie les achievements basés sur le nombre de tours"""

        # Résistance prolongée
        if self.turn_count >= 20 and self.stats["min_volonte"] > 70:
            self.unlock_achievement("iron_will")

        # NPC très efficace
        if self.stats["npc_successes"] >= 10:
            npc_success_rate = (
                self.stats["npc_successes"] / 
                max(1, self.stats["npc_successes"] + self.stats["npc_failures"])
            )
            if npc_success_rate > 0.8:
                self.unlock_achievement("master_seducer")

    def check_end_conditions(self) -> Optional[str]:
        """
        Vérifie les conditions de fin de partie

        Returns:
            Type de fin ou None si jeu continue
        """
        # Soumission complète
        if self.stats["min_volonte"] <= 5 and self.stats["max_excitation"] >= 90:
            self.unlock_achievement("full_submission")
            return "submission_complete"

        # Résistance victorieuse
        if self.turn_count > 25 and self.stats["min_volonte"] > 70:
            self.unlock_achievement("resistance_victory")
            return "resistance_victory"

        # Fuite réussie
        if self.has_story_flag("escape_successful"):
            return "escape_success"

        # Limite de tours atteinte
        if self.turn_count >= 50:
            return "time_limit"

        return None

    def get_session_summary(self) -> Dict[str, Any]:
        """Retourne un résumé complet de la session"""

        # Calcul ratios
        total_actions = max(1, self.stats["total_actions"])
        player_actions = self.stats["player_resistances"] + self.stats["player_submissions"]
        npc_actions = self.stats["npc_successes"] + self.stats["npc_failures"]

        return {
            "session_info": {
                "id": self.session_id,
                "duration_seconds": self.session_duration,
                "turns": self.turn_count,
                "phase": self.game_phase,
                "current_location": self.current_location
            },
            "progression": {
                "locations_visited": len(self.achievements["location_reached"]),
                "story_flags": len(self.story_flags),
                "major_events": len(self.major_events)
            },
            "player_performance": {
                "resistance_ratio": self.stats["player_resistances"] / max(1, player_actions),
                "submission_ratio": self.stats["player_submissions"] / max(1, player_actions),
                "min_volonte_reached": self.stats["min_volonte"],
                "max_excitation_reached": self.stats["max_excitation"],
                "peak_exposure": self.stats["peak_exposure"]
            },
            "npc_performance": {
                "success_rate": self.stats["npc_successes"] / max(1, npc_actions),
                "escalation_attempts": self.stats["escalation_attempts"],
                "adaptations_made": sum(1 for flag in self.story_flags if "adapt" in flag)
            },
            "achievements": {
                "unlocked": sum(1 for achieved in self.achievements.values() if achieved),
                "total": len(self.achievements),
                "list": [name for name, achieved in self.achievements.items() if achieved]
            }
        }

    def to_dict(self) -> Dict[str, Any]:
        """Sérialisation complète du game state"""
        base_dict = super().to_dict()
        base_dict.update({
            "session_summary": self.get_session_summary(),
            "current_state": {
                "location": self.current_location,
                "turn": self.turn_count,
                "phase": self.game_phase
            },
            "achievements_unlocked": sum(1 for a in self.achievements.values() if a),
            "debug_info": self.debug_info
        })
        return base_dict

    def __repr__(self) -> str:
        achievements_count = sum(1 for a in self.achievements.values() if a)
        return (f"GameState(turn={self.turn_count}, "
                f"location={self.current_location}, "
                f"phase={self.game_phase}, "
                f"achievements={achievements_count}/{len(self.achievements)})")
