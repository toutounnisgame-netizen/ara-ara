"""
NPCMale V2.0 - IA adaptative avec feedback visible
Correctif: Adaptation comportementale visible + variabilité actions
"""

from core.entity import Entity
from components.personality import PersonalityComponent
from components.dialogue import DialogueComponent
from components.action import ActionComponent
from typing import Dict, Any, List, Optional, Tuple
import random

class NPCMale(Entity):
    """NPC masculin avec IA adaptative avancée et feedback visible"""

    def __init__(self, personality_type: str = None, name: str = "Marcus"):
        super().__init__(f"npc_male_{name.lower()}")

        # Configuration personnalité avec seed cohérence
        self.personality_type = personality_type or random.choice(["patient", "direct", "mixed"])
        self.display_name = name
        self.behavior_seed = random.randint(1000, 9999)

        # État session avec tracking détaillé
        self.interaction_count = 0
        self.successful_actions = 0
        self.failed_actions = 0

        # NOUVEAU V2.0: Historique adaptation pour feedback
        self.adaptation_history = []
        self.last_strategy_announced = None

        # Pool actions par intensité pour escalation
        self.action_pools = {
            1: ["compliment", "regard_insistant", "conversation_charme"],
            2: ["contact_epaule", "rapprochement_physique"],
            3: ["main_cuisse", "caresses_douces"],
            4: ["baiser_leger", "caresses"],
            5: ["baiser_profond", "caresses_intimes", "removal_vetement"]
        }

        # Niveau escalation actuel
        self.current_escalation_level = 1

        # Dernières actions pour éviter répétitions
        self._recent_actions = []

        self._setup_components()

    def _setup_components(self):
        """Configuration components avec personnalité différenciée"""

        # PersonalityComponent avec traits spécialisés
        personality = PersonalityComponent(
            base_personality=self.personality_type,
            session_seed=self.behavior_seed
        )
        self._configure_personality_traits(personality)
        self.add_component(personality)

        # DialogueComponent
        dialogue = DialogueComponent(
            current_scene="seduction_initiale",
            current_location="bar"
        )
        self.add_component(dialogue)

        # ActionComponent avec actions par niveau
        actions = ActionComponent()
        self._setup_npc_actions(actions)
        self.add_component(actions)

    def _configure_personality_traits(self, personality: PersonalityComponent):
        """Configuration traits différenciés par personnalité"""

        if self.personality_type == "patient":
            personality.traits.update({
                "dominance": 0.5,      # Moins dominant
                "patience": 0.95,      # Très patient
                "charm": 0.9,          # Très charmeur
                "adaptability": 0.8,   # Très adaptable
                "persistence": 0.7,    # Modérément persistant
                "subtlety": 0.95,      # Très subtil
                "intelligence": 0.9    # Très intelligent
            })

        elif self.personality_type == "direct":
            personality.traits.update({
                "dominance": 0.95,     # Très dominant
                "patience": 0.2,       # Peu patient
                "charm": 0.6,          # Charme moyen
                "adaptability": 0.4,   # Peu adaptable
                "persistence": 0.95,   # Très persistant
                "subtlety": 0.3,       # Peu subtil
                "intelligence": 0.7    # Intelligence moyenne
            })

        else:  # mixed - Équilibré et intelligent
            personality.traits.update({
                "dominance": 0.7,      # Dominant modéré
                "patience": 0.6,       # Patience moyenne
                "charm": 0.8,          # Bon charme
                "adaptability": 0.95,  # Très adaptable (signature)
                "persistence": 0.7,    # Persistence modérée
                "subtlety": 0.7,       # Subtilité modérée
                "intelligence": 0.95   # Très intelligent (signature)
            })

    def _setup_npc_actions(self, action_component: ActionComponent):
        """Setup actions avec escalation intelligente"""

        # Toutes actions disponibles par défaut
        all_actions = []
        for level_actions in self.action_pools.values():
            all_actions.extend(level_actions)

        for action in all_actions:
            # Success rate basé sur niveau escalation et personnalité
            base_rate = 0.5
            action_component.add_action(action, success_rate=base_rate)

    def choose_next_action(self, player_resistance: float, 
                          context: Dict[str, Any]) -> Tuple[str, Optional[str]]:
        """
        Choix action avec IA adaptative VISIBLE et feedback

        Returns:
            Tuple (action, message_adaptation) où message_adaptation peut être None
        """
        personality = self.get_component_of_type(PersonalityComponent)
        if not personality:
            return "compliment", None

        # ADAPTATION avec feedback visible
        old_strategy = personality.strategy_modifier
        old_escalation_rate = personality.escalation_rate

        # Adaptation selon résistance avec feedback
        personality.adapt_to_resistance(
            player_resistance, 
            success=context.get("last_success", False)
        )

        new_strategy = personality.strategy_modifier
        adaptation_message = None

        # FEEDBACK ADAPTATION VISIBLE
        if old_strategy != new_strategy and new_strategy != self.last_strategy_announced:
            adaptation_message = self._generate_adaptation_message(old_strategy, new_strategy)
            self.last_strategy_announced = new_strategy

            # Historique pour analytics
            self.adaptation_history.append({
                "from": old_strategy,
                "to": new_strategy,
                "resistance_level": player_resistance,
                "interaction_count": self.interaction_count
            })

        # SÉLECTION ACTION avec escalation intelligente
        chosen_action = self._intelligent_action_selection(
            player_resistance, 
            personality, 
            context
        )

        # Update historique actions récentes
        self._recent_actions.append(chosen_action)
        if len(self._recent_actions) > 3:
            self._recent_actions.pop(0)

        self.interaction_count += 1

        return chosen_action, adaptation_message

    def _generate_adaptation_message(self, old_strategy: str, new_strategy: str) -> str:
        """Génère message adaptation visible selon personnalité"""

        # Messages selon personnalité du NPC
        if self.personality_type == "patient":
            messages = {
                ("normal", "extra_patient"): f"{self.display_name} semble ralentir, observant tes réactions avec plus d'attention...",
                ("normal", "confident"): f"Tu sens {self.display_name} gagner en assurance, ses gestes deviennent plus sûrs...",
                ("extra_patient", "normal"): f"{self.display_name} reprend un rythme plus naturel, encouragé par tes réactions...",
                ("confident", "extra_patient"): f"Face à ta résistance, {self.display_name} redevient plus prudent et attentionné..."
            }
        elif self.personality_type == "direct":
            messages = {
                ("normal", "aggressive"): f"{self.display_name} devient plus insistant, sa patience semble s'amenuiser...",
                ("normal", "confident"): f"Il gagne en assurance, son approche devient plus directe...",
                ("aggressive", "normal"): f"Il modère légèrement son approche, mais reste déterminé...",
                ("confident", "aggressive"): f"Sa confiance se mue en détermination plus affirmée..."
            }
        else:  # mixed
            messages = {
                ("normal", "extra_patient"): f"{self.display_name} ajuste sa stratégie, devenant plus attentif à tes réactions...",
                ("normal", "confident"): f"Tu le vois analyser la situation et adapter son approche...",
                ("normal", "aggressive"): f"Il change de tactique, devenant plus direct dans ses intentions...",
                ("extra_patient", "confident"): f"Sentant une ouverture, il devient plus entreprenant...",
                ("confident", "extra_patient"): f"Il réévalue la situation et revient à une approche plus mesurée..."
            }

        return messages.get((old_strategy, new_strategy), "")

    def _intelligent_action_selection(self, player_resistance: float, 
                                    personality: PersonalityComponent,
                                    context: Dict[str, Any]) -> str:
        """Sélection action avec IA avancée et escalation"""

        # Ajustement niveau escalation selon résistance
        if player_resistance > 0.8:  # Résistance forte
            # Rester à niveau bas ou descendre
            self.current_escalation_level = min(2, self.current_escalation_level)
        elif player_resistance > 0.5:  # Résistance modérée
            # Escalation prudente
            if personality.traits["patience"] > 0.7:
                self.current_escalation_level = min(3, self.current_escalation_level)
            else:
                self.current_escalation_level = min(4, self.current_escalation_level + 1)
        elif player_resistance > 0.2:  # Faible résistance
            # Escalation plus agressive
            if personality.traits["dominance"] > 0.7:
                self.current_escalation_level = min(5, self.current_escalation_level + 1)
            else:
                self.current_escalation_level = min(4, self.current_escalation_level + 1)
        else:  # Très faible résistance
            # Escalation maximale selon personnalité
            if personality.traits["persistence"] > 0.8:
                self.current_escalation_level = 5
            else:
                self.current_escalation_level = min(5, self.current_escalation_level + 1)

        # Ajustement selon lieu
        location = context.get("location", "bar")
        max_escalation_by_location = {
            "bar": 2,      # Public - actions discrètes seulement
            "voiture": 4,  # Semi-privé
            "salon": 4,    # Privé
            "chambre": 5   # Intime - tout autorisé
        }

        max_allowed = max_escalation_by_location.get(location, 2)
        effective_escalation = min(self.current_escalation_level, max_allowed)

        # Pool actions possibles
        possible_actions = []
        for level in range(1, effective_escalation + 1):
            possible_actions.extend(self.action_pools.get(level, []))

        # Filtrage actions récentes pour éviter répétition
        filtered_actions = [a for a in possible_actions if a not in self._recent_actions[-2:]]
        if not filtered_actions:
            filtered_actions = possible_actions  # Fallback si tout récent

        # Sélection avec préférences personnalité
        action_scores = {}
        for action in filtered_actions:
            score = 0.5  # Base score

            # Bonus selon traits personnalité
            if "charme" in action or "conversation" in action:
                score += personality.traits["charm"] * 0.3

            if "contact" in action or "caresse" in action:
                score += personality.traits["dominance"] * 0.3

            if "leger" in action or action in ["compliment", "regard_insistant"]:
                score += personality.traits["subtlety"] * 0.2

            # Bonus expérience apprise
            score += personality.get_action_preference_score(action)

            # Malus si action très récente
            if action == self._recent_actions[-1:]:
                score -= 0.4

            action_scores[action] = score

        # Sélection avec randomness pondéré
        if not action_scores:
            return "compliment"  # Fallback sécurisé

        # Top 3 actions avec probabilités
        sorted_actions = sorted(action_scores.items(), key=lambda x: x[1], reverse=True)
        top_actions = sorted_actions[:min(3, len(sorted_actions))]

        if len(top_actions) == 1:
            return top_actions[0][0]

        # Sélection probabiliste
        actions_only = [action for action, score in top_actions]
        weights = [3, 2, 1] if len(top_actions) >= 3 else [2, 1]

        return random.choices(actions_only, weights=weights[:len(actions_only)])[0]

    def process_action_result(self, action: str, success: bool, 
                            player_reaction: str = ""):
        """Traite résultat action pour apprentissage IA"""

        personality = self.get_component_of_type(PersonalityComponent)
        if personality:
            personality.learn_from_interaction(action, success)

        # Stats session
        if success:
            self.successful_actions += 1
        else:
            self.failed_actions += 1

    def get_behavioral_state(self) -> Dict[str, Any]:
        """État comportemental avec info adaptation visible"""

        personality = self.get_component_of_type(PersonalityComponent)
        success_rate = self.successful_actions / max(1, self.interaction_count) if self.interaction_count > 0 else 0

        state = {
            "name": self.display_name,
            "personality_type": self.personality_type,
            "interaction_count": self.interaction_count,
            "success_rate": success_rate,
            "current_escalation": self.current_escalation_level,
            "recent_actions": self._recent_actions.copy(),
            "adaptations_made": len(self.adaptation_history)
        }

        if personality:
            state.update({
                "current_strategy": personality.strategy_modifier,
                "escalation_rate": personality.escalation_rate,
                "dominant_traits": [
                    trait for trait, value in personality.traits.items() 
                    if value > 0.8
                ]
            })

        return state

    def get_adaptation_summary(self) -> List[str]:
        """Résumé adaptations visibles pour debug"""

        if not self.adaptation_history:
            return ["Aucune adaptation comportementale encore."]

        summary = []
        for adaptation in self.adaptation_history[-3:]:  # 3 dernières
            summary.append(
                f"Tour {adaptation['interaction_count']}: "
                f"{adaptation['from']} → {adaptation['to']} "
                f"(résistance: {adaptation['resistance_level']:.1%})"
            )

        return summary

    def reset_session_state(self):
        """Reset état session pour nouvelle partie"""

        self.interaction_count = 0
        self.successful_actions = 0
        self.failed_actions = 0
        self.current_escalation_level = 1
        self._recent_actions.clear()
        self.adaptation_history.clear()
        self.last_strategy_announced = None

        personality = self.get_component_of_type(PersonalityComponent)
        if personality:
            personality.reset_adaptation()

    def __repr__(self) -> str:
        success_rate = round((self.successful_actions / max(1, self.interaction_count)) * 100)
        return (f"NPCMale(name={self.display_name}, "
                f"personality={self.personality_type}, "
                f"escalation={self.current_escalation_level}, "
                f"success_rate={success_rate}%)")

# IA AVANCÉE: Feedback visible + escalation intelligente + variabilité
