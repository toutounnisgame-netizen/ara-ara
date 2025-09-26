"""
PlayerCharacter V2.0 - Entité joueur complète avec toutes méthodes
Compatibility layers et méthodes manquantes
"""

from core.entity import Entity
from components.stats import StatsComponent
from components.clothing import ClothingComponent
from typing import Dict, Any, Optional

class PlayerCharacter(Entity):
    """Joueur avec toutes méthodes V2.0 pour compatibility complète"""

    def __init__(self, name: str = "Joueuse"):
        super().__init__(f"player_{name}")

        self.name = name
        self.display_name = name

        # Setup components de base
        self._setup_initial_stats()
        self._setup_initial_clothing()

    def _setup_initial_stats(self):
        """Configuration stats initiales"""

        stats = StatsComponent()
        stats.volonte = 100
        stats.excitation = 0

        # Seuils initiaux
        stats.thresholds = {
            "vulnerable": False,    # volonte < 40
            "aroused": False,       # excitation > 60
            "submissive": False,    # volonte < 20
            "climax_ready": False   # excitation > 85
        }

        self.add_component(stats)

    def _setup_initial_clothing(self):
        """Configuration vêtements initiaux"""

        clothing = ClothingComponent()

        # État initial conservateur
        clothing.pieces = {
            "robe": {
                "state": "normale",
                "last_modified": 0,
                "description": "Une robe élégante bien ajustée"
            },
            "soutien_gorge": {
                "state": "normale", 
                "last_modified": 0,
                "description": "Un soutien-gorge discret"
            },
            "culotte": {
                "state": "normale",
                "last_modified": 0, 
                "description": "Une culotte assortie"
            }
        }

        clothing.exposure_level = 0
        clothing.initial_outfit = "conservatrice"

        self.add_component(clothing)

    def get_current_state_summary(self) -> Dict[str, Any]:
        """Retourne résumé état joueur actuel pour systems"""

        stats = self.get_component_of_type(StatsComponent)
        clothing = self.get_component_of_type(ClothingComponent)

        if not stats:
            return {
                "stats": {"volonte": 100, "excitation": 0},
                "resistance": 1.0,
                "arousal": 0.0,
                "exposure": 0,
                "clothing": []
            }

        # Stats de base
        summary = {
            "stats": {
                "volonte": getattr(stats, 'volonte', 100),
                "excitation": getattr(stats, 'excitation', 0)
            },
            "resistance": self.get_resistance_level(),
            "arousal": getattr(stats, 'excitation', 0) / 100.0,  # Normalisé 0-1
            "exposure": 0,
            "clothing": []
        }

        # Ajout info vêtements si présent
        if clothing:
            if hasattr(clothing, 'exposure_level'):
                summary["exposure"] = clothing.exposure_level

            # Vêtements modifiés
            if hasattr(clothing, 'pieces'):
                modified_pieces = []
                for piece, data in clothing.pieces.items():
                    if data.get("state", "normale") != "normale":
                        modified_pieces.append(f"{piece}: {data['state']}")

                summary["clothing"] = modified_pieces

        return summary

    def get_resistance_level(self) -> float:
        """Retourne niveau résistance normalisé 0.0-1.0"""

        stats = self.get_component_of_type(StatsComponent)
        if not stats:
            return 1.0

        # Résistance basée sur volonté normalisée
        if hasattr(stats, 'get_resistance_level'):
            return stats.get_resistance_level()
        else:
            # Fallback calculation
            volonte = getattr(stats, 'volonte', 100)
            excitation = getattr(stats, 'excitation', 0)

            # Calcul simple: volonté élevée + excitation faible = résistance élevée
            resistance = volonte / 100.0
            excitement_penalty = (excitation / 100.0) * 0.3

            return max(0.0, min(1.0, resistance - excitement_penalty))

    def get_arousal_level(self) -> float:
        """Retourne niveau excitation normalisé 0.0-1.0"""

        stats = self.get_component_of_type(StatsComponent)
        if not stats:
            return 0.0

        return getattr(stats, 'excitation', 0) / 100.0

    def get_clothing_state(self) -> Dict[str, Any]:
        """Retourne état détaillé vêtements"""

        clothing = self.get_component_of_type(ClothingComponent)
        if not clothing:
            return {"exposure": 0, "pieces": {}, "modified": []}

        modified_pieces = []
        if hasattr(clothing, 'pieces'):
            for piece, data in clothing.pieces.items():
                if data.get("state", "normale") != "normale":
                    modified_pieces.append({
                        "piece": piece,
                        "state": data["state"], 
                        "description": data.get("description", "")
                    })

        return {
            "exposure": getattr(clothing, 'exposure_level', 0),
            "pieces": getattr(clothing, 'pieces', {}),
            "modified": modified_pieces
        }

    def update_thresholds(self):
        """Met à jour seuils automatiques selon stats"""

        stats = self.get_component_of_type(StatsComponent)
        if not stats:
            return

        # Mise à jour seuils automatiques
        volonte = getattr(stats, 'volonte', 100)
        excitation = getattr(stats, 'excitation', 0)

        if hasattr(stats, 'thresholds'):
            stats.thresholds.update({
                "vulnerable": volonte <= 40,
                "aroused": excitation >= 60,
                "submissive": volonte <= 20, 
                "climax_ready": excitation >= 85
            })

    def to_dict(self) -> Dict[str, Any]:
        """Sérialisation enrichie"""

        base_dict = super().to_dict()
        base_dict.update({
            "name": self.name,
            "display_name": self.display_name,
            "current_state": self.get_current_state_summary(),
            "resistance": self.get_resistance_level(),
            "arousal": self.get_arousal_level()
        })
        return base_dict

# PLAYER V2.0: Méthodes complètes + compatibility + state management
