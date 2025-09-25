"""
ClothingSystem V2.0 - Système vêtements actif avec descriptions
Modifications graduelles et affichage temps réel
"""

from core.system import System
from core.entity import Entity
from components.clothing import ClothingComponent
from typing import List, Dict, Any, Optional
import random

class ClothingSystem(System):
    """System vêtements avec modifications graduelles et feedback"""

    def __init__(self):
        super().__init__("ClothingSystem")

        # ESCALATION VÊTEMENTS PAR NIVEAU
        self.clothing_escalation = {
            1: {  # Niveau social - ajustements mineurs
                "actions": ["ajuster_bretelles", "lisser_tissu", "replacer_cheveux"],
                "descriptions": [
                    "Il ajuste délicatement la bretelle de ta robe.",
                    "Sa main lisse le tissu de ta jupe.",
                    "Il replace une mèche de cheveux derrière ton oreille."
                ]
            },
            2: {  # Niveau contact - déplacements légers
                "actions": ["glisser_bretelle", "remonter_leger_jupe", "ouvrir_bouton_haut"],
                "descriptions": [
                    "Sa main fait glisser la bretelle de ton épaule.",
                    "Il remonte légèrement le bas de ta jupe en parlant.",
                    "Il dégrafe subtilement le bouton du haut de ton chemisier."
                ]
            },
            3: {  # Niveau intime - modifications visibles
                "actions": ["deboutonner_chemisier", "remonter_jupe", "faire_glisser_robe"],
                "descriptions": [
                    "Il déboutonne lentement ton chemisier, bouton par bouton.",
                    "Ta jupe remonte, dévoilant tes cuisses nacrées.",
                    "Il fait glisser ta robe le long de tes épaules."
                ]
            },
            4: {  # Niveau avancé - dévoilement
                "actions": ["retirer_chemisier", "baisser_bretelles_soutien_gorge", "faire_tomber_jupe"],
                "descriptions": [
                    "Il retire complètement ton chemisier, admirant ta silhouette.",
                    "Les bretelles de ton soutien-gorge glissent de tes épaules.",
                    "Ta jupe tombe au sol dans un froissement soyeux."
                ]
            },
            5: {  # Niveau maximal - nudité
                "actions": ["retirer_soutien_gorge", "faire_glisser_culotte", "denuder_completement"],
                "descriptions": [
                    "Il dégrafe ton soutien-gorge d'un geste expert.",
                    "Ta culotte glisse le long de tes jambes tremblantes.",
                    "Tu te retrouves complètement nue devant son regard ardent."
                ]
            }
        }

        # Modificateurs par lieu pour réalisme
        self.location_clothing_modifiers = {
            "bar": 0.3,      # Public - très peu de modifications
            "voiture": 0.7,  # Semi-privé - modifications modérées  
            "salon": 1.0,    # Privé - modifications normales
            "chambre": 1.3   # Intime - modifications accentuées
        }

    def update(self, entities: List[Entity], delta_time: float = 0.0, **kwargs):
        """Update vêtements avec modifications contextuelles"""

        # Pas d'update automatique - modifications via actions
        pass

    def apply_clothing_action(self, player: Entity, action_type: str, 
                            escalation_level: int, location: str) -> Dict[str, Any]:
        """
        Applique modification vêtements avec description

        Args:
            player: Entity player
            action_type: Type d'action effectuée  
            escalation_level: Niveau escalation (1-5)
            location: Lieu actuel

        Returns:
            Dict avec description et état
        """

        clothing = player.get_component_of_type(ClothingComponent)
        if not clothing:
            return {"success": False, "description": "", "visible_change": False}

        # Modificateur lieu
        location_mod = self.location_clothing_modifiers.get(location, 1.0)

        # Chance de modification selon escalation et lieu
        base_chance = min(0.9, escalation_level * 0.15 * location_mod)

        if random.random() > base_chance:
            return {"success": False, "description": "", "visible_change": False}

        # Sélection modification selon escalation
        if escalation_level in self.clothing_escalation:
            escalation_data = self.clothing_escalation[escalation_level]
            chosen_action = random.choice(escalation_data["actions"])
            description = random.choice(escalation_data["descriptions"])

            # Application modification au component
            result = self._apply_specific_clothing_change(clothing, chosen_action, escalation_level)

            return {
                "success": True,
                "description": description,
                "action": chosen_action,
                "escalation_level": escalation_level,
                "visible_change": True,
                "exposure_level": result.get("new_exposure", 0)
            }

        return {"success": False, "description": "", "visible_change": False}

    def _apply_specific_clothing_change(self, clothing: ClothingComponent, 
                                      action: str, level: int) -> Dict[str, Any]:
        """Applique changement spécifique à un vêtement"""

        # Mapping actions -> états vêtements
        action_mappings = {
            # Niveau 1
            "ajuster_bretelles": ("robe", "ajustee"),
            "lisser_tissu": ("jupe", "lissee"),

            # Niveau 2  
            "glisser_bretelle": ("robe", "bretelle_glissee"),
            "remonter_leger_jupe": ("jupe", "legerement_remontee"),
            "ouvrir_bouton_haut": ("chemisier", "bouton_ouvert"),

            # Niveau 3
            "deboutonner_chemisier": ("chemisier", "deboutonne"),
            "remonter_jupe": ("jupe", "remontee"),
            "faire_glisser_robe": ("robe", "glissee_epaules"),

            # Niveau 4
            "retirer_chemisier": ("chemisier", "retire"),
            "baisser_bretelles_soutien_gorge": ("soutien_gorge", "bretelles_baissees"),
            "faire_tomber_jupe": ("jupe", "tombee"),

            # Niveau 5
            "retirer_soutien_gorge": ("soutien_gorge", "retire"),
            "faire_glisser_culotte": ("culotte", "glissee"),
            "denuder_completement": ("culotte", "retiree")
        }

        if action in action_mappings:
            piece_name, new_state = action_mappings[action]

            if hasattr(clothing, 'pieces') and piece_name in clothing.pieces:
                clothing.pieces[piece_name]["state"] = new_state
                clothing.pieces[piece_name]["last_modified"] = level

                # Mise à jour exposition
                if hasattr(clothing, '_update_derived_stats'):
                    clothing._update_derived_stats()

                # Mark dirty pour affichage
                clothing.mark_dirty()

                return {
                    "success": True,
                    "piece_modified": piece_name,
                    "new_state": new_state,
                    "new_exposure": getattr(clothing, 'exposure_level', 0)
                }

        return {"success": False}

    def get_clothing_display_text(self, player: Entity) -> str:
        """Génère texte affichage état vêtements"""

        clothing = player.get_component_of_type(ClothingComponent)
        if not clothing:
            return ""

        # Seulement si modifications visibles
        if getattr(clothing, 'exposure_level', 0) == 0:
            return ""

        # Description des pièces modifiées
        if hasattr(clothing, 'get_most_exposed_pieces'):
            exposed_pieces = clothing.get_most_exposed_pieces(2)

            if exposed_pieces:
                descriptions = []
                for piece_data in exposed_pieces:
                    piece = piece_data["piece"]
                    state = piece_data["state"]
                    descriptions.append(f"{piece}: {state}")

                return "👗 " + " | ".join(descriptions)

        return f"👗 Exposition: {getattr(clothing, 'exposure_level', 0)}%"

# CLOTHING SYSTEM V2.0: Modifications graduelles + descriptions immersives
