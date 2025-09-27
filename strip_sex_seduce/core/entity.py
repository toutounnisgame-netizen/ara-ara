"""
Core ECS - Entity Management
Une Entity est un conteneur d'ID avec des Components
"""

from typing import Dict, List, Optional, Type, TypeVar
from core.component import Component, ComponentType
import uuid

T = TypeVar('T', bound=Component)

class Entity:
    """
    Entity de base du système ECS
    Contient uniquement un ID et gère ses components
    """

    def __init__(self, entity_id: str = None):
        self.id = entity_id or f"entity_{uuid.uuid4().hex[:8]}"
        self._components: Dict[ComponentType, Component] = {}

    def add_component(self, component: Component) -> 'Entity':
        """
        Ajoute un component à l'entity
        Auto-détection du type de component
        """
        # Détection automatique du type
        component_type = self._detect_component_type(component)

        if component_type:
            component.entity_id = self.id
            self._components[component_type] = component
        else:
            raise ValueError(f"Type de component non reconnu: {type(component)}")

        return self

    def get_component(self, component_type: ComponentType) -> Optional[Component]:
        """Récupère un component par son type"""
        return self._components.get(component_type)

    def get_component_of_type(self, component_class: Type[T]) -> Optional[T]:
        """Récupère un component par sa classe"""
        for component in self._components.values():
            if isinstance(component, component_class):
                return component
        return None

    def has_component(self, component_type: ComponentType) -> bool:
        """Vérifie la présence d'un component"""
        return component_type in self._components

    def remove_component(self, component_type: ComponentType) -> bool:
        """Supprime un component"""
        if component_type in self._components:
            del self._components[component_type]
            return True
        return False

    def get_all_components(self) -> List[Component]:
        """Retourne tous les components de l'entity"""
        return list(self._components.values())

    def _detect_component_type(self, component: Component) -> Optional[ComponentType]:
        """Détecte automatiquement le type d'un component"""
        class_name = component.__class__.__name__.lower()

        if "stats" in class_name:
            return ComponentType.STATS
        elif "clothing" in class_name:
            return ComponentType.CLOTHING
        elif "dialogue" in class_name:
            return ComponentType.DIALOGUE
        elif "personality" in class_name:
            return ComponentType.PERSONALITY
        elif "action" in class_name:
            return ComponentType.ACTION

        return None

    def to_dict(self) -> Dict:
        """Sérialise l'entity complète"""
        return {
            "id": self.id,
            "components": {
                comp_type.value: comp.to_dict() 
                for comp_type, comp in self._components.items()
            }
        }

    def __repr__(self) -> str:
        return f"Entity(id={self.id}, components={len(self._components)})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Entity):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
