"""
NPCMale Entity - Entity NPC masculin avec IA adaptative
Personnage non-joueur avec comportement intelligent et évolutif
"""

from core.entity import Entity
from components.personality import PersonalityComponent
from components.dialogue import DialogueComponent
from components.action import ActionComponent
from typing import Dict, Any, List, Optional
import random

class NPCMale(Entity):
    """
    Entity représentant le personnage NPC masculin
    Doté d'une IA adaptative qui évolue selon les interactions
    """

    def __init__(self, personality_type: str = None, name: str = "Marcus"):
        # ID unique pour le NPC
        super().__init__(f"npc_male_{name.lower()}")

        # Configuration personnalité
        self.personality_type = personality_type or random.choice(["patient", "direct", "mixed"])
        self.display_name = name

        # Seed pour cohérence comportementale durant session
        self.behavior_seed = random.randint(1000, 9999)

        # État session
        self.interaction_count = 0
        self.successful_actions = 0
        self.failed_actions = 0

        # Configuration components
        self._setup_components()

    def _setup_components(self):
        """Configuration initiale des components NPC"""

        # PersonalityComponent - Cœur de l'IA adaptative
        personality = PersonalityComponent(
            base_personality=self.personality_type,
            session_seed=self.behavior_seed
        )
        self._configure_personality_traits(personality)
        self.add_component(personality)

        # DialogueComponent - Gestion réponses NPC
        dialogue = DialogueComponent(
            current_scene="seduction_initiale",
            current_location="bar"
        )
        self.add_component(dialogue)

        # ActionComponent - Actions NPC disponibles
        actions = ActionComponent()
        self._setup_npc_actions(actions)
        self.add_component(actions)

    def _configure_personality_traits(self, personality: PersonalityComponent):
        """Configure les traits selon le type de personnalité"""

        if self.personality_type == "patient":
            personality.traits.update({
                "dominance": 0.6,
                "patience": 0.9,
                "charm": 0.8,
                "adaptability": 0.7,
                "persistence": 0.8,
                "subtlety": 0.9,
                "intelligence": 0.8
            })

        elif self.personality_type == "direct":
            personality.traits.update({
                "dominance": 0.9,
                "patience": 0.3,
                "charm": 0.5,
                "adaptability": 0.5,
                "persistence": 0.9,
                "subtlety": 0.4,
                "intelligence": 0.7
            })

        else:  # mixed
            personality.traits.update({
                "dominance": 0.7,
                "patience": 0.6,
                "charm": 0.7,
                "adaptability": 0.8,
                "persistence": 0.7,
                "subtlety": 0.7,
                "intelligence": 0.9
            })

    def _setup_npc_actions(self, action_component: ActionComponent):
        """Configure les actions disponibles pour le NPC"""

        # Actions légères (intensité 1-2)
        action_component.add_action("compliment", success_rate=0.8)
        action_component.add_action("regard_insistant", success_rate=0.7)
        action_component.add_action("conversation_charme", success_rate=0.9)
        action_component.add_action("contact_epaule", success_rate=0.6)

        # Actions escalation modérée (intensité 3-4)
        action_component.add_action("main_cuisse", success_rate=0.5)
        action_component.add_action("baiser_leger", success_rate=0.4)
        action_component.add_action("rapprochement_physique", success_rate=0.6)
        action_component.add_action("caresses_douces", success_rate=0.3)

        # Actions escalation forte (intensité 5+)
        action_component.add_action("baiser_profond", success_rate=0.2)
        action_component.add_action("caresses_intimes", success_rate=0.1)
        action_component.add_action("removal_vetement", success_rate=0.1)

        # Actions adaptatives
        action_component.add_action("patience_tactique", success_rate=0.9)
        action_component.add_action("changement_sujet", success_rate=0.8)
        action_component.add_action("recul_temporaire", success_rate=0.7)

    def choose_next_action(self, player_resistance: float, context: Dict[str, Any]) -> str:
        """
        Choisit la prochaine action selon IA adaptative

        Args:
            player_resistance: Niveau résistance joueur (0.0-1.0)
            context: Contexte actuel (lieu, historique, etc.)

        Returns:
            Nom de l'action choisie
        """
        personality = self.get_component_of_type(PersonalityComponent)
        actions = self.get_component_of_type(ActionComponent)

        if not personality or not actions:
            return "compliment"  # Action de fallback

        # Adaptation comportementale
        personality.adapt_to_resistance(player_resistance, 
                                      success=context.get("last_success", False))

        # Filtrage actions selon niveau escalation autorisé
        available_actions = self._filter_actions_by_escalation(
            actions.possible_actions, 
            player_resistance, 
            context
        )

        if not available_actions:
            return "compliment"

        # Sélection intelligente selon personnalité
        chosen_action = self._intelligent_action_selection(
            available_actions, 
            personality, 
            player_resistance
        )

        # Apprentissage pour futures interactions
        self.interaction_count += 1

        return chosen_action

    def _filter_actions_by_escalation(self, all_actions: List[str], 
                                    resistance: float, 
                                    context: Dict[str, Any]) -> List[str]:
        """Filtre les actions selon le niveau d'escalation approprié"""

        # Définition intensités actions
        action_intensities = {
            "compliment": 1, "conversation_charme": 1, "regard_insistant": 1,
            "contact_epaule": 2, "rapprochement_physique": 2,
            "main_cuisse": 3, "baiser_leger": 3,
            "caresses_douces": 4, "baiser_profond": 4,
            "caresses_intimes": 5, "removal_vetement": 5
        }

        # Niveau escalation maximal selon résistance
        if resistance > 0.8:
            max_intensity = 2  # Actions très douces seulement
        elif resistance > 0.5:
            max_intensity = 3  # Escalation modérée
        elif resistance > 0.2:
            max_intensity = 4  # Escalation forte
        else:
            max_intensity = 5  # Tout autorisé

        # Ajustement selon lieu
        location = context.get("location", "bar")
        if location == "bar":  # Public
            max_intensity = min(max_intensity, 2)
        elif location == "voiture":  # Semi-privé
            max_intensity = min(max_intensity, 4)
        # salon/chambre = pas de limite

        # Filtrage final
        filtered = [
            action for action in all_actions
            if action_intensities.get(action, 1) <= max_intensity
        ]

        return filtered or ["compliment"]  # Toujours une option de fallback

    def _intelligent_action_selection(self, available_actions: List[str], 
                                    personality: PersonalityComponent, 
                                    resistance: float) -> str:
        """Sélection intelligente d'action selon personnalité"""

        action_scores = {}

        for action in available_actions:
            score = 0.5  # Score de base

            # Ajustement selon traits personnalité
            if "charm" in action or "conversation" in action:
                score += personality.traits["charm"] * 0.3

            if "contact" in action or "caresses" in action:
                score += personality.traits["dominance"] * 0.3

            if "patient" in action or "doux" in action:
                score += personality.traits["patience"] * 0.3

            if "leger" in action or "subtil" in action:
                score += personality.traits["subtlety"] * 0.2

            # Bonus expérience apprise
            score += personality.get_action_preference_score(action)

            # Pénalité si action récente (évite répétition)
            if action == context.get("last_action"):
                score -= 0.3

            action_scores[action] = score

        # Sélection avec randomness pondéré
        sorted_actions = sorted(action_scores.items(), key=lambda x: x[1], reverse=True)

        # Top 3 avec probabilités pondérées
        top_actions = sorted_actions[:3]
        if len(top_actions) == 1:
            return top_actions[0][0]

        # Sélection probabiliste favorisant les meilleures actions
        weights = [3, 2, 1] if len(top_actions) >= 3 else [2, 1]
        actions_only = [action for action, score in top_actions]

        return random.choices(actions_only, weights=weights)[0]

    def process_action_result(self, action: str, success: bool, 
                            player_reaction: str = ""):
        """
        Traite le résultat d'une action pour apprentissage

        Args:
            action: Action effectuée
            success: Si l'action a été efficace
            player_reaction: Réaction du joueur
        """
        personality = self.get_component_of_type(PersonalityComponent)

        if personality:
            personality.learn_from_interaction(action, success)

        # Statistiques session
        if success:
            self.successful_actions += 1
        else:
            self.failed_actions += 1

    def get_behavioral_state(self) -> Dict[str, Any]:
        """Retourne l'état comportemental actuel"""
        personality = self.get_component_of_type(PersonalityComponent)

        base_state = {
            "name": self.display_name,
            "personality_type": self.personality_type,
            "interaction_count": self.interaction_count,
            "success_rate": (
                self.successful_actions / max(1, self.interaction_count)
            ),
            "behavior_seed": self.behavior_seed
        }

        if personality:
            base_state.update({
                "current_strategy": personality.strategy_modifier,
                "escalation_rate": personality.escalation_rate,
                "dominant_traits": [
                    trait for trait, value in personality.traits.items() 
                    if value > 0.7
                ],
                "adaptations_made": len(personality.adaptation_history)
            })

        return base_state

    def reset_session_state(self):
        """Remet à zéro l'état de session"""
        self.interaction_count = 0
        self.successful_actions = 0
        self.failed_actions = 0

        personality = self.get_component_of_type(PersonalityComponent)
        if personality:
            personality.reset_adaptation()

    def __repr__(self) -> str:
        success_rate = (
            round((self.successful_actions / max(1, self.interaction_count)) * 100)
        )

        return (f"NPCMale(name={self.display_name}, "
                f"personality={self.personality_type}, "
                f"interactions={self.interaction_count}, "
                f"success_rate={success_rate}%)")
