"""
StatsComponent V3.0 - Gestion stats avec seuils automatiques
"""
from core.component import Component
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class StatsComponent(Component):
    """Component stats avec gestion automatique seuils et modifications"""

    # Stats principales
    volonte: int = 100          # Résistance joueur (0-100)
    excitation: int = 0         # Arousal niveau (0-100)

    # Seuils automatiques
    thresholds: dict = field(default_factory=lambda: {
        "vulnerable": False,     # volonte < 40
        "aroused": False,        # excitation > 60
        "submissive": False,     # volonte < 20
        "climax_ready": False    # excitation > 85
    })

    # Modificateurs temporaires
    modifiers: dict = field(default_factory=dict)

    # Historique pour debug et analytics
    history: list = field(default_factory=list)

    # Métadonnées
    last_modified: str = ""
    is_dirty: bool = False      # Flag pour optimisation affichage

    def apply_modifier(self, stat_name: str, value: int, source: str = "unknown") -> Dict[str, Any]:
        """Applique modification stat avec validation et logging"""
        old_value = getattr(self, stat_name, 0)

        # Application modification avec limites
        if stat_name == "volonte":
            new_value = max(0, min(100, old_value + value))
            self.volonte = new_value
        elif stat_name == "excitation":
            new_value = max(0, min(100, old_value + value))
            self.excitation = new_value
        else:
            return {"success": False, "error": f"Stat inconnue: {stat_name}"}

        actual_change = new_value - old_value

        # Logging modification
        self.history.append({
            "timestamp": datetime.now().isoformat(),
            "stat": stat_name,
            "old_value": old_value,
            "new_value": new_value,
            "modifier": value,
            "actual_change": actual_change,
            "source": source
        })

        # Update seuils automatiques
        self._update_thresholds()

        # Marquer comme modifié pour affichage
        self.mark_dirty()
        self.last_modified = datetime.now().isoformat()

        return {
            "success": True,
            "old_value": old_value,
            "new_value": new_value,
            "actual_change": actual_change
        }

    def _update_thresholds(self):
        """Met à jour les seuils automatiques"""
        self.thresholds["vulnerable"] = self.volonte < 40
        self.thresholds["aroused"] = self.excitation > 60
        self.thresholds["submissive"] = self.volonte < 20
        self.thresholds["climax_ready"] = self.excitation > 85

    def apply_temporary_effects_decay(self, decay_rate: float = 0.95):
        """Applique decay aux effets temporaires"""
        for effect, value in self.modifiers.items():
            if isinstance(value, (int, float)):
                self.modifiers[effect] = value * decay_rate
                if abs(self.modifiers[effect]) < 0.1:
                    del self.modifiers[effect]

    def get_resistance_level(self) -> float:
        """Retourne niveau résistance normalisé (0.0-1.0)"""
        return self.volonte / 100.0

    def get_arousal_level(self) -> float:
        """Retourne niveau arousal normalisé (0.0-1.0)"""
        return self.excitation / 100.0

    def mark_dirty(self):
        """Marque component comme modifié pour affichage"""
        self.is_dirty = True

    def mark_clean(self):
        """Marque component comme traité pour affichage"""
        self.is_dirty = False

    def get_current_state(self) -> Dict[str, Any]:
        """Retourne état actuel complet"""
        return {
            "volonte": self.volonte,
            "excitation": self.excitation,
            "resistance_level": self.get_resistance_level(),
            "arousal_level": self.get_arousal_level(),
            "thresholds": self.thresholds.copy(),
            "modifiers": self.modifiers.copy(),
            "is_dirty": self.is_dirty
        }

    def to_dict(self) -> Dict[str, Any]:
        """Sérialisation pour sauvegarde"""
        return {
            "volonte": self.volonte,
            "excitation": self.excitation,
            "thresholds": self.thresholds,
            "modifiers": self.modifiers,
            "last_modified": self.last_modified,
            "history_count": len(self.history)
        }

    def __repr__(self) -> str:
        return f"StatsComponent(volonte={self.volonte}, excitation={self.excitation}, thresholds_active={sum(self.thresholds.values())})"
