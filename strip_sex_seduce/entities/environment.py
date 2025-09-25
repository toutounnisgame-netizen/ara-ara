"""
Environment Entity - Gestion lieux et contextes
Représente les différents environnements du jeu avec leurs contraintes
"""

from core.entity import Entity
from components.action import ActionComponent
from typing import Dict, List, Any, Optional

class Environment(Entity):
    """
    Entity représentant un environnement/lieu de jeu
    Chaque lieu a ses propres règles et actions possibles
    """

    def __init__(self, location: str):
        super().__init__(f"env_{location}")

        # Identification
        self.location = location
        self.display_name = self._get_display_name(location)

        # Propriétés du lieu
        self.privacy_level = self._get_privacy_level(location)
        self.social_visibility = self._get_social_visibility(location)
        self.escape_difficulty = self._get_escape_difficulty(location)

        # Contraintes et règles
        self.social_constraints = self._get_social_constraints(location)
        self.location_modifiers = self._get_location_modifiers(location)

        # Actions spécifiques au lieu
        self.interactive_objects = self._get_interactive_objects(location)

        # Setup components
        self._setup_components()

    def _get_display_name(self, location: str) -> str:
        """Retourne le nom d'affichage du lieu"""
        names = {
            "bar": "Bar - Le Moonlight",
            "voiture": "Sa Voiture",
            "salon": "Salon de l'Appartement", 
            "chambre": "Chambre à Coucher"
        }
        return names.get(location, location.title())

    def _get_privacy_level(self, location: str) -> float:
        """Niveau d'intimité du lieu (0.0-1.0)"""
        privacy_map = {
            "bar": 0.2,         # Très public
            "voiture": 0.6,     # Semi-privé
            "salon": 0.8,       # Privé
            "chambre": 1.0      # Très intime
        }
        return privacy_map.get(location, 0.5)

    def _get_social_visibility(self, location: str) -> bool:
        """Si le lieu est socialement visible"""
        return location in ["bar", "restaurant", "cafe"]

    def _get_escape_difficulty(self, location: str) -> float:
        """Difficulté de fuite du lieu (0.0-1.0)"""
        difficulty_map = {
            "bar": 0.2,         # Facile de partir
            "voiture": 0.6,     # Moyenne difficulté
            "salon": 0.4,       # Relativement facile
            "chambre": 0.8      # Difficile de partir
        }
        return difficulty_map.get(location, 0.5)

    def _get_social_constraints(self, location: str) -> Dict[str, Any]:
        """Contraintes sociales du lieu"""
        constraints = {
            "bar": {
                "public_visibility": True,
                "noise_concerns": True,
                "time_pressure": False,
                "interruption_risk": 0.7,
                "escape_possible": True,
                "social_norms": "strict"
            },
            "voiture": {
                "public_visibility": False,
                "noise_concerns": True,
                "time_pressure": False,
                "interruption_risk": 0.3,
                "escape_possible": True,
                "social_norms": "relaxed"
            },
            "salon": {
                "public_visibility": False,
                "noise_concerns": False,
                "time_pressure": False,
                "interruption_risk": 0.1,
                "escape_possible": True,
                "social_norms": "private"
            },
            "chambre": {
                "public_visibility": False,
                "noise_concerns": False,
                "time_pressure": False,
                "interruption_risk": 0.05,
                "escape_possible": False,
                "social_norms": "intimate"
            }
        }
        return constraints.get(location, constraints["bar"])

    def _get_location_modifiers(self, location: str) -> Dict[str, float]:
        """Modificateurs de stats selon le lieu"""
        modifiers = {
            "bar": {
                "volonte_modifier": 0.0,        # Pas de modificateur
                "excitation_modifier": -0.1,    # Légèrement moins excitant
                "resistance_bonus": 0.2         # Plus facile de résister en public
            },
            "voiture": {
                "volonte_modifier": -0.1,       # Légère baisse résistance
                "excitation_modifier": 0.1,     # Plus excitant
                "resistance_bonus": 0.0         # Pas de bonus
            },
            "salon": {
                "volonte_modifier": -0.2,       # Baisse résistance notable
                "excitation_modifier": 0.2,     # Nettement plus excitant
                "resistance_bonus": -0.1        # Résistance plus difficile
            },
            "chambre": {
                "volonte_modifier": -0.3,       # Forte baisse résistance
                "excitation_modifier": 0.3,     # Très excitant
                "resistance_bonus": -0.2        # Résistance difficile
            }
        }
        return modifiers.get(location, modifiers["bar"])

    def _get_interactive_objects(self, location: str) -> List[Dict[str, Any]]:
        """Objets interactifs dans le lieu"""
        objects = {
            "bar": [
                {
                    "name": "comptoir",
                    "actions": ["s_appuyer", "commander_verre"],
                    "effects": {"social": +1}
                },
                {
                    "name": "banquette",
                    "actions": ["s_asseoir_pres", "conversation_privee"],
                    "effects": {"intimacy": +1}
                }
            ],
            "voiture": [
                {
                    "name": "siege_passager",
                    "actions": ["se_rapprocher", "ajuster_siege"],
                    "effects": {"physical_proximity": +2}
                },
                {
                    "name": "radio",
                    "actions": ["changer_ambiance", "baisser_musique"],
                    "effects": {"mood": +1}
                }
            ],
            "salon": [
                {
                    "name": "canape",
                    "actions": ["s_asseoir_ensemble", "se_rapprocher"],
                    "effects": {"intimacy": +2, "physical_contact": +1}
                },
                {
                    "name": "eclairage",
                    "actions": ["tamiser_lumiere", "ambiance_romantique"],
                    "effects": {"mood": +2, "inhibition": -1}
                }
            ],
            "chambre": [
                {
                    "name": "lit",
                    "actions": ["s_asseoir_sur", "s_allonger"],
                    "effects": {"intimacy": +3, "physical_escalation": +2}
                },
                {
                    "name": "porte",
                    "actions": ["fermer_cle", "verouiller"],
                    "effects": {"privacy": +2, "escape_difficulty": +1}
                }
            ]
        }
        return objects.get(location, [])

    def _setup_components(self):
        """Configuration des components de l'environment"""

        # ActionComponent pour les actions liées au lieu
        actions = ActionComponent()
        self._setup_location_actions(actions)
        self.add_component(actions)

    def _setup_location_actions(self, action_component: ActionComponent):
        """Configure les actions possibles dans ce lieu"""

        location_actions = {
            "bar": [
                "commander_verre", "conversation_bar", "danser_ensemble",
                "sortir_terrasse", "aller_voiture", "compliment_tenue"
            ],
            "voiture": [
                "conduire_appartement", "arreter_endroit_isole", 
                "ajuster_retroviseur", "main_cuisse_conduite",
                "baiser_voiture", "caresses_voiture"
            ],
            "salon": [
                "visiter_appartement", "offrir_boisson", "mettre_musique",
                "s_asseoir_canape", "rapprochement_salon", 
                "baiser_salon", "caresses_salon", "aller_chambre"
            ],
            "chambre": [
                "fermer_porte", "tamiser_eclairage", "s_asseoir_lit",
                "rapprochement_intime", "caresses_intimes", 
                "deshabillage", "intimite_complete"
            ]
        }

        actions_list = location_actions.get(self.location, [])
        for action in actions_list:
            # Configuration basique - sera raffinée par les systems
            action_component.add_action(action, success_rate=0.5)

    def get_available_transitions(self) -> List[str]:
        """Retourne les lieux accessibles depuis ici"""
        transitions = {
            "bar": ["voiture"],
            "voiture": ["bar", "salon"],
            "salon": ["voiture", "chambre"],
            "chambre": ["salon"]
        }
        return transitions.get(self.location, [])

    def calculate_action_success_rate(self, action: str, 
                                    player_resistance: float) -> float:
        """
        Calcule le taux de succès d'une action dans ce lieu

        Args:
            action: Action tentée
            player_resistance: Résistance actuelle joueur (0.0-1.0)

        Returns:
            Taux de succès (0.0-1.0)
        """
        # Taux de base selon action
        base_rates = {
            "conversation": 0.9,
            "compliment": 0.8,
            "contact_leger": 0.6,
            "contact_moyen": 0.4,
            "contact_intime": 0.2,
            "escalation": 0.3
        }

        # Déterminer catégorie action
        if any(word in action for word in ["conversation", "parler", "discuter"]):
            base_rate = base_rates["conversation"]
        elif any(word in action for word in ["compliment", "charme"]):
            base_rate = base_rates["compliment"]
        elif any(word in action for word in ["contact", "main", "toucher"]):
            base_rate = base_rates["contact_leger"]
        elif any(word in action for word in ["caresse", "baiser"]):
            base_rate = base_rates["contact_moyen"]
        elif any(word in action for word in ["intime", "deshabillage"]):
            base_rate = base_rates["contact_intime"]
        else:
            base_rate = 0.5

        # Ajustement selon résistance
        resistance_penalty = player_resistance * 0.5

        # Ajustement selon lieu (privacy bonus)
        privacy_bonus = self.privacy_level * 0.2

        # Ajustement selon contraintes sociales
        social_penalty = 0.3 if self.social_constraints["public_visibility"] else 0.0

        # Calcul final
        final_rate = base_rate - resistance_penalty + privacy_bonus - social_penalty

        return max(0.05, min(0.95, final_rate))  # Entre 5% et 95%

    def get_environment_description(self) -> str:
        """Retourne une description narrative du lieu"""
        descriptions = {
            "bar": (
                "L'atmosphère du bar est animée mais tamisée. La musique crée "
                "une ambiance propice aux conversations intimes, bien qu'il y ait "
                "d'autres clients autour."
            ),
            "voiture": (
                "L'habitacle de sa voiture offre une intimité relative. "
                "L'espace confiné favorise la proximité physique tout en "
                "gardant une échappatoire possible."
            ),
            "salon": (
                "Le salon de l'appartement est décoré avec goût. L'éclairage "
                "tamisé et l'ambiance feutrée créent une atmosphère romantique "
                "et relaxante."
            ),
            "chambre": (
                "La chambre est le sanctuaire de l'intimité. L'atmosphère y est "
                "chargée de possibilités, et les options d'échappatoire "
                "se font rares."
            )
        }
        return descriptions.get(self.location, f"Vous êtes dans {self.display_name}")

    def to_dict(self) -> Dict[str, Any]:
        """Sérialisation complète de l'environment"""
        base_dict = super().to_dict()
        base_dict.update({
            "location": self.location,
            "display_name": self.display_name,
            "privacy_level": self.privacy_level,
            "escape_difficulty": self.escape_difficulty,
            "social_constraints": self.social_constraints,
            "available_transitions": self.get_available_transitions(),
            "interactive_objects_count": len(self.interactive_objects)
        })
        return base_dict

    def __repr__(self) -> str:
        return (f"Environment(location={self.location}, "
                f"privacy={self.privacy_level:.1f}, "
                f"escape_difficulty={self.escape_difficulty:.1f})")
