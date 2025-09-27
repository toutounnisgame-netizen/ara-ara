"""
Inventory Component V2.0 - Gestion items érotiques et équipements
"""
from core.component import Component
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class InventoryItem:
    """Item individuel avec propriétés gameplay"""
    item_id: str
    name: str
    category: str  # alcohol, aphrodisiac, toy, tech, protection
    description: str
    effects: Dict[str, int] = field(default_factory=dict)
    usage_type: str = "consumable"  # consumable, reusable, permanent
    location_restrictions: List[str] = field(default_factory=list)
    arousal_requirements: int = 0
    confidence_requirements: int = 0
    energy_cost: int = 0
    cooldown_turns: int = 0
    narrative_descriptions: Dict[str, str] = field(default_factory=dict)
    combination_effects: Dict[str, Dict] = field(default_factory=dict)
    unlock_requirements: str = ""

@dataclass  
class InventoryComponent(Component):
    """Component inventory avec gestion équipements et effets"""

    # Items possédés avec quantités
    items: Dict[str, int] = field(default_factory=dict)

    # Items actuellement équipés/utilisés
    equipped: Dict[str, str] = field(default_factory=dict)

    # Items disponibles pour achat/déblocage
    available_items: Set[str] = field(default_factory=set)

    # Historique utilisation pour analytics
    usage_history: List[Dict[str, Any]] = field(default_factory=list)

    # Cooldowns actifs
    item_cooldowns: Dict[str, int] = field(default_factory=dict)

    def has_item(self, item_id: str) -> bool:
        """Vérifie possession item"""
        return item_id in self.items and self.items[item_id] > 0

    def get_item_count(self, item_id: str) -> int:
        """Retourne quantité item"""
        return self.items.get(item_id, 0)

    def add_item(self, item_id: str, quantity: int = 1) -> bool:
        """Ajoute items à l'inventory"""
        if item_id not in self.items:
            self.items[item_id] = 0
        self.items[item_id] += quantity
        self.mark_dirty()
        return True

    def use_item(self, item_id: str, quantity: int = 1) -> bool:
        """Utilise item si disponible"""
        if not self.has_item(item_id):
            return False

        if self.items[item_id] < quantity:
            return False

        self.items[item_id] -= quantity
        if self.items[item_id] <= 0:
            del self.items[item_id]

        # Log utilisation
        self.usage_history.append({
            "item_id": item_id,
            "quantity": quantity,
            "timestamp": datetime.now().isoformat(),
            "context": "used"
        })

        self.mark_dirty()
        return True

    def equip_item(self, item_id: str, slot: str) -> bool:
        """Équipe item dans slot spécifique"""
        if not self.has_item(item_id):
            return False

        self.equipped[slot] = item_id
        self.mark_dirty()
        return True

    def unequip_item(self, slot: str) -> Optional[str]:
        """Déséquipe item d'un slot"""
        if slot not in self.equipped:
            return None

        item_id = self.equipped[slot]
        del self.equipped[slot]
        self.mark_dirty()
        return item_id

    def is_item_on_cooldown(self, item_id: str) -> bool:
        """Vérifie si item est en cooldown"""
        return item_id in self.item_cooldowns and self.item_cooldowns[item_id] > 0

    def update_cooldowns(self) -> None:
        """Met à jour les cooldowns"""
        expired_items = []
        for item_id, cooldown in self.item_cooldowns.items():
            if cooldown > 0:
                self.item_cooldowns[item_id] -= 1
            if self.item_cooldowns[item_id] <= 0:
                expired_items.append(item_id)

        for item_id in expired_items:
            del self.item_cooldowns[item_id]

    def get_equipped_items(self) -> Dict[str, str]:
        """Retourne items équipés"""
        return self.equipped.copy()

    def get_available_items(self) -> List[str]:
        """Retourne items disponibles (pas en cooldown)"""
        available = []
        for item_id in self.items.keys():
            if not self.is_item_on_cooldown(item_id):
                available.append(item_id)
        return available

    def to_dict(self) -> Dict[str, Any]:
        """Sérialisation pour sauvegarde"""
        return {
            "items": self.items,
            "equipped": self.equipped,
            "available_items": list(self.available_items),
            "usage_count": len(self.usage_history),
            "cooldowns": self.item_cooldowns
        }

    def __repr__(self) -> str:
        return f"InventoryComponent(items={len(self.items)}, equipped={len(self.equipped)})"
