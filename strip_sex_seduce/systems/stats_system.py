"""
StatsSystem - Gestion équilibrage résistance/excitation
System central pour gameplay résistance/cession
"""

from core.system import System
from core.entity import Entity
from components.stats import StatsComponent
from typing import List, Dict, Any, Optional

class StatsSystem(System):
    """System gérant l'équilibrage des stats joueur"""

    def __init__(self):
        super().__init__("StatsSystem")

        # Configuration équilibrage
        self.action_effects = {
            "compliment": {"volonte": -2, "excitation": 3},
            "contact_epaule": {"volonte": -5, "excitation": 5},
            "main_cuisse": {"volonte": -8, "excitation": 12},
            "baiser_leger": {"volonte": -10, "excitation": 15},
            "caresses": {"volonte": -12, "excitation": 20}
        }

    def update(self, entities: List[Entity], delta_time: float = 0.0, **kwargs):
        """Update principal du system"""

        # Filtrage entities avec StatsComponent
        stats_entities = self.filter_entities(entities, [])

        for entity in stats_entities:
            stats = entity.get_component_of_type(StatsComponent)
            if stats:
                # Application effets temporaires decay
                stats.apply_temporary_effects_decay()

    def apply_npc_action(self, player: Entity, action: str, 
                        context: Dict[str, Any]) -> Dict[str, Any]:
        """Applique effets action NPC sur joueur"""

        stats = player.get_component_of_type(StatsComponent)
        if not stats:
            return {"success": False, "error": "Pas de StatsComponent"}

        # Récupération effets action
        effects = self.action_effects.get(action, {"volonte": 0, "excitation": 0})

        # Application avec context
        stats_before = {"volonte": stats.volonte, "excitation": stats.excitation}

        for stat, value in effects.items():
            # Modificateurs selon lieu
            modified_value = self._apply_context_modifiers(value, context)
            stats.apply_modifier(stat, modified_value, source=f"npc_{action}")

        stats_after = {"volonte": stats.volonte, "excitation": stats.excitation}

        return {
            "success": True,
            "stats_before": stats_before,
            "stats_after": stats_after,
            "effects_applied": effects
        }

    def apply_player_resistance(self, player: Entity, 
                              context: Dict[str, Any]) -> Dict[str, Any]:
        """Applique effets résistance joueur"""

        stats = player.get_component_of_type(StatsComponent)
        if not stats:
            return {"success": False}

        # Effet résistance selon type
        resistance_type = context.get("type", "soft_resistance")

        if resistance_type == "soft_resistance":
            volonte_gain = 5
            success_chance = 0.7
        else:  # firm_resistance
            volonte_gain = 10
            success_chance = 0.9

        # Application
        import random
        success = random.random() < success_chance

        if success:
            stats.apply_modifier("volonte", volonte_gain, source="player_resistance")

        return {
            "success": success,
            "volonte_gained": volonte_gain if success else 0
        }

    def _apply_context_modifiers(self, base_value: int, 
                                context: Dict[str, Any]) -> int:
        """Applique modificateurs contextuels"""

        # Modificateur selon lieu
        location = context.get("location", "bar")
        privacy = context.get("privacy", 0.5)

        # Plus privé = effets plus forts
        privacy_modifier = 1.0 + (privacy * 0.3)

        return int(base_value * privacy_modifier)
