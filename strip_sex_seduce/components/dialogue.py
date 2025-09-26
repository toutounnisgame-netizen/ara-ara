"""
DialogueComponent - Gestion dialogues contextuels adaptatifs
Génération de textes selon stats, vêtements et personnalité
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from core.component import Component

@dataclass
class DialogueComponent(Component):
    """
    Component gérant les dialogues et interactions textuelles
    Adaptatif selon le contexte et l'état du joueur
    """

    # État dialogue actuel
    current_scene: str = "introduction"
    current_location: str = "bar"

    # Choix disponibles pour le joueur
    available_choices: List[Dict[str, Any]] = field(default_factory=list)

    # Réponse/action NPC actuelle
    npc_response: str = ""
    npc_action_type: str = ""

    # Flags contextuels pour adaptation
    context_flags: List[str] = field(default_factory=list)

    # Historique dialogue pour cohérence
    dialogue_history: List[Dict[str, str]] = field(default_factory=list)

    # Cache des réponses générées pour performance
    _response_cache: Dict[str, List[str]] = field(default_factory=dict)

    def __post_init__(self):
        """Initialisation après création"""
        super().__init__()

    def add_choice(self, text: str, action: str, requirements: Dict = None, 
                  enabled: bool = True) -> None:
        """
        Ajoute un choix disponible pour le joueur

        Args:
            text: Texte affiché au joueur
            action: Action interne associée
            requirements: Conditions pour activer le choix
            enabled: Si le choix est disponible
        """
        choice = {
            "text": text,
            "action": action,
            "requirements": requirements or {},
            "enabled": enabled,
            "id": len(self.available_choices)
        }
        self.available_choices.append(choice)
        self.mark_dirty()

    def clear_choices(self):
        """Efface tous les choix actuels"""
        self.available_choices.clear()
        self.mark_dirty()

    def get_enabled_choices(self) -> List[Dict[str, Any]]:
        """Retourne seulement les choix activés"""
        return [choice for choice in self.available_choices if choice["enabled"]]

    def set_npc_response(self, response: str, action_type: str = ""):
        """Définit la réponse/action actuelle du NPC"""
        self.npc_response = response
        self.npc_action_type = action_type

        # Ajout à l'historique
        self.dialogue_history.append({
            "type": "npc_response",
            "content": response,
            "action_type": action_type,
            "location": self.current_location
        })

        # Limitation historique pour mémoire
        if len(self.dialogue_history) > 50:
            self.dialogue_history = self.dialogue_history[-40:]

        self.mark_dirty()

    def add_context_flag(self, flag: str):
        """Ajoute un flag contextuel"""
        if flag not in self.context_flags:
            self.context_flags.append(flag)
            self.mark_dirty()

    def remove_context_flag(self, flag: str):
        """Supprime un flag contextuel"""
        if flag in self.context_flags:
            self.context_flags.remove(flag)
            self.mark_dirty()

    def has_context_flag(self, flag: str) -> bool:
        """Vérifie la présence d'un flag contextuel"""
        return flag in self.context_flags

    def update_location_context(self, location: str):
        """Met à jour le contexte de lieu"""
        if location != self.current_location:
            self.current_location = location
            self.add_context_flag(f"location_{location}")
            self.mark_dirty()

    def get_dialogue_context(self) -> Dict[str, Any]:
        """Retourne le contexte complet pour génération dialogue"""
        return {
            "scene": self.current_scene,
            "location": self.current_location,
            "flags": self.context_flags.copy(),
            "history_count": len(self.dialogue_history),
            "last_npc_action": self.npc_action_type,
            "choices_available": len(self.available_choices)
        }

    def cache_response(self, key: str, responses: List[str]):
        """Met en cache des réponses générées"""
        self._response_cache[key] = responses

    def get_cached_response(self, key: str) -> Optional[List[str]]:
        """Récupère des réponses en cache"""
        return self._response_cache.get(key)

    def clear_cache(self):
        """Vide le cache de réponses"""
        self._response_cache.clear()

    def to_dict(self) -> Dict[str, Any]:
        """Sérialisation complète du component"""
        base_dict = super().to_dict()
        base_dict.update({
            "current_scene": self.current_scene,
            "current_location": self.current_location,
            "choices_count": len(self.available_choices),
            "context_flags": self.context_flags.copy(),
            "dialogue_history_count": len(self.dialogue_history),
            "npc_action_type": self.npc_action_type,
            "cache_size": len(self._response_cache)
        })
        return base_dict
