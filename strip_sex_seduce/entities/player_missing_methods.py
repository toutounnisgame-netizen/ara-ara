"""
PlayerCharacter - Correctifs méthodes manquantes critiques
Résolution get_current_state_summary() et get_resistance_level()
"""

def get_current_state_summary(self) -> Dict[str, Any]:
    """Retourne résumé état joueur actuel pour systems"""

    from components.stats import StatsComponent
    from components.clothing import ClothingComponent

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
            "volonte": getattr(stats, 'volonte', 100),
            "excitation": getattr(stats, 'excitation', 0)
        },
        "resistance": stats.get_resistance_level() if hasattr(stats, 'get_resistance_level') else 1.0,
        "arousal": getattr(stats, 'excitation', 0) / 100.0,  # Normalisé 0-1
        "exposure": 0,
        "clothing": []
    }

    # Ajout info vêtements si présent
    if clothing:
        if hasattr(clothing, 'get_exposure_level'):
            summary["exposure"] = clothing.get_exposure_level()

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

    from components.stats import StatsComponent

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

        # Simple calculation: volonté élevée + excitation faible = résistance élevée
        resistance = volonte / 100.0
        excitement_penalty = (excitation / 100.0) * 0.3

        return max(0.0, min(1.0, resistance - excitement_penalty))

# AJOUT MÉTHODES PLAYER pour compatibilité totale
