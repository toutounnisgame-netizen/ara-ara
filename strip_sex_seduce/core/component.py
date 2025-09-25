"""
Core ECS - Component Base Classes
Architecture Entity-Component-System stricte
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import json

class ComponentType(Enum):
    """Types de components disponibles"""
    STATS = "stats"
    CLOTHING = "clothing"
    DIALOGUE = "dialogue"
    PERSONALITY = "personality"
    ACTION = "action"

class Component(ABC):
    """
    Base class pour tous les components ECS
    Un component ne contient que des données, pas de logique
    """

    def __init__(self):
        self._entity_id: Optional[str] = None
        self._dirty = False  # Flag pour optimisation updates

    @property
    def entity_id(self) -> Optional[str]:
        return self._entity_id

    @entity_id.setter  
    def entity_id(self, value: str):
        self._entity_id = value

    @property
    def is_dirty(self) -> bool:
        return self._dirty

    def mark_dirty(self):
        """Marque le component comme modifié"""
        self._dirty = True

    def mark_clean(self):
        """Marque le component comme synchronisé"""
        self._dirty = False

    def to_dict(self) -> Dict[str, Any]:
        """Sérialise le component en dictionnaire"""
        return {
            "type": self.__class__.__name__,
            "entity_id": self._entity_id,
            "dirty": self._dirty
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Component':
        """Désérialise depuis dictionnaire"""
        instance = cls()
        instance._entity_id = data.get("entity_id")
        instance._dirty = data.get("dirty", False)
        return instance

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(entity_id={self._entity_id})"
