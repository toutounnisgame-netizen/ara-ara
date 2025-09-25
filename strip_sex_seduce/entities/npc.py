"""
NPCMale V2.0 - IA adaptative complète avec feedback visible
Personnalité évolutive et adaptation comportementale
"""

from core.entity import Entity
from components.personality import PersonalityComponent
from components.action import ActionComponent
from typing import Dict, List, Any, Tuple, Optional
import random
import time

class NPCMale(Entity):
    """NPC masculin avec IA adaptative avancée et feedback utilisateur"""

    def __init__(self, personality_type: str = "mixed"):
        super().__init__("npc_male")

        # Identification
        self.personality_type = personality_type
        self.display_name = "Marcus"  # Nom par défaut

        # État comportemental
        self.interaction_count = 0
        self.successful_actions = 0
        self.failed_actions = 0
        self.current_escalation_level = 1

        # Historique adaptation pour IA
        self.resistance_history = []
        self.action_history = []
        self.adaptation_messages = []

        # État session
        self.adaptations_made = 0
        self.current_strategy = "normal"
        self.last_adaptation_time = 0

        # Setup components
        self._setup_personality(personality_type)
        self._setup_actions()

    def _setup_personality(self, personality_type: str):
        """Configure personnalité selon type"""

        personality_configs = {
            "patient": {
                "traits": {
                    "dominance": 0.4,
                    "patience": 0.9,
                    "charm": 0.8,
                    "adaptability": 0.7,
                    "persistence": 0.6,
                    "subtlety": 0.8
                },
                "strategy_preferences": ["gentle", "persistent", "charming"]
            },
            "direct": {
                "traits": {
                    "dominance": 0.8,
                    "patience": 0.3,
                    "charm": 0.6,
                    "adaptability": 0.4,
                    "persistence": 0.9,
                    "subtlety": 0.2
                },
                "strategy_preferences": ["confident", "direct", "escalation"]
            },
            "mixed": {
                "traits": {
                    "dominance": 0.6,
                    "patience": 0.5,
                    "charm": 0.7,
                    "adaptability": 0.8,
                    "persistence": 0.7,
                    "subtlety": 0.5
                },
                "strategy_preferences": ["adaptive", "balanced", "responsive"]
            }
        }

        config = personality_configs.get(personality_type, personality_configs["mixed"])

        personality = PersonalityComponent()
        personality.traits.update(config["traits"])
        personality.base_personality = personality_type
        personality.strategy_preferences = config["strategy_preferences"]

        self.add_component(personality)

    def _setup_actions(self):
        """Configure actions disponibles"""

        actions = ActionComponent()

        # Actions par niveau escalation
        action_sets = {
            1: ["compliment", "conversation_charme", "regard_insistant"],
            2: ["contact_epaule", "rapprochement_physique"],
            3: ["main_cuisse", "caresses_douces"],
            4: ["baiser_leger", "caresses"],
            5: ["baiser_profond", "caresses_intimes"]
        }

        for level, action_list in action_sets.items():
            for action in action_list:
                actions.add_action(action, success_rate=0.7)

        self.add_component(actions)

    def choose_next_action(self, player_resistance: float, 
                          context: Dict[str, Any]) -> Tuple[str, Optional[str]]:
        """
        IA adaptative choix action + message adaptation visible

        Args:
            player_resistance: Niveau résistance 0.0-1.0
            context: Contexte environnement/historique

        Returns:
            Tuple (action_choisie, message_adaptation_ou_None)
        """

        # Enregistrement pour analytics
        self.resistance_history.append(player_resistance)
        self.interaction_count += 1

        # Limite historique pour performance
        if len(self.resistance_history) > 10:
            self.resistance_history = self.resistance_history[-5:]

        # ANALYSE ADAPTATION NÉCESSAIRE
        adaptation_message = self._analyze_need_adaptation(player_resistance, context)

        # CHOIX ACTION selon stratégie actuelle
        chosen_action = self._select_action_by_strategy(player_resistance, context)

        # Historique action
        self.action_history.append({
            "action": chosen_action,
            "resistance": player_resistance,
            "escalation": self.current_escalation_level,
            "timestamp": time.time()
        })

        return chosen_action, adaptation_message

    def _analyze_need_adaptation(self, resistance: float, context: Dict) -> Optional[str]:
        """Analyse si adaptation nécessaire et génère message"""

        # Pas d'adaptation les 2 premiers tours
        if self.interaction_count < 3:
            return None

        # Analyse tendance résistance sur dernières actions
        if len(self.resistance_history) >= 3:
            recent_resistance = self.resistance_history[-3:]
            avg_resistance = sum(recent_resistance) / len(recent_resistance)

            personality = self.get_component_of_type(PersonalityComponent)
            if not personality:
                return None

            adaptation_threshold = 0.7  # Seuil adaptation

            # RÉSISTANCE FORTE -> Adaptation patience
            if avg_resistance > adaptation_threshold and self.current_strategy != "extra_patient":
                self.current_strategy = "extra_patient"
                self.adaptations_made += 1

                # Message selon personnalité
                if self.personality_type == "patient":
                    return "Tu le sens qui ralentit le rythme, devenant encore plus attentionné..."
                elif self.personality_type == "direct":
                    return "Il prend une grande inspiration, visiblement en train de réévaluer son approche..."
                else:  # mixed
                    return "Marcus devient plus patient, ajustant sa stratégie à ta résistance..."

            # RÉSISTANCE FAIBLE -> Adaptation confiance  
            elif avg_resistance < 0.3 and self.current_strategy != "confident":
                self.current_strategy = "confident"
                self.adaptations_made += 1

                if self.personality_type == "direct":
                    return "Tu sens une nouvelle assurance dans ses gestes, plus déterminé..."
                elif self.personality_type == "patient":
                    return "Il devient plus entreprenant, encouragé par ta réceptivité..."
                else:  # mixed
                    return "Marcus s'enhardis, sentant que tu es plus réceptive..."

            # RÉSISTANCE VARIABLE -> Adaptation équilibrée
            elif len(set(recent_resistance)) >= 2 and self.current_strategy != "adaptive":
                self.current_strategy = "adaptive"
                self.adaptations_made += 1

                return "Il semble analyser tes réactions, adaptant son comportement en temps réel..."

        return None

    def _select_action_by_strategy(self, resistance: float, context: Dict) -> str:
        """Sélectionne action selon stratégie adaptée"""

        location = context.get("location", "bar")

        # ACTIONS SELON STRATÉGIE ACTUELLE
        if self.current_strategy == "extra_patient":
            # Stratégie patience - actions douces
            if resistance > 0.7:
                actions = ["compliment", "conversation_charme"]
            else:
                actions = ["regard_insistant", "contact_epaule"]

        elif self.current_strategy == "confident":
            # Stratégie confiance - escalation plus rapide
            if resistance < 0.3:
                actions = ["rapprochement_physique", "main_cuisse", "caresses_douces"]
            else:
                actions = ["contact_epaule", "rapprochement_physique"]

        elif self.current_strategy == "adaptive":
            # Stratégie adaptive - selon contexte
            if resistance > 0.6:
                actions = ["compliment", "conversation_charme"]
            elif resistance > 0.3:
                actions = ["contact_epaule", "rapprochement_physique"]
            else:
                actions = ["main_cuisse", "caresses_douces"]

        else:  # strategy normale
            # Choix standard selon résistance
            if resistance > 0.7:
                actions = ["compliment", "conversation_charme", "regard_insistant"]
            elif resistance > 0.4:
                actions = ["contact_epaule", "rapprochement_physique"]
            else:
                actions = ["main_cuisse", "caresses_douces"]

        # FILTRAGE SELON LIEU (contraintes sociales)
        if location == "bar":
            # En public - actions limitées
            allowed_public = ["compliment", "conversation_charme", "regard_insistant", "contact_epaule"]
            actions = [a for a in actions if a in allowed_public]

        # Sélection finale
        if not actions:
            actions = ["compliment"]  # Fallback sûr

        return random.choice(actions)

    def get_behavioral_state(self) -> Dict[str, Any]:
        """État comportemental complet pour analytics et debug"""

        success_rate = 0.0
        if self.interaction_count > 0:
            success_rate = self.successful_actions / self.interaction_count

        return {
            "name": self.display_name,
            "personality_type": self.personality_type,
            "interaction_count": self.interaction_count,
            "success_rate": success_rate,
            "current_escalation": self.current_escalation_level,
            "recent_actions": self.action_history[-3:] if self.action_history else [],
            "adaptations_made": self.adaptations_made,
            "current_strategy": self.current_strategy,
            "escalation_rate": 1.0,
            "avg_resistance_faced": sum(self.resistance_history) / len(self.resistance_history) if self.resistance_history else 0.5,
            "dominant_traits": self._get_dominant_traits()
        }

    def _get_dominant_traits(self) -> List[str]:
        """Retourne traits dominants pour affichage"""

        personality = self.get_component_of_type(PersonalityComponent)
        if not personality:
            return ["charme"]

        # Tri traits par valeur
        sorted_traits = sorted(personality.traits.items(), key=lambda x: x[1], reverse=True)

        return [trait[0] for trait in sorted_traits[:2]]

    def record_action_result(self, success: bool):
        """Enregistre résultat d'une action pour analytics"""

        if success:
            self.successful_actions += 1
        else:
            self.failed_actions += 1

    def to_dict(self) -> Dict[str, Any]:
        """Sérialisation enrichie"""

        base_dict = super().to_dict()
        base_dict.update({
            "personality_type": self.personality_type,
            "display_name": self.display_name,
            "interaction_count": self.interaction_count,
            "adaptations_made": self.adaptations_made,
            "current_strategy": self.current_strategy
        })
        return base_dict

# NPC V2.0: IA adaptative + feedback visible + personnalité évolutive
