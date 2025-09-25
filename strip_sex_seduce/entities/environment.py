"""
Environment V2.0 COMPATIBLE - Résolution signature ActionComponent
Version adaptée au ActionComponent existant (sans description parameter)
"""

from core.entity import Entity
from components.action import ActionComponent
from typing import Dict, List, Any, Optional

class Environment(Entity):
    """Environment COMPATIBLE avec ActionComponent existant"""

    def __init__(self, location: str):
        super().__init__(f"env_{location}")

        # Identification
        self.location = location
        self.display_name = self._get_display_name(location)

        # Propriétés étendues - TOUTES MÉTHODES IMPLÉMENTÉES
        self.privacy_level = self._get_privacy_level(location)
        self.social_visibility = self._get_social_visibility(location)
        self.escape_difficulty = self._get_escape_difficulty(location)
        self.intimacy_multiplier = self._get_intimacy_multiplier(location)

        # Contraintes et règles
        self.social_constraints = self._get_social_constraints(location)
        self.location_modifiers = self._get_location_modifiers(location)

        # Actions contextuelles spécialisées
        self.contextual_actions = self._get_contextual_actions(location)
        self.atmosphere_descriptions = self._get_atmosphere_descriptions(location)

        # Setup components COMPATIBLE
        self._setup_components()

    def _get_display_name(self, location: str) -> str:
        """Noms immersifs des lieux"""
        names = {
            "bar": "Le Moonlight - Bar Lounge",
            "voiture": "Sa BMW dans le parking", 
            "salon": "Salon de son Appartement",
            "chambre": "Sa Chambre Intime"
        }
        return names.get(location, location.title())

    def _get_privacy_level(self, location: str) -> float:
        """Niveau intimité/privacy du lieu"""
        privacy_levels = {
            "bar": 0.2,        # Public - très peu d'intimité
            "voiture": 0.6,    # Semi-privé - intimité modérée
            "salon": 0.8,      # Privé - forte intimité
            "chambre": 1.0     # Intime - intimité maximale
        }
        return privacy_levels.get(location, 0.5)

    def _get_social_visibility(self, location: str) -> float:
        """Visibilité sociale (inverse de privacy)"""
        return 1.0 - self._get_privacy_level(location)

    def _get_escape_difficulty(self, location: str) -> float:
        """Difficulté s'échapper du lieu"""
        difficulties = {
            "bar": 0.2,        # Facile de partir d'un bar
            "voiture": 0.4,    # Moyennement difficile (dépendance)
            "salon": 0.3,      # Assez facile (porte d'entrée)
            "chambre": 0.8     # Difficile (intimité, engagement)
        }
        return difficulties.get(location, 0.5)

    def _get_intimacy_multiplier(self, location: str) -> float:
        """Multiplicateur d'intimité pour les actions"""
        multipliers = {
            "bar": 0.7,        # Moins intime (public)
            "voiture": 1.2,    # Plus intime (privé relatif)
            "salon": 1.5,      # Très intime (chez lui)
            "chambre": 2.0     # Maximum intimité
        }
        return multipliers.get(location, 1.0)

    def _get_social_constraints(self, location: str) -> Dict[str, Any]:
        """Contraintes sociales du lieu"""
        constraints = {
            "bar": {
                "max_escalation": 2,
                "forbidden_actions": ["caresses_intimes", "removal_vetement"],
                "social_pressure": "high",
                "witnesses": True
            },
            "voiture": {
                "max_escalation": 4,
                "forbidden_actions": ["removal_vetement"],
                "social_pressure": "medium",
                "witnesses": False
            },
            "salon": {
                "max_escalation": 4,
                "forbidden_actions": [],
                "social_pressure": "low",
                "witnesses": False
            },
            "chambre": {
                "max_escalation": 5,
                "forbidden_actions": [],
                "social_pressure": "none",
                "witnesses": False
            }
        }
        return constraints.get(location, constraints["bar"])

    def _get_contextual_actions(self, location: str) -> List[Dict[str, Any]]:
        """Actions spécifiques par lieu avec descriptions intégrées"""

        actions = {
            "bar": [
                {
                    "name": "commander_verre_ensemble",
                    "description": "Il commande pour vous deux, choisissant avec goût",
                    "intimacy_gain": 5,
                    "escalation_level": 1
                },
                {
                    "name": "conversation_proche",
                    "description": "Il se penche pour parler dans votre oreille malgré la musique", 
                    "intimacy_gain": 8,
                    "escalation_level": 2
                },
                {
                    "name": "contact_discret",
                    "description": "Ses doigts effleurent les vôtres en prenant son verre",
                    "intimacy_gain": 12,
                    "escalation_level": 2
                }
            ],
            "voiture": [
                {
                    "name": "ajuster_retroviseur_pretexte",
                    "description": "Il ajuste le rétroviseur, se rapprochant de vous",
                    "intimacy_gain": 10,
                    "escalation_level": 2
                },
                {
                    "name": "main_sur_changement_vitesse", 
                    "description": "En changeant de vitesse, sa main frôle votre cuisse",
                    "intimacy_gain": 15,
                    "escalation_level": 3
                },
                {
                    "name": "arrêt_point_vue",
                    "description": "Il s'arrête à un point de vue pour 'admirer le paysage'",
                    "intimacy_gain": 20,
                    "escalation_level": 3
                }
            ],
            "salon": [
                {
                    "name": "service_vin_rapprochement",
                    "description": "Il vous sert un verre, profitant du service pour se rapprocher",
                    "intimacy_gain": 15,
                    "escalation_level": 3
                },
                {
                    "name": "montrer_art_contact",
                    "description": "En vous montrant un tableau, il se place derrière vous",
                    "intimacy_gain": 25,
                    "escalation_level": 4
                },
                {
                    "name": "invitation_canape",
                    "description": "Il vous invite à vous asseoir près de lui sur le canapé",
                    "intimacy_gain": 30,
                    "escalation_level": 4
                }
            ],
            "chambre": [
                {
                    "name": "fermeture_porte_symbolique",
                    "description": "Il ferme doucement la porte, vos regards se croisent",
                    "intimacy_gain": 35,
                    "escalation_level": 5
                },
                {
                    "name": "invitation_assoir_lit",
                    "description": "Il vous invite à vous asseoir au bord du lit",
                    "intimacy_gain": 40,
                    "escalation_level": 5
                },
                {
                    "name": "ambiance_intime_musique",
                    "description": "Il lance une playlist sensuelle pour l'ambiance",
                    "intimacy_gain": 30,
                    "escalation_level": 4
                }
            ]
        }

        return actions.get(location, [])

    def _get_atmosphere_descriptions(self, location: str) -> List[str]:
        """Descriptions atmosphériques pour immersion"""

        descriptions = {
            "bar": [
                "L'ambiance feutrée du bar lounge crée une intimité troublante.",
                "Les conversations se mélangent au jazz, créant un cocon sonore.",
                "L'éclairage tamisé fait danser les ombres sur vos visages.",
                "Autour de vous, d'autres couples partagent des moments complices."
            ],
            "voiture": [
                "L'habitacle vous isole du monde, créant une bulle d'intimité.",
                "Le cuir des sièges exhale un parfum masculin et raffiné.",
                "Par les vitres teintées, la ville défile dans un flou artistique.",
                "L'espace confiné amplifie chaque geste, chaque regard."
            ],
            "salon": [
                "Le salon reflète son goût sûr : élégant et sensuel à la fois.",
                "Les bougies projettent une lumière dorée sur les murs.",
                "L'art contemporain aux murs témoigne de sa culture raffinée.",
                "Le grand canapé semble vous inviter à vous rapprocher."
            ],
            "chambre": [
                "La chambre respire la sensualité assumée et l'intimité.",
                "Le grand lit domine l'espace, promesse de plaisirs à venir.",
                "L'éclairage indirect crée une ambiance propice aux confidences.",
                "Ici, les masques tombent, seule l'authenticité compte."
            ]
        }

        return descriptions.get(location, ["Vous vous trouvez dans un lieu indéterminé."])

    def _get_location_modifiers(self, location: str) -> Dict[str, float]:
        """Modificateurs stats selon lieu"""

        modifiers = {
            "bar": {
                "volonte_modifier": 1.1,
                "excitation_modifier": 0.9,
                "resistance_bonus": 0.15
            },
            "voiture": {
                "volonte_modifier": 0.95,
                "excitation_modifier": 1.1,
                "resistance_bonus": 0.05
            },
            "salon": {
                "volonte_modifier": 0.8,
                "excitation_modifier": 1.3,
                "resistance_bonus": -0.05
            },
            "chambre": {
                "volonte_modifier": 0.6,
                "excitation_modifier": 1.6,
                "resistance_bonus": -0.15
            }
        }
        return modifiers.get(location, modifiers["bar"])

    def _setup_components(self):
        """Setup components COMPATIBLE avec ActionComponent existant"""

        # ActionComponent avec signature compatible
        actions = ActionComponent()

        # AJOUT ACTIONS SANS PARAMETER description (compatible)
        for action_data in self.contextual_actions:
            # Signature compatible: seulement name et success_rate
            actions.add_action(
                action_data["name"],
                success_rate=0.7  # Pas de description parameter
            )

        self.add_component(actions)

    # MÉTHODES UTILITY INCHANGÉES
    def get_random_atmosphere_description(self) -> str:
        """Retourne description aléatoire pour variété"""
        import random
        return random.choice(self.atmosphere_descriptions)

    def get_available_contextual_actions(self, escalation_level: int = 1) -> List[Dict[str, Any]]:
        """Retourne actions contextuelles selon niveau escalation"""
        available_actions = []
        for action in self.contextual_actions:
            if action["escalation_level"] <= escalation_level:
                available_actions.append(action)
        return available_actions

    def calculate_action_effectiveness(self, action: str, player_resistance: float,
                                    escalation_level: int) -> float:
        """Calcule effectiveness action contextuelle"""
        base_effectiveness = 0.5 + (self.privacy_level * 0.3)
        resistance_modifier = max(0.1, 1.0 - player_resistance)
        escalation_modifier = min(1.0, escalation_level / 5.0)
        environment_bonus = self.intimacy_multiplier * 0.1

        final_effectiveness = (base_effectiveness * resistance_modifier * 
                             escalation_modifier) + environment_bonus

        return min(0.95, max(0.05, final_effectiveness))

    def get_transition_requirements(self) -> Dict[str, Any]:
        """Requirements pour transition depuis ce lieu"""

        requirements = {
            "bar": {
                "min_excitation": 25,
                "max_volonte": 85,
                "next_location": "voiture",
                "transition_message": "Il te propose de continuer ailleurs..."
            },
            "voiture": {
                "min_excitation": 45,
                "max_volonte": 70,
                "next_location": "salon",
                "transition_message": "Son appartement n'est qu'à deux minutes..."
            },
            "salon": {
                "min_excitation": 65,
                "max_volonte": 50,
                "next_location": "chambre",
                "transition_message": "Il te tend la main vers la chambre..."
            },
            "chambre": {
                "next_location": None,
                "transition_message": "Vous y êtes..."
            }
        }

        return requirements.get(self.location, {})

    def get_action_description(self, action_name: str) -> str:
        """Récupère description action depuis données contextuelles"""

        for action_data in self.contextual_actions:
            if action_data["name"] == action_name:
                return action_data["description"]

        return f"Action {action_name} effectuée."

    def to_dict(self) -> Dict[str, Any]:
        """Sérialisation enrichie"""
        base_dict = super().to_dict()
        base_dict.update({
            "location": self.location,
            "display_name": self.display_name,
            "privacy_level": self.privacy_level,
            "intimacy_multiplier": self.intimacy_multiplier,
            "contextual_actions_count": len(self.contextual_actions),
            "atmosphere_descriptions_count": len(self.atmosphere_descriptions)
        })
        return base_dict

# ENVIRONMENT V2.0 COMPATIBLE: Signature ActionComponent respectée
