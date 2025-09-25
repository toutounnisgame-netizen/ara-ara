"""
PlayerCharacter - Correctif compatibilité méthodes manquantes
Résolution get_current_state_summary() et autres méthodes
"""

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

    # Stats base
    summary = {
        "stats": {
            "volonte": stats.volonte,
            "excitation": stats.excitation
        },
        "resistance": stats.get_resistance_level(),
        "arousal": stats.excitation / 100.0,  # Normalisé 0-1
        "exposure": 0,
        "clothing": []
    }

    # Ajout info vêtements si présent
    if clothing:
        summary["exposure"] = clothing.get_exposure_level()

        # Vêtements modifiés
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
    return stats.get_resistance_level()

# CORRECTIF PLAYERCHARACTER pour compatibilité complète
