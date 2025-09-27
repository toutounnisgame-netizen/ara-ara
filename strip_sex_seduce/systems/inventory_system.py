"""
InventorySystem V2.0 - Gestion items érotiques et effets gameplay
"""
from core.system import System
from core.entity import Entity
from components.inventory import InventoryComponent, InventoryItem
from components.stats import StatsComponent
from components.seduction import SeductionComponent
from typing import List, Dict, Any, Optional
import json
import random

class InventorySystem(System):
    """System pour gestion complète items et équipements"""

    def __init__(self):
        super().__init__("InventorySystem")
        self.item_catalog = {}
        self.combination_effects = {}
        self._load_item_catalog()

    def _load_item_catalog(self):
        """Charge catalogue items depuis assets"""
        try:
            with open("assets/config/items_catalog.json", 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.item_catalog = config.get("items", {})
                self.combination_effects = config.get("combinations", {})
        except FileNotFoundError:
            # Catalogue par défaut
            self.item_catalog = self._get_default_item_catalog()
            self.combination_effects = self._get_default_combinations()

    def update(self, entities: List[Entity], delta_time: float = 0.0, **kwargs):
        """Update système inventory"""
        for entity in entities:
            inventory_comp = entity.get_component_of_type(InventoryComponent)
            if inventory_comp:
                # Mise à jour cooldowns items
                inventory_comp.update_cooldowns()

                # Vérification effets items équipés
                self._process_equipped_items_effects(entity, inventory_comp)

    def use_item(self, entity: Entity, item_id: str, target_entity: Optional[Entity] = None, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Utilise un item avec effets complets"""
        inventory_comp = entity.get_component_of_type(InventoryComponent)
        if not inventory_comp:
            return {"success": False, "error": "Pas d'inventory component"}

        # Vérification possession et disponibilité
        if not inventory_comp.has_item(item_id):
            return {"success": False, "error": f"Item {item_id} non possédé"}

        if inventory_comp.is_item_on_cooldown(item_id):
            cooldown = inventory_comp.item_cooldowns.get(item_id, 0)
            return {"success": False, "error": f"Item en cooldown ({cooldown} tours)"}

        # Récupération données item
        item_data = self.item_catalog.get(item_id)
        if not item_data:
            return {"success": False, "error": f"Item {item_id} non trouvé dans catalogue"}

        # Vérification requirements contextuels
        requirements_check = self._check_item_requirements(entity, item_data, context or {})
        if not requirements_check["valid"]:
            return {"success": False, "error": requirements_check["reason"]}

        # Application effets
        effects_result = self._apply_item_effects(entity, item_data, target_entity, context or {})

        # Consommation item si consumable
        if item_data.get("usage_type", "consumable") == "consumable":
            inventory_comp.use_item(item_id, 1)

        # Application cooldown
        cooldown = item_data.get("cooldown_turns", 0)
        if cooldown > 0:
            inventory_comp.item_cooldowns[item_id] = cooldown

        return {
            "success": True,
            "item_name": item_data.get("name", item_id),
            "effects": effects_result,
            "narrative": self._generate_usage_narrative(item_id, item_data, context or {})
        }

    def _check_item_requirements(self, entity: Entity, item_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Vérifie requirements usage item"""
        # Vérification lieu
        location_restrictions = item_data.get("location_restrictions", [])
        if location_restrictions:
            current_location = context.get("location", "bar")
            if current_location not in location_restrictions:
                return {"valid": False, "reason": f"Item non utilisable à {current_location}"}

        # Vérification arousal minimum
        arousal_req = item_data.get("arousal_requirements", 0)
        if arousal_req > 0:
            stats_comp = entity.get_component_of_type(StatsComponent)
            if stats_comp and getattr(stats_comp, 'excitation', 0) < arousal_req:
                return {"valid": False, "reason": f"Arousal insuffisant (requis: {arousal_req})"}

        # Vérification confiance minimum
        confidence_req = item_data.get("confidence_requirements", 0)
        if confidence_req > 0:
            # Assumé que confiance est dans seduction component
            seduction_comp = entity.get_component_of_type(SeductionComponent)
            confidence = getattr(seduction_comp, 'confidence', 50) if seduction_comp else 50
            if confidence < confidence_req:
                return {"valid": False, "reason": f"Confiance insuffisante (requis: {confidence_req})"}

        # Vérification énergie
        energy_cost = item_data.get("energy_cost", 0)
        if energy_cost > 0:
            stats_comp = entity.get_component_of_type(StatsComponent)
            energy = getattr(stats_comp, 'energie', 100) if stats_comp else 100
            if energy < energy_cost:
                return {"valid": False, "reason": f"Énergie insuffisante (requis: {energy_cost})"}

        return {"valid": True}

    def _apply_item_effects(self, entity: Entity, item_data: Dict[str, Any], target_entity: Optional[Entity], context: Dict[str, Any]) -> Dict[str, Any]:
        """Applique effets item sur entity"""
        effects_applied = {}
        item_effects = item_data.get("effects", {})

        stats_comp = entity.get_component_of_type(StatsComponent)
        seduction_comp = entity.get_component_of_type(SeductionComponent)

        # Effets sur stats principales
        for effect_name, effect_value in item_effects.items():
            if effect_name == "libido_boost" and stats_comp:
                old_arousal = getattr(stats_comp, 'excitation', 0)
                new_arousal = min(100, old_arousal + effect_value)
                stats_comp.excitation = new_arousal
                effects_applied["arousal"] = {"old": old_arousal, "new": new_arousal, "change": effect_value}

            elif effect_name == "confidence_boost" and seduction_comp:
                # Boost confiance temporaire
                if not hasattr(seduction_comp, 'temporary_bonuses'):
                    seduction_comp.temporary_bonuses = {}
                seduction_comp.temporary_bonuses["confidence"] = effect_value
                effects_applied["confidence"] = {"boost": effect_value, "duration": "temporary"}

            elif effect_name == "energy_restore" and stats_comp:
                old_energy = getattr(stats_comp, 'energie', 100)
                new_energy = min(100, old_energy + effect_value)
                stats_comp.energie = new_energy
                effects_applied["energy"] = {"old": old_energy, "new": new_energy, "change": effect_value}

            elif effect_name == "disinhibition" and stats_comp:
                # Réduction volonté temporaire
                old_volonte = getattr(stats_comp, 'volonte', 100)
                new_volonte = max(0, old_volonte - effect_value)
                stats_comp.volonte = new_volonte
                effects_applied["volonte"] = {"old": old_volonte, "new": new_volonte, "change": -effect_value}

        # Effets spéciaux selon item
        item_category = item_data.get("category", "")
        if item_category == "aphrodisiac":
            effects_applied.update(self._apply_aphrodisiac_effects(entity, item_data, context))
        elif item_category == "toy":
            effects_applied.update(self._apply_toy_effects(entity, item_data, context))
        elif item_category == "alcohol":
            effects_applied.update(self._apply_alcohol_effects(entity, item_data, context))

        # Effets sur NPC cible si présent
        if target_entity:
            target_effects = self._apply_target_effects(target_entity, item_data, context)
            if target_effects:
                effects_applied["target_effects"] = target_effects

        return effects_applied

    def _apply_aphrodisiac_effects(self, entity: Entity, item_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Effets spécifiques aphrodisiaques"""
        effects = {}

        # Boost libido mutuel
        stats_comp = entity.get_component_of_type(StatsComponent)
        if stats_comp:
            boost_amount = random.randint(15, 25)  # Variabilité
            old_arousal = getattr(stats_comp, 'excitation', 0)
            new_arousal = min(100, old_arousal + boost_amount)
            stats_comp.excitation = new_arousal

            effects["aphrodisiac_boost"] = {
                "amount": boost_amount,
                "old_arousal": old_arousal,
                "new_arousal": new_arousal
            }

        # Effet réchauffement corporel si gingembre
        if "gingembre" in item_data.get("item_id", ""):
            effects["body_warming"] = {"intensity": "high", "duration": 5}

        return effects

    def _apply_toy_effects(self, entity: Entity, item_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Effets spécifiques toys érotiques"""
        effects = {}

        toy_type = item_data.get("item_id", "")

        if "vibrator" in toy_type:
            # Auto-stimulation + démonstration
            stats_comp = entity.get_component_of_type(StatsComponent)
            if stats_comp:
                self_arousal_boost = 25
                old_arousal = getattr(stats_comp, 'excitation', 0)
                new_arousal = min(100, old_arousal + self_arousal_boost)
                stats_comp.excitation = new_arousal

                effects["self_stimulation"] = {
                    "toy": "vibrator",
                    "arousal_boost": self_arousal_boost,
                    "demonstration_effect": "high"
                }

        elif "plug" in toy_type:
            # Préparation + provocation
            effects["anal_preparation"] = {"ready": True, "provocation_level": "high"}

        elif "menottes" in toy_type:
            # BDSM léger
            effects["bdsm_play"] = {"type": "light", "control": "shared", "excitement": "high"}

        return effects

    def _apply_alcohol_effects(self, entity: Entity, item_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Effets spécifiques alcool"""
        effects = {}

        alcohol_type = item_data.get("item_id", "")
        stats_comp = entity.get_component_of_type(StatsComponent)

        if not stats_comp:
            return effects

        if "champagne" in alcohol_type:
            # Désinhibition progressive + ambiance romantique
            disinhibition = random.randint(10, 15)
            old_volonte = getattr(stats_comp, 'volonte', 100)
            new_volonte = max(0, old_volonte - disinhibition)
            stats_comp.volonte = new_volonte

            effects["champagne_effect"] = {
                "disinhibition": disinhibition,
                "ambiance": "romantic",
                "shared": True
            }

        elif "shots" in alcohol_type:
            # Désinhibition rapide intense
            disinhibition = random.randint(20, 30)
            old_volonte = getattr(stats_comp, 'volonte', 100)
            new_volonte = max(0, old_volonte - disinhibition)
            stats_comp.volonte = new_volonte

            effects["shots_effect"] = {
                "disinhibition": disinhibition,
                "intensity": "high",
                "rapid_onset": True
            }

        return effects

    def _apply_target_effects(self, target_entity: Entity, item_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Applique effets sur NPC cible"""
        effects = {}

        # Les aphrodisiaques et alcool affectent aussi le NPC
        category = item_data.get("category", "")
        if category in ["aphrodisiac", "alcohol"]:
            # Assume que NPC a des stats similaires
            target_stats = target_entity.get_component_of_type(StatsComponent)
            if target_stats:
                arousal_boost = random.randint(10, 20)
                old_arousal = getattr(target_stats, 'excitation', 0)
                new_arousal = min(100, old_arousal + arousal_boost)
                target_stats.excitation = new_arousal

                effects["npc_arousal_boost"] = {
                    "amount": arousal_boost,
                    "old": old_arousal,
                    "new": new_arousal
                }

        return effects

    def _generate_usage_narrative(self, item_id: str, item_data: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Génère description narrative usage item"""
        location = context.get("location", "bar")
        narratives = item_data.get("narrative_descriptions", {})

        # Description spécifique au lieu si disponible
        if location in narratives:
            return narratives[location]

        # Description générique
        return narratives.get("default", f"Tu utilises {item_data.get('name', item_id)}.")

    def _process_equipped_items_effects(self, entity: Entity, inventory_comp: InventoryComponent):
        """Traite effets items équipés en continu"""
        equipped_items = inventory_comp.get_equipped_items()

        for slot, item_id in equipped_items.items():
            item_data = self.item_catalog.get(item_id)
            if not item_data:
                continue

            # Effets passifs items équipés
            passive_effects = item_data.get("passive_effects", {})
            if passive_effects:
                self._apply_passive_effects(entity, passive_effects)

    def _apply_passive_effects(self, entity: Entity, passive_effects: Dict[str, Any]):
        """Applique effets passifs faibles mais continus"""
        stats_comp = entity.get_component_of_type(StatsComponent)
        seduction_comp = entity.get_component_of_type(SeductionComponent)

        # Effets très légers pour éviter exploitation
        for effect, value in passive_effects.items():
            if effect == "confidence_aura" and seduction_comp:
                # Micro-bonus confiance
                if not hasattr(seduction_comp, 'equipment_bonuses'):
                    seduction_comp.equipment_bonuses = {}
                seduction_comp.equipment_bonuses["confidence"] = value

    def get_available_items(self, entity: Entity, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Retourne items utilisables dans contexte actuel"""
        inventory_comp = entity.get_component_of_type(InventoryComponent)
        if not inventory_comp:
            return []

        available_items = []

        for item_id in inventory_comp.get_available_items():
            item_data = self.item_catalog.get(item_id)
            if not item_data:
                continue

            # Vérification requirements
            requirements_check = self._check_item_requirements(entity, item_data, context)
            if requirements_check["valid"]:
                available_items.append({
                    "item_id": item_id,
                    "name": item_data.get("name", item_id),
                    "description": item_data.get("description", ""),
                    "category": item_data.get("category", ""),
                    "energy_cost": item_data.get("energy_cost", 0),
                    "quantity": inventory_comp.get_item_count(item_id)
                })

        return available_items

    def _get_default_item_catalog(self) -> Dict[str, Any]:
        """Catalogue items par défaut"""
        return {
            "champagne": {
                "name": "Champagne Dom Pérignon",
                "category": "alcohol",
                "description": "Champagne de luxe pour ambiance romantique",
                "effects": {"disinhibition": 12, "confidence_boost": 8},
                "usage_type": "consumable",
                "location_restrictions": ["bar", "salon", "chambre"],
                "energy_cost": 0,
                "cooldown_turns": 0,
                "narrative_descriptions": {
                    "bar": "Tu proposes de partager une coupe avec lui, vos regards se croisent...",
                    "salon": "Le champagne coule sur tes lèvres, il ne peut détacher ses yeux...",
                    "chambre": "Vous buvez au même verre, l'intimité monte d'un cran...",
                    "default": "Tu partages le champagne avec lui."
                }
            },
            "vibrator_discret": {
                "name": "Vibrator discret",
                "category": "toy",
                "description": "Jouet intime pour démonstration de désir",
                "effects": {"self_arousal": 25, "demonstration": 30},
                "usage_type": "reusable",
                "location_restrictions": ["salon", "chambre"],
                "arousal_requirements": 60,
                "confidence_requirements": 70,
                "energy_cost": 5,
                "cooldown_turns": 3,
                "narrative_descriptions": {
                    "salon": "Tu sors discrètement ton petit ami, ses yeux s'écarquillent...",
                    "chambre": "Tu lui montres ton jouet favori, il déglutit difficilement...",
                    "default": "Tu utilises ton vibrator devant lui."
                }
            }
            # Plus d'items...
        }

    def _get_default_combinations(self) -> Dict[str, Any]:
        """Effets combinations items par défaut"""
        return {
            "champagne+chocolat": {
                "name": "Aphrodisiaque Parfait",
                "combined_effects": {"arousal_boost": 35, "disinhibition": 20},
                "description": "La combinaison parfaite pour une soirée inoubliable"
            }
        }

    def get_system_stats(self) -> Dict[str, Any]:
        """Statistiques système"""
        return {
            "system_name": self.name,
            "items_in_catalog": len(self.item_catalog),
            "combinations_available": len(self.combination_effects)
        }
