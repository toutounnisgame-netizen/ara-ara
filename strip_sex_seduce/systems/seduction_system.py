"""
SeductionSystem V2.0 - Mécaniques séduction avancées et feedback NPC
"""
from core.system import System
from core.entity import Entity
from components.seduction import SeductionComponent, SeductionTechnique
from components.stats import StatsComponent
from components.progression import ProgressionComponent
from typing import List, Dict, Any, Optional
import random
import math

class SeductionSystem(System):
    """System pour mécaniques séduction et calcul effectiveness"""

    def __init__(self):
        super().__init__("SeductionSystem")
        self.technique_definitions = self._load_technique_definitions()
        self.effectiveness_cache = {}  # Cache calculs

    def update(self, entities: List[Entity], delta_time: float = 0.0, **kwargs):
        """Update système séduction"""
        for entity in entities:
            seduction_comp = entity.get_component_of_type(SeductionComponent)
            if seduction_comp:
                # Mise à jour cooldowns techniques
                seduction_comp.update_cooldowns()

                # Decay effets temporaires
                self._decay_temporary_effects(seduction_comp)

                # Calcul bonuses situationnels
                context = kwargs.get('context', {})
                if context:
                    self._update_situational_bonuses(entity, seduction_comp, context)

    def calculate_seduction_effectiveness(self, player_entity: Entity, action_data: Dict[str, Any], npc_entity: Entity, context: Dict[str, Any]) -> Dict[str, Any]:
        """Calcul effectiveness action séduction sur NPC"""
        seduction_comp = player_entity.get_component_of_type(SeductionComponent)
        stats_comp = player_entity.get_component_of_type(StatsComponent)

        if not seduction_comp:
            return {"effectiveness": 0.5, "analysis": "Pas de component séduction"}

        # Base effectiveness depuis l'action
        base_effectiveness = action_data.get("base_effectiveness", 0.5)

        # Modificateurs skill du joueur
        skill_modifiers = self._calculate_skill_modifiers(seduction_comp, action_data)

        # Modificateurs stats joueur
        stats_modifiers = self._calculate_stats_modifiers(stats_comp, context)

        # Modificateurs contextuels (lieu, timing, etc.)
        context_modifiers = self._calculate_context_modifiers(context)

        # Modificateurs réaction NPC
        npc_modifiers = self._calculate_npc_modifiers(npc_entity, action_data, context)

        # Effectiveness finale
        final_effectiveness = base_effectiveness + skill_modifiers + stats_modifiers + context_modifiers + npc_modifiers
        final_effectiveness = max(0.05, min(0.95, final_effectiveness))  # Clamp 5-95%

        # Calcul arousal impact sur NPC
        arousal_impact = self._calculate_arousal_impact(final_effectiveness, action_data, npc_entity, context)

        return {
            "effectiveness": final_effectiveness,
            "arousal_impact": arousal_impact,
            "breakdown": {
                "base": base_effectiveness,
                "skill": skill_modifiers,
                "stats": stats_modifiers,
                "context": context_modifiers,
                "npc_reaction": npc_modifiers
            },
            "analysis": self._generate_effectiveness_analysis(final_effectiveness, skill_modifiers, context_modifiers)
        }

    def _calculate_skill_modifiers(self, seduction_comp: SeductionComponent, action_data: Dict[str, Any]) -> float:
        """Modificateurs basés sur skills séduction"""
        modifiers = 0.0

        # Bonus niveau séduction général
        seduction_level = seduction_comp.seduction_level
        level_bonus = min(0.20, seduction_level * 0.02)  # Max +20% au niveau 10
        modifiers += level_bonus

        # Bonus technique maîtrisée
        action_category = action_data.get("category", "")
        matching_technique = None

        for technique in seduction_comp.mastered_techniques.values():
            if technique.category == action_category:
                matching_technique = technique
                break

        if matching_technique:
            technique_bonus = (matching_technique.mastery_level - 1) * 0.01  # +1% par niveau mastery
            modifiers += technique_bonus

        # Bonus style correspondant
        player_style = seduction_comp.seduction_style
        if player_style == "balanced":
            modifiers += 0.03  # Petit bonus partout
        elif player_style == action_category:
            modifiers += 0.08  # Gros bonus si spécialisé

        # Bonus success rate récent
        if seduction_comp.success_rate > 0.7:
            confidence_bonus = (seduction_comp.success_rate - 0.5) * 0.2  # Max +10%
            modifiers += confidence_bonus

        return modifiers

    def _calculate_stats_modifiers(self, stats_comp: Optional[StatsComponent], context: Dict[str, Any]) -> float:
        """Modificateurs basés sur stats joueur"""
        if not stats_comp:
            return 0.0

        modifiers = 0.0

        # Confiance du joueur (assume dans seduction_comp mais peut être dans stats)
        confidence = getattr(stats_comp, 'confiance', 50)  # Fallback
        if confidence > 80:
            modifiers += 0.10
        elif confidence > 60:
            modifiers += 0.05
        elif confidence < 30:
            modifiers -= 0.05

        # Énergie du joueur
        energy = getattr(stats_comp, 'energie', 100)
        if energy > 80:
            modifiers += 0.03
        elif energy < 30:
            modifiers -= 0.08  # Fatigue pénalise beaucoup

        # Arousal joueur (motivation)
        arousal = getattr(stats_comp, 'excitation', 0)
        if arousal > 60:
            modifiers += 0.06  # Plus motivée = plus efficace
        elif arousal < 20:
            modifiers -= 0.03  # Pas assez dans le mood

        return modifiers

    def _calculate_context_modifiers(self, context: Dict[str, Any]) -> float:
        """Modificateurs contextuels situation"""
        modifiers = 0.0

        # Privacy level - plus privé = actions plus efficaces
        privacy = context.get("privacy_level", 0.5)
        if privacy > 0.8:
            modifiers += 0.12  # Très privé
        elif privacy > 0.6:
            modifiers += 0.06  # Privé
        elif privacy < 0.3:
            modifiers -= 0.05  # Trop public peut gêner

        # Timing dans la session
        turn_count = context.get("turn_count", 0)
        if turn_count > 15:  # Session longue
            familiarity_bonus = min(0.08, turn_count * 0.003)  # Familiarité progressive
            modifiers += familiarity_bonus

        # Moment opportun (si NPC déjà excité)
        npc_arousal = context.get("npc_arousal", 0)
        if npc_arousal > 70:
            modifiers += 0.10  # Moment parfait
        elif npc_arousal > 50:
            modifiers += 0.05  # Bon timing

        # Cohérence avec actions précédentes
        last_action_success = context.get("last_action_success", None)
        if last_action_success is True:
            modifiers += 0.05  # Momentum positif
        elif last_action_success is False:
            modifiers -= 0.03  # Récupérer après échec

        return modifiers

    def _calculate_npc_modifiers(self, npc_entity: Entity, action_data: Dict[str, Any], context: Dict[str, Any]) -> float:
        """Modificateurs basés sur état et personnalité NPC"""
        modifiers = 0.0

        # Récupération stats NPC
        npc_stats = npc_entity.get_component_of_type(StatsComponent)
        npc_arousal = getattr(npc_stats, 'excitation', 0) if npc_stats else 0
        npc_patience = getattr(npc_stats, 'patience', 100) if npc_stats else 100

        # NPC très excité = plus réceptif
        if npc_arousal > 80:
            modifiers += 0.15
        elif npc_arousal > 60:
            modifiers += 0.08
        elif npc_arousal < 20:
            modifiers -= 0.05  # Pas encore dans le mood

        # NPC impatient = actions directes plus efficaces
        if npc_patience < 30:
            action_category = action_data.get("category", "")
            if action_category in ["direct", "physical"]:
                modifiers += 0.10  # Impatient = veut du concret
            elif action_category in ["subtle", "tease"]:
                modifiers -= 0.08  # Impatient = pas envie de jouer

        # Personnalité NPC (si component personality disponible)
        npc_personality = getattr(npc_entity, 'personality', None)
        if npc_personality:
            personality_type = getattr(npc_personality, 'base_personality', 'balanced')
            action_category = action_data.get("category", "")

            # Correspondances personnalité/action
            if personality_type == "dominant" and action_category == "submissive":
                modifiers += 0.12
            elif personality_type == "patient" and action_category == "subtle":
                modifiers += 0.08
            elif personality_type == "direct" and action_category == "physical":
                modifiers += 0.10

        return modifiers

    def _calculate_arousal_impact(self, effectiveness: float, action_data: Dict[str, Any], npc_entity: Entity, context: Dict[str, Any]) -> int:
        """Calcul impact arousal sur NPC"""
        base_arousal_impact = action_data.get("arousal_impact", 5)

        # Modification selon effectiveness
        impact_multiplier = 0.5 + (effectiveness * 1.0)  # 0.5x à 1.5x selon effectiveness

        # Facteur privacité - certaines actions plus impactantes en privé
        privacy_factor = 1.0
        action_category = action_data.get("category", "")
        privacy_level = context.get("privacy_level", 0.5)

        if action_category in ["physical", "explicit"] and privacy_level > 0.7:
            privacy_factor = 1.3  # Actions physiques plus impactantes en privé
        elif action_category in ["exhibition", "tease"] and privacy_level < 0.4:
            privacy_factor = 1.2  # Exhibition plus excitante en public

        # Calcul final avec variabilité
        final_impact = base_arousal_impact * impact_multiplier * privacy_factor
        final_impact *= random.uniform(0.8, 1.2)  # ±20% variabilité

        return max(1, int(round(final_impact)))

    def _decay_temporary_effects(self, seduction_comp: SeductionComponent):
        """Decay effets temporaires"""
        if hasattr(seduction_comp, 'temporary_bonuses'):
            for effect in list(seduction_comp.temporary_bonuses.keys()):
                current_value = seduction_comp.temporary_bonuses[effect]
                # Decay de 10% par turn
                new_value = current_value * 0.9
                if new_value < 0.5:  # Seuil minimum
                    del seduction_comp.temporary_bonuses[effect]
                else:
                    seduction_comp.temporary_bonuses[effect] = new_value

    def _update_situational_bonuses(self, entity: Entity, seduction_comp: SeductionComponent, context: Dict[str, Any]):
        """Met à jour bonus situationnels"""
        if not hasattr(seduction_comp, 'situational_bonuses'):
            seduction_comp.situational_bonuses = {}

        # Clear anciens bonuses
        seduction_comp.situational_bonuses.clear()

        # Nouveau bonus privacy
        privacy = context.get("privacy_level", 0.5)
        if privacy > 0.8:
            seduction_comp.situational_bonuses["privacy"] = 0.15

        # Bonus momentum si success récent
        if context.get("last_action_success"):
            seduction_comp.situational_bonuses["momentum"] = 0.08

    def recommend_best_action(self, player_entity: Entity, available_actions: List[Dict[str, Any]], npc_entity: Entity, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Recommande meilleure action selon contexte"""
        if not available_actions:
            return None

        best_action = None
        best_effectiveness = 0.0

        for action_data in available_actions:
            effectiveness_result = self.calculate_seduction_effectiveness(
                player_entity, action_data, npc_entity, context
            )

            if effectiveness_result["effectiveness"] > best_effectiveness:
                best_effectiveness = effectiveness_result["effectiveness"]
                best_action = action_data.copy()
                best_action["predicted_effectiveness"] = best_effectiveness
                best_action["predicted_arousal_impact"] = effectiveness_result["arousal_impact"]

        return best_action

    def _generate_effectiveness_analysis(self, final_effectiveness: float, skill_modifiers: float, context_modifiers: float) -> str:
        """Génère analyse textuelle effectiveness"""
        if final_effectiveness > 0.8:
            return f"Action très efficace ! Skill: {skill_modifiers:+.2f}, Contexte: {context_modifiers:+.2f}"
        elif final_effectiveness > 0.6:
            return f"Action efficace. Skill: {skill_modifiers:+.2f}, Contexte: {context_modifiers:+.2f}"
        elif final_effectiveness > 0.4:
            return f"Action moyennement efficace. Skill: {skill_modifiers:+.2f}, Contexte: {context_modifiers:+.2f}"
        else:
            return f"Action peu efficace. Skill: {skill_modifiers:+.2f}, Contexte: {context_modifiers:+.2f}"

    def unlock_new_techniques(self, player_entity: Entity) -> List[str]:
        """Débloque nouvelles techniques selon progression"""
        seduction_comp = player_entity.get_component_of_type(SeductionComponent)
        progression_comp = player_entity.get_component_of_type(ProgressionComponent)

        if not seduction_comp or not progression_comp:
            return []

        newly_unlocked = []
        level = seduction_comp.seduction_level

        # Définitions techniques débloquées par niveau
        level_unlocks = {
            3: ["technique_tease", "technique_eye_contact"],
            5: ["technique_physical_escalation", "technique_verbal_seduction"],
            7: ["technique_resistance_breaking", "technique_arousal_control"],
            10: ["technique_master_seduction", "technique_multi_stimulation"]
        }

        if level in level_unlocks:
            for technique_id in level_unlocks[level]:
                if technique_id not in seduction_comp.mastered_techniques:
                    # Créer technique
                    technique_data = self.technique_definitions.get(technique_id, {})
                    technique = SeductionTechnique(
                        technique_id=technique_id,
                        name=technique_data.get("name", technique_id),
                        category=technique_data.get("category", "balanced"),
                        effectiveness=technique_data.get("base_effectiveness", 0.6),
                        energy_cost=technique_data.get("energy_cost", 5)
                    )

                    # Apprentissage
                    if seduction_comp.learn_technique(technique):
                        newly_unlocked.append(technique_id)
                        progression_comp.unlock_technique(technique_id, "level_progression")

        return newly_unlocked

    def _load_technique_definitions(self) -> Dict[str, Any]:
        """Charge définitions techniques depuis assets ou défaut"""
        # Pour l'instant, définitions hardcodées
        return {
            "technique_tease": {
                "name": "Maîtrise du Tease",
                "category": "playful",
                "base_effectiveness": 0.65,
                "energy_cost": 3,
                "description": "Art de faire monter la tension par le jeu et la frustration contrôlée"
            },
            "technique_physical_escalation": {
                "name": "Escalation Physique",
                "category": "physical", 
                "base_effectiveness": 0.75,
                "energy_cost": 5,
                "description": "Progression naturelle et irrésistible des contacts physiques"
            },
            "technique_master_seduction": {
                "name": "Séduction Maîtresse",
                "category": "dominant",
                "base_effectiveness": 0.90,
                "energy_cost": 8,
                "description": "Contrôle total de l'escalation et des réactions masculines"
            }
        }

    def get_system_stats(self) -> Dict[str, Any]:
        """Statistiques système"""
        return {
            "system_name": self.name,
            "techniques_defined": len(self.technique_definitions),
            "cache_size": len(self.effectiveness_cache)
        }
