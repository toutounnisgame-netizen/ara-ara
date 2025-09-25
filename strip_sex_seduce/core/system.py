"""
Core ECS - System Base Classes
Systems contiennent la logique et opèrent sur entities/components
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from core.entity import Entity
from core.component import Component, ComponentType
import time

class System(ABC):
    """
    Base class pour tous les systems ECS
    Un system contient la logique métier et opère sur les entities
    """

    def __init__(self, name: str = None):
        self.name = name or self.__class__.__name__
        self.enabled = True
        self._performance_stats = {
            "total_calls": 0,
            "total_time": 0.0,
            "avg_time": 0.0,
            "last_update_time": 0.0
        }

    @abstractmethod
    def update(self, entities: List[Entity], delta_time: float = 0.0, **kwargs) -> None:
        """
        Méthode principale d'update du system
        Doit être implémentée par chaque system concret
        """
        pass

    def filter_entities(self, entities: List[Entity], 
                       required_components: List[ComponentType]) -> List[Entity]:
        """
        Filtre les entities qui possèdent tous les components requis
        Optimisation pour éviter de traiter des entities non pertinentes
        """
        filtered = []
        for entity in entities:
            if all(entity.has_component(comp_type) for comp_type in required_components):
                filtered.append(entity)
        return filtered

    def update_with_performance_tracking(self, entities: List[Entity], 
                                       delta_time: float = 0.0, **kwargs) -> None:
        """
        Wrapper pour update avec tracking performance
        """
        if not self.enabled:
            return

        start_time = time.perf_counter()

        try:
            self.update(entities, delta_time, **kwargs)
        except Exception as e:
            print(f"❌ Erreur dans {self.name}: {e}")
            raise

        end_time = time.perf_counter()
        update_time = end_time - start_time

        # Mise à jour statistiques performance
        self._performance_stats["total_calls"] += 1
        self._performance_stats["total_time"] += update_time
        self._performance_stats["avg_time"] = (
            self._performance_stats["total_time"] / self._performance_stats["total_calls"]
        )
        self._performance_stats["last_update_time"] = update_time

    def get_performance_stats(self) -> Dict[str, float]:
        """Retourne les statistiques de performance"""
        return self._performance_stats.copy()

    def reset_performance_stats(self):
        """Remet à zéro les statistiques"""
        self._performance_stats = {
            "total_calls": 0,
            "total_time": 0.0,
            "avg_time": 0.0,
            "last_update_time": 0.0
        }

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(enabled={self.enabled})"

class SystemManager:
    """
    Gestionnaire centralisant tous les systems
    Responsable de l'ordre d'exécution et coordination
    """

    def __init__(self):
        self._systems: List[System] = []
        self._system_order: Dict[str, int] = {}

    def add_system(self, system: System, priority: int = 0):
        """
        Ajoute un system avec une priorité d'exécution
        Priority plus faible = exécution plus tôt
        """
        self._systems.append(system)
        self._system_order[system.name] = priority

        # Tri par priorité
        self._systems.sort(key=lambda s: self._system_order.get(s.name, 0))

    def remove_system(self, system_name: str) -> bool:
        """Supprime un system par son nom"""
        for i, system in enumerate(self._systems):
            if system.name == system_name:
                del self._systems[i]
                del self._system_order[system_name]
                return True
        return False

    def update_all(self, entities: List[Entity], delta_time: float = 0.0, **kwargs):
        """Met à jour tous les systems dans l'ordre de priorité"""
        for system in self._systems:
            system.update_with_performance_tracking(entities, delta_time, **kwargs)

    def get_system(self, system_name: str) -> Optional[System]:
        """Récupère un system par son nom"""
        for system in self._systems:
            if system.name == system_name:
                return system
        return None

    def get_all_systems(self) -> List[System]:
        """Retourne tous les systems"""
        return self._systems.copy()

    def get_performance_report(self) -> Dict[str, Dict]:
        """Génère un rapport de performance de tous les systems"""
        report = {}
        for system in self._systems:
            report[system.name] = system.get_performance_stats()
        return report

    def __len__(self) -> int:
        return len(self._systems)
