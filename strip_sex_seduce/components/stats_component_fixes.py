"""
StatsComponent - Correctifs méthodes manquantes
Ajout get_resistance_level() et autres méthodes critiques
"""

def get_resistance_level(self) -> float:
    """Retourne niveau résistance normalisé 0.0-1.0"""

    # Résistance basée sur volonté (0-100 -> 0.0-1.0)
    resistance = self.volonte / 100.0

    # Ajustement selon excitation (plus excité = moins résistant)
    excitement_penalty = (self.excitation / 100.0) * 0.3

    # Résistance finale ajustée
    final_resistance = max(0.0, min(1.0, resistance - excitement_penalty))

    return final_resistance

def mark_dirty(self):
    """Marque component comme modifié pour update"""
    self.is_dirty = True

def mark_clean(self):
    """Marque component comme propre après update"""
    self.is_dirty = False

@property
def thresholds(self) -> Dict[str, bool]:
    """Property thresholds pour compatibilité"""

    return {
        "vulnerable": self.volonte <= 40,
        "aroused": self.excitation >= 50,
        "submissive": self.volonte <= 25,
        "climax_ready": self.excitation >= 80
    }

# AJOUT MÉTHODES MANQUANTES STATS COMPONENT
