"""
StatsSystem V2.0 - Affichage temps réel + effets visibles
Correctif: Stats mises à jour visibles + équilibrage progression
"""

from core.system import System
from core.entity import Entity
from components.stats import StatsComponent
from typing import List, Dict, Any, Optional
import random

class StatsSystem(System):
    """System stats avec affichage temps réel et équilibrage amélioré"""

    def __init__(self):
        super().__init__("StatsSystem")

        # ÉQUILIBRAGE V2.0 - Progression fluide garantie
        self.action_effects = {
            # Actions douces - progression graduelle
            "compliment": {"volonte": -3, "excitation": 4},
            "regard_insistant": {"volonte": -2, "excitation": 6}, 
            "conversation_charme": {"volonte": -4, "excitation": 3},

            # Actions contact leger - escalation visible
            "contact_epaule": {"volonte": -6, "excitation": 8},
            "rapprochement_physique": {"volonte": -5, "excitation": 10},

            # Actions contact modéré - impact significatif
            "main_cuisse": {"volonte": -10, "excitation": 15},
            "caresses_douces": {"volonte": -8, "excitation": 12},

            # Actions intenses - effets majeurs
            "baiser_leger": {"volonte": -12, "excitation": 18},
            "caresses": {"volonte": -15, "excitation": 22},
            "baiser_profond": {"volonte": -18, "excitation": 25},

            # Actions très intenses - fin de partie proche
            "caresses_intimes": {"volonte": -20, "excitation": 30},
            "removal_vetement": {"volonte": -25, "excitation": 35}
        }

        # Modificateurs par lieu pour réalisme
        self.location_modifiers = {
            "bar": {"volonte_mult": 1.2, "excitation_mult": 0.8},      # Plus résistance public
            "voiture": {"volonte_mult": 1.0, "excitation_mult": 1.1},   # Équilibré
            "salon": {"volonte_mult": 0.8, "excitation_mult": 1.3},     # Moins résistance privé
            "chambre": {"volonte_mult": 0.6, "excitation_mult": 1.5}    # Très excitant privé
        }

        # Messages de transition seuils pour feedback
        self.threshold_messages = {
            "vulnerable_entered": "💔 Tu te sens plus vulnérable à ses avances...",
            "aroused_entered": "🔥 Tu ne peux plus ignorer ton excitation croissante...",
            "submissive_entered": "😵 Ta volonté s'effrite dangereusement...",
            "climax_ready_entered": "💥 Ton corps tout entier réclame plus..."
        }

        # Derniers seuils pour détection changements
        self._last_thresholds = {}

    def update(self, entities: List[Entity], delta_time: float = 0.0, **kwargs):
        """Update avec gestion effets temporaires + seuils"""

        # Filtrage entities avec stats
        for entity in entities:
            stats = entity.get_component_of_type(StatsComponent)
            if stats and stats.is_dirty:
                # Decay effets temporaires
                stats.apply_temporary_effects_decay(decay_rate=0.9)

                # Check transitions seuils pour feedback
                self._check_threshold_transitions(entity, stats)

                stats.mark_clean()

    def apply_npc_action(self, player: Entity, action: str, 
                        context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Application effets NPC avec affichage temps réel GARANTI

        Args:
            player: Entity player
            action: Action NPC effectuée
            context: Contexte (lieu, privacy, etc.)

        Returns:
            Dict résultats avec changements visibles
        """
        stats = player.get_component_of_type(StatsComponent)
        if not stats:
            return {"success": False, "error": "Pas de StatsComponent", "visible_change": False}

        # Sauvegarde état avant
        stats_before = {
            "volonte": stats.volonte,
            "excitation": stats.excitation,
            "thresholds": stats.thresholds.copy()
        }

        # Récupération effets base
        base_effects = self.action_effects.get(action, {"volonte": -1, "excitation": 2})

        # APPLICATION MODIFICATEURS CONTEXTUELS
        location = context.get("location", "bar")
        location_mod = self.location_modifiers.get(location, self.location_modifiers["bar"])

        # Calcul effets finaux avec modificateurs
        final_effects = {}
        for stat, value in base_effects.items():
            if stat == "volonte":
                final_effects[stat] = int(value * location_mod["volonte_mult"])
            elif stat == "excitation":  
                final_effects[stat] = int(value * location_mod["excitation_mult"])
            else:
                final_effects[stat] = value

        # APPLICATION RÉELLE avec feedback
        changes_made = {}
        for stat, value in final_effects.items():
            result = stats.apply_modifier(stat, value, source=f"npc_{action}")
            changes_made[stat] = result["actual_change"]

        # État après modification
        stats_after = {
            "volonte": stats.volonte,
            "excitation": stats.excitation,
            "thresholds": stats.thresholds.copy()
        }

        # FORCE DIRTY FLAG pour affichage immédiat
        stats.mark_dirty()

        # Détection changements significatifs pour feedback
        volonte_change = abs(changes_made.get("volonte", 0))
        excitation_change = abs(changes_made.get("excitation", 0))
        significant_change = volonte_change >= 5 or excitation_change >= 5

        return {
            "success": True,
            "stats_before": stats_before,
            "stats_after": stats_after,
            "changes_made": changes_made,
            "effects_applied": final_effects,
            "location_modified": location != "bar",
            "visible_change": significant_change,
            "escalation_level": self._calculate_escalation_level(action)
        }

    def apply_player_resistance(self, player: Entity, 
                              resistance_type: str,
                              context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Résistance joueur avec types différenciés et feedback

        Args:
            player: Entity player
            resistance_type: Type résistance (soft/firm/desperate)
            context: Contexte action

        Returns:
            Résultats résistance avec feedback
        """
        stats = player.get_component_of_type(StatsComponent)
        if not stats:
            return {"success": False, "visible_change": False}

        # Paramètres par type résistance
        resistance_params = {
            "soft_resistance": {
                "volonte_gain": 5,
                "success_chance": 0.6,
                "message_success": "Tu arrives à te reprendre un peu...",
                "message_failure": "Ta résistance n'a pas l'effet escompté..."
            },
            "firm_resistance": {
                "volonte_gain": 10,
                "success_chance": 0.8,
                "message_success": "Tu te redresses, retrouvant ta détermination !",
                "message_failure": "Malgré tes efforts, tu n'arrives plus à résister..."
            },
            "desperate_resistance": {
                "volonte_gain": 15,
                "success_chance": 0.4,  # Risqué mais fort gain
                "message_success": "Dans un sursaut de volonté, tu reprends le contrôle !",
                "message_failure": "Ta résistance désespérée ne fait que retarder l'inévitable..."
            }
        }

        params = resistance_params.get(resistance_type, resistance_params["soft_resistance"])

        # Test réussite
        success = random.random() < params["success_chance"]

        # Application selon contexte lieu  
        location = context.get("location", "bar")
        location_bonus = 0
        if location == "bar":
            location_bonus = 3  # Plus facile résister en public
        elif location == "voiture":
            location_bonus = 1
        # salon/chambre: pas de bonus

        if success:
            volonte_gain = params["volonte_gain"] + location_bonus
            stats.apply_modifier("volonte", volonte_gain, source="player_resistance")
            message = params["message_success"]
            visible_change = True
        else:
            # Échec résistance = petit malus volonté
            stats.apply_modifier("volonte", -2, source="resistance_failure")
            message = params["message_failure"]
            visible_change = False

        stats.mark_dirty()

        return {
            "success": success,
            "message": message,
            "resistance_type": resistance_type,
            "visible_change": visible_change,
            "location_bonus": location_bonus
        }

    def _calculate_escalation_level(self, action: str) -> int:
        """Calcule niveau escalation action (1-5)"""
        escalation_map = {
            # Niveau 1 - Actions sociales
            "compliment": 1, "regard_insistant": 1, "conversation_charme": 1,

            # Niveau 2 - Contact léger
            "contact_epaule": 2, "rapprochement_physique": 2,

            # Niveau 3 - Contact modéré 
            "main_cuisse": 3, "caresses_douces": 3,

            # Niveau 4 - Actions intimes
            "baiser_leger": 4, "caresses": 4,

            # Niveau 5 - Actions très intimes
            "baiser_profond": 5, "caresses_intimes": 5, "removal_vetement": 5
        }

        return escalation_map.get(action, 2)  # Default niveau 2

    def _check_threshold_transitions(self, entity: Entity, stats: StatsComponent):
        """Détecte transitions seuils et génère feedback"""

        entity_id = entity.id
        current_thresholds = stats.thresholds.copy()
        last_thresholds = self._last_thresholds.get(entity_id, {})

        # Détection nouveaux seuils atteints
        messages = []
        for threshold_name, is_active in current_thresholds.items():
            was_active = last_thresholds.get(threshold_name, False)

            # Nouveau seuil atteint
            if is_active and not was_active:
                message_key = f"{threshold_name}_entered"
                if message_key in self.threshold_messages:
                    messages.append(self.threshold_messages[message_key])

        # Stockage pour prochaine fois
        self._last_thresholds[entity_id] = current_thresholds

        # Ajout messages au contexte pour affichage
        if messages and hasattr(entity, 'get_component_of_type'):
            dialogue_comp = entity.get_component_of_type(type(None))  # Simplified pour perf
            # Messages seront affichés par game_session

        return messages

    def get_stats_display_text(self, player: Entity) -> Dict[str, str]:
        """Génère texte affichage stats formaté"""

        stats = player.get_component_of_type(StatsComponent)
        if not stats:
            return {"volonte": "???", "excitation": "???", "status": ""}

        # Texte base
        volonte_text = f"{stats.volonte}/100"
        excitation_text = f"{stats.excitation}/100"

        # Indicateurs visuels selon seuils
        status_indicators = []
        if stats.thresholds.get("vulnerable", False):
            status_indicators.append("😰 Vulnérable")
        if stats.thresholds.get("aroused", False):
            status_indicators.append("🔥 Excitée")  
        if stats.thresholds.get("submissive", False):
            status_indicators.append("😵 Soumise")
        if stats.thresholds.get("climax_ready", False):
            status_indicators.append("💥 Au bord...")

        status_text = " | ".join(status_indicators) if status_indicators else ""

        return {
            "volonte": volonte_text,
            "excitation": excitation_text, 
            "status": status_text,
            "has_status": len(status_indicators) > 0
        }

# OPTIMISÉ: Affichage temps réel + équilibrage + feedback seuils
