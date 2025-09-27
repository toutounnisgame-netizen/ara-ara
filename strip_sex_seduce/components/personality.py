"""
PersonalityComponent - Gestion personnalité adaptative NPC
IA comportementale qui s'adapte selon résistance joueur
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from core.component import Component

@dataclass  
class PersonalityComponent(Component):
    """
    Component gérant la personnalité adaptative du NPC
    Traits évolutifs selon les interactions avec le joueur
    """

    # Personnalité de base
    base_personality: str = "patient"  # patient/direct/mixed

    # Traits de base (0.0-1.0)
    traits: Dict[str, float] = field(default_factory=lambda: {
        "dominance": 0.7,           # Tendance à dominer la situation
        "patience": 0.6,            # Patience face à la résistance
        "charm": 0.8,               # Capacité de séduction
        "adaptability": 0.5,        # Adaptation comportementale
        "persistence": 0.7,         # Persévérance face aux refus
        "subtlety": 0.6,            # Préférence actions subtiles
        "intelligence": 0.8         # Intelligence tactique
    })

    # État adaptatif actuel
    strategy_modifier: str = "normal"    # normal/extra_patient/aggressive/retreat
    escalation_rate: float = 1.0         # Multiplicateur vitesse escalation
    current_strategy: str = "seduction"   # seduction/pressure/charm

    # Patterns de réponse selon contexte
    response_patterns: Dict[str, List[str]] = field(default_factory=lambda: {
        "high_resistance": [],      # Actions si résistance forte (>0.8)
        "medium_resistance": [],    # Actions si résistance modérée (0.3-0.8)
        "low_resistance": [],       # Actions si résistance faible (<0.3)
        "retreat": [],              # Actions si échec répétés
        "success": []               # Actions si progression positive
    })

    # Historique adaptation
    adaptation_history: List[Dict[str, Any]] = field(default_factory=list)

    # État session
    session_seed: int = 0                # Seed pour cohérence
    learned_responses: Dict[str, int] = field(default_factory=dict)  # Réponses apprises

    # Compteurs performance
    success_count: int = 0
    failure_count: int = 0
    resistance_encounters: int = 0

    def __post_init__(self):
        """Initialisation après création"""
        super().__init__()
        self._initialize_response_patterns()

    def _initialize_response_patterns(self):
        """Initialise les patterns de base selon la personnalité"""
        if self.base_personality == "patient":
            self.response_patterns.update({
                "high_resistance": ["compliment", "conversation", "patience", "charme_subtil"],
                "medium_resistance": ["contact_leger", "rapprochement", "seduction"],
                "low_resistance": ["escalation_douce", "progression", "confiance"],
                "retreat": ["recul_temporaire", "changement_sujet", "patience_extreme"]
            })
        elif self.base_personality == "direct":
            self.response_patterns.update({
                "high_resistance": ["persistence", "pression_douce", "determination"],
                "medium_resistance": ["escalation", "contact_direct", "assertivite"],
                "low_resistance": ["progression_rapide", "escalation_directe", "dominance"],
                "retreat": ["changement_tactique", "pause_courte", "reaffirmation"]
            })
        else:  # mixed
            self.response_patterns.update({
                "high_resistance": ["adaptation", "lecture_situation", "flexibility"],
                "medium_resistance": ["equilibre", "test_receptivite", "ajustement"],
                "low_resistance": ["opportunisme", "escalation_adaptee", "profiter"],
                "retreat": ["analyse", "changement_complet", "nouvelle_approche"]
            })

    def adapt_to_resistance(self, resistance_level: float, success: bool = False):
        """
        Adapte la personnalité selon le niveau de résistance rencontré

        Args:
            resistance_level: Niveau résistance joueur (0.0-1.0)
            success: Si la dernière action a été un succès
        """
        old_modifier = self.strategy_modifier
        old_rate = self.escalation_rate

        # Comptage pour analytics
        self.resistance_encounters += 1
        if success:
            self.success_count += 1
        else:
            self.failure_count += 1

        # Adaptation selon niveau résistance
        if resistance_level > 0.8:  # Résistance très forte
            if self.traits["adaptability"] > 0.6:
                self.strategy_modifier = "extra_patient"
                self.escalation_rate = max(0.3, self.escalation_rate * 0.7)

                # Augmente patience si adaptatif
                self.traits["patience"] = min(1.0, self.traits["patience"] + 0.05)

        elif resistance_level > 0.5:  # Résistance modérée
            if self.traits["intelligence"] > 0.7:
                self.strategy_modifier = "analytical"
                self.escalation_rate = 0.8

        elif resistance_level < 0.3:  # Faible résistance
            if self.traits["dominance"] > 0.6:
                self.strategy_modifier = "confident"
                self.escalation_rate = min(2.0, self.escalation_rate * 1.2)

                # Augmente dominance si opportuniste
                self.traits["dominance"] = min(1.0, self.traits["dominance"] + 0.03)

        # Adaptation selon succès/échecs répétés
        success_rate = self.success_count / max(1, self.resistance_encounters)

        if success_rate < 0.3 and self.resistance_encounters > 5:
            # Trop d'échecs -> stratégie plus prudente
            self.strategy_modifier = "retreat"
            self.escalation_rate *= 0.6
            self.traits["subtlety"] = min(1.0, self.traits["subtlety"] + 0.1)

        elif success_rate > 0.7:
            # Beaucoup de succès -> plus assertif
            self.strategy_modifier = "aggressive" if self.traits["dominance"] > 0.7 else "confident"
            self.escalation_rate = min(1.5, self.escalation_rate * 1.1)

        # Enregistrement historique adaptation
        if old_modifier != self.strategy_modifier or abs(old_rate - self.escalation_rate) > 0.1:
            self.adaptation_history.append({
                "resistance_level": resistance_level,
                "success": success,
                "old_strategy": old_modifier,
                "new_strategy": self.strategy_modifier,
                "old_rate": old_rate,
                "new_rate": self.escalation_rate,
                "success_rate": success_rate,
                "encounter_count": self.resistance_encounters
            })

            # Limite historique
            if len(self.adaptation_history) > 20:
                self.adaptation_history = self.adaptation_history[-15:]

        self.mark_dirty()

    def get_preferred_actions(self, resistance_level: float) -> List[str]:
        """
        Retourne les actions préférées selon niveau résistance

        Args:
            resistance_level: Niveau résistance actuel (0.0-1.0)

        Returns:
            Liste des actions recommandées
        """
        if resistance_level > 0.8:
            return self.response_patterns["high_resistance"]
        elif resistance_level > 0.3:
            return self.response_patterns["medium_resistance"]
        else:
            return self.response_patterns["low_resistance"]

    def learn_from_interaction(self, action: str, success: bool):
        """
        Apprend des interactions précédentes

        Args:
            action: Action tentée
            success: Si l'action a été efficace
        """
        if action not in self.learned_responses:
            self.learned_responses[action] = 0

        # Pondération apprentissage
        if success:
            self.learned_responses[action] += 2
        else:
            self.learned_responses[action] -= 1

        # Évite les valeurs extrêmes
        self.learned_responses[action] = max(-5, min(10, self.learned_responses[action]))

        self.mark_dirty()

    def get_action_preference_score(self, action: str) -> float:
        """
        Retourne le score de préférence pour une action
        Combine traits de base et expérience apprise

        Returns:
            Score entre -1.0 et 2.0
        """
        # Score de base selon traits
        base_score = 0.5

        # Ajustements selon traits personnalité
        if "contact" in action and self.traits["dominance"] > 0.7:
            base_score += 0.3
        if "subtil" in action and self.traits["subtlety"] > 0.7:
            base_score += 0.4
        if "charm" in action and self.traits["charm"] > 0.7:
            base_score += 0.3

        # Score appris
        learned_score = self.learned_responses.get(action, 0) * 0.1

        return base_score + learned_score

    def reset_adaptation(self):
        """Remet l'adaptation à l'état initial"""
        self.strategy_modifier = "normal"
        self.escalation_rate = 1.0
        self.success_count = 0
        self.failure_count = 0
        self.resistance_encounters = 0
        self.learned_responses.clear()
        self.adaptation_history.clear()
        self.mark_dirty()

    def get_personality_summary(self) -> Dict[str, Any]:
        """Retourne un résumé de l'état personnalité"""
        return {
            "base_type": self.base_personality,
            "current_strategy": self.strategy_modifier,
            "escalation_rate": round(self.escalation_rate, 2),
            "dominant_traits": {
                trait: round(value, 2) 
                for trait, value in self.traits.items() 
                if value > 0.7
            },
            "success_rate": round(self.success_count / max(1, self.resistance_encounters), 2),
            "adaptations_count": len(self.adaptation_history),
            "learned_actions": len(self.learned_responses)
        }

    def to_dict(self) -> Dict[str, Any]:
        """Sérialisation complète du component"""
        base_dict = super().to_dict()
        base_dict.update({
            "personality_summary": self.get_personality_summary(),
            "traits": {k: round(v, 2) for k, v in self.traits.items()},
            "strategy_modifier": self.strategy_modifier,
            "escalation_rate": round(self.escalation_rate, 2),
            "performance": {
                "success_count": self.success_count,
                "failure_count": self.failure_count,
                "encounters": self.resistance_encounters
            }
        })
        return base_dict
