"""
ClothingSystem V2.0 - Gestion vêtements avec progression visible
Correctif: Modifications graduelles + affichage temps réel + réalisme
"""

from core.system import System
from core.entity import Entity
from components.clothing import ClothingComponent
from typing import List, Dict, Any, Optional

class ClothingSystem(System):
    """System vêtements avec modifications graduelles et affichage visible"""

    def __init__(self):
        super().__init__("ClothingSystem")

        # Correspondance actions NPC → modifications vêtements
        self.action_clothing_effects = {
            # Actions légères - ajustements subtils
            "contact_epaule": {
                "pieces": ["bretelles_robe"],
                "modifications": ["legerement_deplacee", "glissee"],
                "exposure_gain": 2,
                "description": "La bretelle de ta robe glisse légèrement sous sa caresse..."
            },
            "rapprochement_physique": {
                "pieces": ["robe", "chemisier"],
                "modifications": ["plis_froissee", "legerement_remontee"],
                "exposure_gain": 3,
                "description": "Tes vêtements se froissent légèrement contre lui..."
            },

            # Actions modérées - modifications visibles
            "main_cuisse": {
                "pieces": ["robe", "jupe"],
                "modifications": ["remontee", "retroussee"],
                "exposure_gain": 8,
                "description": "Sa main fait remonter le tissu, dévoilant tes cuisses..."
            },
            "caresses_douces": {
                "pieces": ["chemisier", "top"],
                "modifications": ["boutonne_partiellement", "entrouverte"],
                "exposure_gain": 10,
                "description": "Ses caresses défont délicatement quelques boutons..."
            },

            # Actions intenses - déshabillement progressif
            "baiser_leger": {
                "pieces": ["veste", "cardigan"],
                "modifications": ["retiree", "tombee"],
                "exposure_gain": 12,
                "description": "Dans l'élan du baiser, ta veste glisse de tes épaules..."
            },
            "caresses": {
                "pieces": ["chemisier", "robe"],
                "modifications": ["largement_ouverte", "descendue_epaules"],
                "exposure_gain": 18,
                "description": "Ses mains expertes dénudent progressivement tes épaules..."
            },

            # Actions très intenses - déshabillement majeur
            "baiser_profond": {
                "pieces": ["soutien_gorge", "chemisier"],
                "modifications": ["défait", "complètement_ouverte"],
                "exposure_gain": 25,
                "description": "La passion vous emporte, vos vêtements deviennent un obstacle..."
            },
            "caresses_intimes": {
                "pieces": ["sous_vetements", "lingerie"],
                "modifications": ["retiree", "mise_de_cote"],
                "exposure_gain": 35,
                "description": "Il écarte délicatement tes derniers voiles de pudeur..."
            }
        }

        # Seuils pour feedback automatique
        self.exposure_thresholds = {
            10: "Tes vêtements commencent à révéler tes formes...",
            25: "Tu te sens de plus en plus dévêtue sous son regard...",
            40: "Une grande partie de ton corps est maintenant exposée...",
            60: "Tu ne portes presque plus rien qui cache ton intimité...",
            80: "Tes derniers vêtements ne tiennent plus qu'à un fil..."
        }

        # Tracking pour feedback unique
        self._exposure_feedback_given = {}

    def update(self, entities: List[Entity], delta_time: float = 0.0, **kwargs):
        """Update système vêtements avec gestion automatique"""

        # Traitement entities avec ClothingComponent
        for entity in entities:
            clothing = entity.get_component_of_type(ClothingComponent)
            if clothing and clothing.is_dirty:
                # Update stats dérivées
                clothing._update_derived_stats()

                # Check seuils exposition pour feedback
                self._check_exposure_feedback(entity, clothing)

                clothing.mark_clean()

    def apply_action_clothing_effects(self, player: Entity, action: str, 
                                    context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Applique effets vêtements selon action NPC

        Args:
            player: Entity player
            action: Action NPC effectuée
            context: Contexte (lieu, résistance, etc.)

        Returns:
            Dict résultats modifications
        """
        clothing = player.get_component_of_type(ClothingComponent)
        if not clothing:
            return {"success": False, "error": "Pas de ClothingComponent"}

        # Vérification si action affecte vêtements
        effect_data = self.action_clothing_effects.get(action)
        if not effect_data:
            return {"success": True, "no_clothing_effect": True}

        # Sauvegarde état avant
        exposure_before = clothing.get_exposure_level()
        pieces_before = clothing.pieces.copy()

        # Modification selon résistance joueur
        player_resistance = context.get("resistance_level", 0.5)

        # Résistance forte = modifications réduites
        if player_resistance > 0.8:
            exposure_reduction = 0.5  # Moitié des effets
            description_prefix = "Malgré tes tentatives de résistance, "
        elif player_resistance > 0.5:
            exposure_reduction = 0.7  # Effets réduits
            description_prefix = "Tu essaies de garder tes vêtements en place mais "
        else:
            exposure_reduction = 1.0  # Effets complets
            description_prefix = ""

        # Application modifications avec résistance
        target_pieces = effect_data["pieces"]
        modifications = effect_data["modifications"]
        base_exposure_gain = effect_data["exposure_gain"]

        # Sélection pièce affectée
        available_pieces = [p for p in target_pieces if p in clothing.pieces]
        if available_pieces:
            import random
            target_piece = random.choice(available_pieces)
            target_modification = random.choice(modifications)

            # Application modification
            result = clothing.modify_piece(
                piece=target_piece,
                modification=target_modification,
                context=f"action_{action}"
            )

            # Gain exposition avec résistance
            final_exposure_gain = int(base_exposure_gain * exposure_reduction)
            clothing.exposure_level = min(100, 
                clothing.exposure_level + final_exposure_gain)

            # Description adaptée
            base_description = effect_data["description"]
            final_description = description_prefix + base_description.lower() if description_prefix else base_description

        else:
            # Pas de pièce disponible - gain exposition réduit
            final_exposure_gain = int(base_exposure_gain * 0.3)
            clothing.exposure_level = min(100, 
                clothing.exposure_level + final_exposure_gain)
            final_description = "Tes vêtements se désorganisent sous ses caresses..."

        # État après modification
        exposure_after = clothing.get_exposure_level()
        pieces_after = clothing.pieces.copy()

        # Force dirty flag pour affichage
        clothing.mark_dirty()

        return {
            "success": True,
            "exposure_before": exposure_before,
            "exposure_after": exposure_after,
            "exposure_gain": final_exposure_gain,
            "pieces_modified": len(pieces_before) != len(pieces_after),
            "description": final_description,
            "resistance_applied": player_resistance > 0.5,
            "visible_change": final_exposure_gain >= 5
        }

    def _check_exposure_feedback(self, entity: Entity, clothing: ClothingComponent):
        """Vérifie seuils exposition et génère feedback automatique"""

        current_exposure = clothing.get_exposure_level()
        entity_id = entity.id

        # Vérification seuils franchis
        if entity_id not in self._exposure_feedback_given:
            self._exposure_feedback_given[entity_id] = set()

        given_feedback = self._exposure_feedback_given[entity_id]

        for threshold, message in self.exposure_thresholds.items():
            if (current_exposure >= threshold and 
                threshold not in given_feedback):

                # Nouveau seuil franchi - feedback unique
                self._exposure_feedback_given[entity_id].add(threshold)

                # Ajout message au contexte pour affichage par game_session
                # (système de messaging à implémenter)
                print(f"\n👗 {message}")

    def get_clothing_display_text(self, player: Entity) -> Dict[str, Any]:
        """Génère texte affichage état vêtements"""

        clothing = player.get_component_of_type(ClothingComponent)
        if not clothing:
            return {"text": "", "exposure": 0, "visible": False}

        exposure_level = clothing.get_exposure_level()

        # Affichage seulement si modifications significatives
        if exposure_level < 5:
            return {"text": "", "exposure": exposure_level, "visible": False}

        # Description selon niveau exposition
        if exposure_level < 15:
            description = "Tes vêtements sont légèrement désordonnés"
        elif exposure_level < 30:
            description = "Ta tenue commence à se défaire"
        elif exposure_level < 50:
            description = "Tes vêtements révèlent beaucoup de peau"
        elif exposure_level < 70:
            description = "Tu es largement dénudée"
        elif exposure_level < 90:
            description = "Tu ne portes presque plus rien"
        else:
            description = "Tu es entièrement exposée à son regard"

        # Détail pièces modifiées
        modified_pieces = []
        for piece, data in clothing.pieces.items():
            if data["state"] != "normale":
                piece_display = self._get_piece_display_name(piece)
                state_display = self._get_state_display_name(data["state"])
                modified_pieces.append(f"{piece_display}: {state_display}")

        details_text = " | ".join(modified_pieces) if modified_pieces else ""

        return {
            "text": description,
            "details": details_text,
            "exposure": exposure_level,
            "visible": True,
            "pieces_count": len(modified_pieces)
        }

    def _get_piece_display_name(self, piece: str) -> str:
        """Noms pièces pour affichage"""

        names = {
            "robe": "Robe",
            "chemisier": "Chemisier", 
            "jupe": "Jupe",
            "pantalon": "Pantalon",
            "soutien_gorge": "Soutien-gorge",
            "culotte": "Culotte",
            "bas": "Bas",
            "chaussures": "Chaussures",
            "veste": "Veste",
            "bretelles_robe": "Bretelles"
        }
        return names.get(piece, piece.title())

    def _get_state_display_name(self, state: str) -> str:
        """États pour affichage"""

        states = {
            "legerement_deplacee": "déplacée",
            "glissee": "glissée",
            "remontee": "remontée", 
            "retroussee": "retroussée",
            "plis_froissee": "froissée",
            "boutonne_partiellement": "entrouverte",
            "entrouverte": "ouverte",
            "retiree": "enlevée",
            "tombee": "tombée",
            "largement_ouverte": "grande ouverte",
            "descendue_epaules": "sur les épaules",
            "défait": "défait",
            "complètement_ouverte": "complètement ouverte",
            "mise_de_cote": "écartée"
        }
        return states.get(state, state)

    def reset_clothing_state(self, player: Entity):
        """Remet vêtements état initial"""

        clothing = player.get_component_of_type(ClothingComponent)
        if clothing:
            clothing.reset_to_initial_state()
            clothing.mark_dirty()

            # Reset feedback donné
            entity_id = player.id
            if entity_id in self._exposure_feedback_given:
                self._exposure_feedback_given[entity_id].clear()

    def get_clothing_progression_summary(self, player: Entity) -> Dict[str, Any]:
        """Résumé progression vêtements pour debug/analytics"""

        clothing = player.get_component_of_type(ClothingComponent)
        if not clothing:
            return {"error": "No clothing component"}

        modified_count = sum(1 for data in clothing.pieces.values() 
                           if data["state"] != "normale")

        return {
            "total_pieces": len(clothing.pieces),
            "modified_pieces": modified_count,
            "exposure_level": clothing.get_exposure_level(),
            "modification_count": len(clothing.modification_history),
            "last_modification": clothing.modification_history[-1] if clothing.modification_history else None
        }

# SYSTÈME VÊTEMENTS V2.0: Modifications graduelles + feedback + réalisme
