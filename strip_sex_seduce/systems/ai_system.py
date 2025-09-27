"""
AISystem V2.0 - Coordination IA adaptative avancée
Correctif: Orchestration IA + feedback + analytics
"""

from core.system import System
from core.entity import Entity
from components.personality import PersonalityComponent
from entities.npc import NPCMale
from entities.player import PlayerCharacter
from typing import List, Dict, Any, Optional

class AISystem(System):
    """System orchestrant l'IA adaptative avec analytics avancées"""

    def __init__(self):
        super().__init__("AISystem")

        # Analytics comportement pour optimisation
        self.behavior_analytics = {
            "total_adaptations": 0,
            "adaptations_by_type": {},
            "effectiveness_by_personality": {
                "patient": {"successes": 0, "attempts": 0},
                "direct": {"successes": 0, "attempts": 0}, 
                "mixed": {"successes": 0, "attempts": 0}
            },
            "resistance_responses": []
        }

        # Seuils adaptation pour fine-tuning
        self.adaptation_thresholds = {
            "high_resistance": 0.7,      # Résistance forte
            "medium_resistance": 0.4,    # Résistance modérée
            "adaptation_sensitivity": 3   # Actions avant adaptation
        }

    def update(self, entities: List[Entity], delta_time: float = 0.0, **kwargs):
        """Update IA avec analytics et optimisation continue"""

        player = kwargs.get("player")
        game_state = kwargs.get("game_state")

        if not player or not game_state:
            return

        # Traitement tous NPCs
        for entity in entities:
            if isinstance(entity, NPCMale):
                self._update_npc_ai(entity, player, game_state)

    def _update_npc_ai(self, npc: NPCMale, player: PlayerCharacter, game_state):
        """Update IA spécifique NPC avec analytics"""

        personality = npc.get_component_of_type(PersonalityComponent)
        if not personality:
            return

        # Récupération métriques performance
        player_resistance = player.get_resistance_level()
        npc_state = npc.get_behavioral_state()

        # Analytics adaptation
        self._analyze_adaptation_effectiveness(npc, player_resistance)

        # Optimisation traits selon performance
        self._optimize_personality_traits(personality, npc_state)

        # Prédiction actions futures
        self._update_action_predictions(npc, player)

    def _analyze_adaptation_effectiveness(self, npc: NPCMale, resistance: float):
        """Analyse effectiveness adaptations pour amélioration"""

        # Tracking adaptations par résistance
        resistance_category = "high" if resistance > 0.7 else "medium" if resistance > 0.3 else "low"

        adaptation_data = {
            "npc_personality": npc.personality_type,
            "resistance_level": resistance,
            "resistance_category": resistance_category,
            "escalation_level": npc.current_escalation_level,
            "success_rate": npc.successful_actions / max(1, npc.interaction_count)
        }

        self.behavior_analytics["resistance_responses"].append(adaptation_data)

        # Limite historique pour performance
        if len(self.behavior_analytics["resistance_responses"]) > 50:
            self.behavior_analytics["resistance_responses"] =                 self.behavior_analytics["resistance_responses"][-30:]

    def _optimize_personality_traits(self, personality: PersonalityComponent, 
                                   npc_state: Dict[str, Any]):
        """Optimisation fine traits selon performance"""

        success_rate = npc_state.get("success_rate", 0.5)
        interaction_count = npc_state.get("interaction_count", 0)

        # Optimisation seulement après expérience suffisante
        if interaction_count < 5:
            return

        # Ajustements selon performance
        if success_rate < 0.3:  # Performance faible
            # Augmente adaptabilité et patience
            personality.traits["adaptability"] = min(1.0, personality.traits["adaptability"] + 0.05)
            personality.traits["patience"] = min(1.0, personality.traits["patience"] + 0.03)

        elif success_rate > 0.8:  # Performance excellente
            # Augmente confiance (dominance)
            personality.traits["dominance"] = min(1.0, personality.traits["dominance"] + 0.02)

        # Sauvegarde modification
        personality.mark_dirty()

    def _update_action_predictions(self, npc: NPCMale, player: PlayerCharacter):
        """Update prédictions actions pour cohérence"""

        # Pas d'implémentation critique pour performance
        # Placeholder pour expansion future
        pass

    def generate_ai_insights(self) -> Dict[str, Any]:
        """Génère insights comportement pour debug/analytics"""

        if not self.behavior_analytics["resistance_responses"]:
            return {"status": "Pas assez de données"}

        responses = self.behavior_analytics["resistance_responses"]

        # Analytics par personnalité
        personality_performance = {}
        for response in responses:
            p_type = response["npc_personality"]
            if p_type not in personality_performance:
                personality_performance[p_type] = []
            personality_performance[p_type].append(response["success_rate"])

        # Moyennes par personnalité
        personality_averages = {}
        for p_type, rates in personality_performance.items():
            personality_averages[p_type] = sum(rates) / len(rates)

        # Analytics par niveau résistance
        resistance_patterns = {}
        for response in responses:
            r_cat = response["resistance_category"]
            if r_cat not in resistance_patterns:
                resistance_patterns[r_cat] = []
            resistance_patterns[r_cat].append(response["success_rate"])

        resistance_averages = {}
        for r_cat, rates in resistance_patterns.items():
            resistance_averages[r_cat] = sum(rates) / len(rates)

        return {
            "total_interactions": len(responses),
            "personality_performance": personality_averages,
            "resistance_patterns": resistance_averages,
            "adaptation_count": self.behavior_analytics["total_adaptations"],
            "best_personality": max(personality_averages.items(), key=lambda x: x[1]) if personality_averages else None
        }

    def get_ai_status_for_display(self, npc: NPCMale) -> str:
        """Status IA formaté pour affichage utilisateur"""

        state = npc.get_behavioral_state()
        personality = npc.get_component_of_type(PersonalityComponent)

        if not personality:
            return ""

        # Formatage pour utilisateur
        strategy_names = {
            "normal": "Équilibré",
            "extra_patient": "Très patient",
            "confident": "Confiant", 
            "aggressive": "Insistant",
            "retreat": "Prudent"
        }

        strategy_display = strategy_names.get(personality.strategy_modifier, "Adaptatif")

        status_parts = []
        status_parts.append(f"Stratégie: {strategy_display}")

        if state["success_rate"] > 0.7:
            status_parts.append("(Efficace)")
        elif state["success_rate"] < 0.3:
            status_parts.append("(En difficulté)")

        if state["adaptations_made"] > 0:
            status_parts.append(f"• {state['adaptations_made']} adaptations")

        return " ".join(status_parts)

    def reset_analytics(self):
        """Reset analytics pour nouvelle session"""

        self.behavior_analytics = {
            "total_adaptations": 0,
            "adaptations_by_type": {},
            "effectiveness_by_personality": {
                "patient": {"successes": 0, "attempts": 0},
                "direct": {"successes": 0, "attempts": 0},
                "mixed": {"successes": 0, "attempts": 0}
            },
            "resistance_responses": []
        }

# SYSTÈME IA: Analytics + optimisation + insights pour amélioration continue
