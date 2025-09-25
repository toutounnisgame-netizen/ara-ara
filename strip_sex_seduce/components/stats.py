"""
StatsComponent - Gestion résistance/excitation avec équilibrage
Composant central du gameplay pour le système résistance/cession
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from core.component import Component

@dataclass
class StatsComponent(Component):
    """
    Component gérant les stats principales du joueur
    - Volonté: Résistance aux actions (0-100)
    - Excitation: Niveau d'arousal (0-100)
    """

    # Stats principales
    volonte: int = 100          # Résistance joueur (0-100)
    excitation: int = 0         # Niveau arousal (0-100)

    # Seuils automatiques calculés
    thresholds: Dict[str, bool] = field(default_factory=lambda: {
        "vulnerable": False,     # volonte < 40
        "aroused": False,       # excitation > 60
        "submissive": False,    # volonte < 20
        "climax_ready": False   # excitation > 85
    })

    # Modificateurs temporaires
    modifiers: Dict[str, int] = field(default_factory=dict)

    # Historique pour debug et analytics
    history: List[Dict[str, Any]] = field(default_factory=list)

    # Limites min/max
    min_stat: int = 0
    max_stat: int = 100

    def __post_init__(self):
        """Initialisation après création"""
        super().__init__()
        self._update_thresholds()

    def apply_modifier(self, stat: str, value: int, temporary: bool = False, 
                      source: str = "unknown") -> Dict[str, int]:
        """
        Applique une modification de stat avec validation

        Args:
            stat: "volonte" ou "excitation" 
            value: Valeur à ajouter/soustraire
            temporary: Si True, effet diminuera avec le temps
            source: Source de la modification pour debug

        Returns:
            Dict avec anciennes et nouvelles valeurs
        """
        old_values = {"volonte": self.volonte, "excitation": self.excitation}

        if stat == "volonte":
            old_val = self.volonte
            self.volonte = max(self.min_stat, min(self.max_stat, self.volonte + value))
            actual_change = self.volonte - old_val

        elif stat == "excitation":
            old_val = self.excitation  
            self.excitation = max(self.min_stat, min(self.max_stat, self.excitation + value))
            actual_change = self.excitation - old_val

        else:
            raise ValueError(f"Stat inconnue: {stat}")

        # Gestion modificateurs temporaires
        if temporary:
            modifier_key = f"temp_{stat}"
            self.modifiers[modifier_key] = self.modifiers.get(modifier_key, 0) + value

        # Historique pour analytics
        self.history.append({
            "stat": stat,
            "value_requested": value,
            "value_actual": actual_change,
            "old_value": old_val,
            "new_value": getattr(self, stat),
            "source": source,
            "temporary": temporary
        })

        # Mise à jour seuils
        self._update_thresholds()
        self.mark_dirty()

        return {
            "old": old_values,
            "new": {"volonte": self.volonte, "excitation": self.excitation},
            "actual_change": actual_change
        }

    def _update_thresholds(self):
        """Met à jour automatiquement les seuils critiques"""
        self.thresholds.update({
            "vulnerable": self.volonte < 40,
            "aroused": self.excitation > 60,
            "submissive": self.volonte < 20,
            "climax_ready": self.excitation > 85
        })

    def apply_temporary_effects_decay(self, decay_rate: float = 0.8):
        """
        Diminue les effets temporaires à chaque tour

        Args:
            decay_rate: Taux de diminution (0.8 = -20% par tour)
        """
        for modifier_key in list(self.modifiers.keys()):
            if modifier_key.startswith("temp_"):
                self.modifiers[modifier_key] = int(self.modifiers[modifier_key] * decay_rate)

                # Supprime si effet négligeable
                if abs(self.modifiers[modifier_key]) < 1:
                    del self.modifiers[modifier_key]

        self._update_thresholds()

    def get_effective_stats(self) -> Dict[str, int]:
        """Retourne les stats avec modificateurs appliqués"""
        effective_volonte = self.volonte
        effective_excitation = self.excitation

        # Application modificateurs temporaires
        for key, value in self.modifiers.items():
            if "volonte" in key:
                effective_volonte = max(0, min(100, effective_volonte + value))
            elif "excitation" in key:
                effective_excitation = max(0, min(100, effective_excitation + value))

        return {
            "volonte": effective_volonte,
            "excitation": effective_excitation
        }

    def get_resistance_level(self) -> float:
        """Retourne le niveau de résistance normalisé (0.0-1.0)"""
        effective = self.get_effective_stats()
        return effective["volonte"] / 100.0

    def get_arousal_level(self) -> float:
        """Retourne le niveau d'excitation normalisé (0.0-1.0)"""
        effective = self.get_effective_stats()
        return effective["excitation"] / 100.0

    def is_in_threshold(self, threshold_name: str) -> bool:
        """Vérifie si un seuil particulier est atteint"""
        return self.thresholds.get(threshold_name, False)

    def get_history_summary(self) -> Dict[str, Any]:
        """Retourne un résumé de l'historique des modifications"""
        if not self.history:
            return {"total_changes": 0}

        total_changes = len(self.history)
        volonte_changes = [h for h in self.history if h["stat"] == "volonte"]
        excitation_changes = [h for h in self.history if h["stat"] == "excitation"]

        return {
            "total_changes": total_changes,
            "volonte_changes": len(volonte_changes),
            "excitation_changes": len(excitation_changes),
            "total_volonte_lost": sum(h["value_actual"] for h in volonte_changes if h["value_actual"] < 0),
            "total_excitation_gained": sum(h["value_actual"] for h in excitation_changes if h["value_actual"] > 0),
            "sources": list(set(h["source"] for h in self.history))
        }

    def reset_stats(self, volonte: int = 100, excitation: int = 0):
        """Remet les stats à des valeurs spécifiées"""
        self.volonte = max(self.min_stat, min(self.max_stat, volonte))
        self.excitation = max(self.min_stat, min(self.max_stat, excitation))
        self.modifiers.clear()
        self._update_thresholds()
        self.mark_dirty()

    def to_dict(self) -> Dict[str, Any]:
        """Sérialisation complète du component"""
        base_dict = super().to_dict()
        base_dict.update({
            "volonte": self.volonte,
            "excitation": self.excitation,
            "thresholds": self.thresholds.copy(),
            "modifiers": self.modifiers.copy(),
            "history_count": len(self.history),
            "effective_stats": self.get_effective_stats()
        })
        return base_dict

    def __repr__(self) -> str:
        return f"StatsComponent(V:{self.volonte}, E:{self.excitation}, thresholds:{sum(self.thresholds.values())})"
