"""
PlayerCharacter Entity - Entity joueur avec components spécialisés
Représente le personnage contrôlé par l'utilisateur
"""

from core.entity import Entity
from components.stats import StatsComponent
from components.clothing import ClothingComponent
from components.dialogue import DialogueComponent
from components.action import ActionComponent
from typing import Dict, Any

class PlayerCharacter(Entity):
    """
    Entity représentant le personnage joueur
    Préconfiguré avec les components essentiels au gameplay
    """

    def __init__(self, name: str = "Joueuse"):
        # ID unique pour le joueur
        super().__init__(f"player_{name.lower().replace(' ', '_')}")

        # Traits de personnalité fixes du joueur
        self.personality_traits = {
            "submissiveness": 0.7,      # Tendance soumission
            "curiosity": 0.6,           # Curiosité pour nouvelles expériences
            "resistance_willpower": 0.8, # Force de volonté de base
            "shyness": 0.7,             # Niveau timidité
            "adventurousness": 0.5      # Goût pour l'aventure
        }

        # Nom d'affichage
        self.display_name = name

        # Ajout des components obligatoires
        self._setup_components()

    def _setup_components(self):
        """Configuration initiale des components"""

        # StatsComponent - État résistance/excitation
        stats = StatsComponent(
            volonte=100,        # Résistance maximale au début
            excitation=0        # Pas d'excitation initiale
        )
        self.add_component(stats)

        # ClothingComponent - Tenue initiale conservatrice
        clothing = ClothingComponent(
            initial_outfit="conservatrice"
        )
        self.add_component(clothing)

        # DialogueComponent - Interface dialogue
        dialogue = DialogueComponent(
            current_scene="introduction",
            current_location="bar"
        )
        self.add_component(dialogue)

        # ActionComponent - Actions joueur de base
        actions = ActionComponent()
        self._setup_player_actions(actions)
        self.add_component(actions)

    def _setup_player_actions(self, action_component: ActionComponent):
        """Configure les actions de base du joueur"""

        # Actions défensives
        action_component.add_action("resist_soft", 
            cost={"volonte": +5}, 
            success_rate=0.7)
        action_component.add_action("resist_firm", 
            cost={"volonte": +10}, 
            success_rate=0.9)

        # Actions permissives
        action_component.add_action("allow", 
            cost={"volonte": -5, "excitation": +3}, 
            success_rate=1.0)
        action_component.add_action("encourage", 
            cost={"volonte": -10, "excitation": +8}, 
            success_rate=1.0)

        # Actions de fuite
        action_component.add_action("escape_attempt", 
            cost={"volonte": +15}, 
            success_rate=0.3)  # Difficile de fuir
        action_component.add_action("create_excuse", 
            cost={"volonte": +5}, 
            success_rate=0.6)

        # Actions sociales
        action_component.add_action("deflect_conversation", 
            success_rate=0.5)
        action_component.add_action("nervous_laugh", 
            success_rate=0.8)

    def get_resistance_level(self) -> float:
        """Retourne le niveau de résistance normalisé (0.0-1.0)"""
        stats = self.get_component_of_type(StatsComponent)
        if stats:
            return stats.get_resistance_level()
        return 1.0  # Résistance maximale par défaut

    def get_arousal_level(self) -> float:
        """Retourne le niveau d'excitation normalisé (0.0-1.0)"""
        stats = self.get_component_of_type(StatsComponent)
        if stats:
            return stats.get_arousal_level()
        return 0.0

    def is_vulnerable(self) -> bool:
        """Vérifie si le joueur est dans un état vulnérable"""
        stats = self.get_component_of_type(StatsComponent)
        if stats:
            return stats.is_in_threshold("vulnerable")
        return False

    def is_highly_aroused(self) -> bool:
        """Vérifie si le joueur est très excité"""
        stats = self.get_component_of_type(StatsComponent)
        if stats:
            return stats.is_in_threshold("aroused")
        return False

    def get_clothing_exposure(self) -> int:
        """Retourne le niveau d'exposition vestimentaire (0-100)"""
        clothing = self.get_component_of_type(ClothingComponent)
        if clothing:
            return clothing.get_exposure_level()
        return 0

    def get_current_state_summary(self) -> Dict[str, Any]:
        """Retourne un résumé complet de l'état actuel"""
        stats = self.get_component_of_type(StatsComponent)
        clothing = self.get_component_of_type(ClothingComponent)
        dialogue = self.get_component_of_type(DialogueComponent)

        summary = {
            "name": self.display_name,
            "resistance": self.get_resistance_level(),
            "arousal": self.get_arousal_level(),
            "exposure": self.get_clothing_exposure(),
            "vulnerable": self.is_vulnerable(),
            "location": dialogue.current_location if dialogue else "unknown"
        }

        if stats:
            summary["stats"] = {
                "volonte": stats.volonte,
                "excitation": stats.excitation,
                "thresholds": stats.thresholds.copy()
            }

        if clothing:
            summary["clothing"] = clothing.get_overall_description()

        return summary

    def can_perform_action(self, action: str) -> bool:
        """Vérifie si le joueur peut effectuer une action"""
        actions = self.get_component_of_type(ActionComponent)
        if actions:
            return actions.is_action_available(action)
        return False

    def get_personality_modifier(self, situation: str) -> float:
        """
        Retourne un modificateur selon la personnalité et situation

        Args:
            situation: Type situation ("resistance", "submission", "curiosity", etc.)

        Returns:
            Multiplicateur entre 0.5 et 1.5
        """
        if situation == "resistance":
            return 0.8 + (self.personality_traits["resistance_willpower"] * 0.4)
        elif situation == "submission":
            return 0.7 + (self.personality_traits["submissiveness"] * 0.6)
        elif situation == "curiosity":
            return 0.6 + (self.personality_traits["curiosity"] * 0.8)
        elif situation == "shyness":
            return 0.5 + (self.personality_traits["shyness"] * 1.0)

        return 1.0  # Modificateur neutre

    def __repr__(self) -> str:
        resistance = round(self.get_resistance_level() * 100)
        arousal = round(self.get_arousal_level() * 100)
        exposure = self.get_clothing_exposure()

        return (f"PlayerCharacter(name={self.display_name}, "
                f"resistance={resistance}%, arousal={arousal}%, exposure={exposure}%)")
