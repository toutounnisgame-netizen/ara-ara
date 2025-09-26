"""
Seduction Component V2.0 - Mécaniques séduction et techniques
"""
from core.component import Component
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class SeductionTechnique:
    """Technique de séduction maîtrisée"""
    technique_id: str
    name: str
    category: str  # subtle, direct, playful, dominant
    effectiveness: float  # 0.0-1.0
    energy_cost: int
    unlock_requirements: Dict[str, Any] = field(default_factory=dict)
    mastery_level: int = 1  # 1-10
    usage_count: int = 0

@dataclass
class SeductionComponent(Component):
    """Component séduction avec techniques et progression"""

    # Niveau général de séduction
    seduction_level: int = 0

    # Techniques maîtrisées
    mastered_techniques: Dict[str, SeductionTechnique] = field(default_factory=dict)

    # Style de séduction préféré
    seduction_style: str = "balanced"  # subtle, direct, playful, dominant, balanced

    # Taux de succès global
    success_rate: float = 0.5

    # Historique succès/échecs pour analytics
    success_history: List[Dict[str, Any]] = field(default_factory=list)

    # Bonus selon situation
    situational_bonuses: Dict[str, float] = field(default_factory=dict)

    # Techniques en cooldown
    technique_cooldowns: Dict[str, int] = field(default_factory=dict)

    # Progression vers prochain niveau
    experience_points: int = 0
    experience_to_next_level: int = 100

    def learn_technique(self, technique: SeductionTechnique) -> bool:
        """Apprend nouvelle technique"""
        if technique.technique_id in self.mastered_techniques:
            return False  # Déjà connue

        self.mastered_techniques[technique.technique_id] = technique
        self.mark_dirty()
        return True

    def improve_technique(self, technique_id: str) -> bool:
        """Améliore technique existante"""
        if technique_id not in self.mastered_techniques:
            return False

        technique = self.mastered_techniques[technique_id]
        if technique.mastery_level < 10:
            technique.mastery_level += 1
            technique.effectiveness = min(1.0, technique.effectiveness + 0.05)
            self.mark_dirty()
            return True
        return False

    def use_technique(self, technique_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Utilise technique de séduction"""
        if technique_id not in self.mastered_techniques:
            return {"success": False, "error": "Technique inconnue"}

        if self.is_technique_on_cooldown(technique_id):
            return {"success": False, "error": "Technique en cooldown"}

        technique = self.mastered_techniques[technique_id]

        # Calcul effectiveness avec contexte
        base_effectiveness = technique.effectiveness
        style_bonus = self._get_style_bonus(technique.category)
        situational_bonus = self._get_situational_bonus(context)

        final_effectiveness = min(1.0, base_effectiveness + style_bonus + situational_bonus)

        # Jet de succès
        import random
        success = random.random() < final_effectiveness

        # Mise à jour statistiques
        technique.usage_count += 1
        self._record_technique_use(technique_id, success, final_effectiveness, context)

        # Application cooldown
        if technique.cooldown_turns > 0:
            self.technique_cooldowns[technique_id] = technique.cooldown_turns

        # Gain XP
        xp_gain = 10 if success else 5
        self._gain_experience(xp_gain)

        self.mark_dirty()

        return {
            "success": success,
            "effectiveness": final_effectiveness,
            "xp_gained": xp_gain,
            "technique": technique.name,
            "style_bonus": style_bonus,
            "situational_bonus": situational_bonus
        }

    def _get_style_bonus(self, technique_category: str) -> float:
        """Bonus selon style préféré"""
        if self.seduction_style == "balanced":
            return 0.05  # Petit bonus partout
        elif self.seduction_style == technique_category:
            return 0.15  # Gros bonus si correspondance
        else:
            return 0.0   # Pas de bonus

    def _get_situational_bonus(self, context: Dict[str, Any]) -> float:
        """Bonus selon situation actuelle"""
        total_bonus = 0.0

        # Bonus lieu privé pour techniques directes
        privacy = context.get('privacy_level', 0.5)
        if privacy > 0.8:
            total_bonus += 0.10

        # Bonus arousal cible élevé
        target_arousal = context.get('target_arousal', 0.5)
        if target_arousal > 0.7:
            total_bonus += 0.08

        # Bonus confiance joueur élevée
        confidence = context.get('player_confidence', 50)
        if confidence > 80:
            total_bonus += 0.12

        return min(0.3, total_bonus)  # Max 30% bonus

    def _record_technique_use(self, technique_id: str, success: bool, effectiveness: float, context: Dict[str, Any]) -> None:
        """Enregistre utilisation technique"""
        self.success_history.append({
            "technique_id": technique_id,
            "success": success,
            "effectiveness": effectiveness,
            "timestamp": datetime.now().isoformat(),
            "context": context.copy()
        })

        # Mise à jour success rate global
        if len(self.success_history) > 0:
            recent_successes = sum(1 for h in self.success_history[-20:] if h['success'])
            self.success_rate = recent_successes / min(20, len(self.success_history))

        # Limite historique
        if len(self.success_history) > 100:
            self.success_history = self.success_history[-50:]

    def _gain_experience(self, xp: int) -> bool:
        """Gagne XP et vérifie level up"""
        self.experience_points += xp

        if self.experience_points >= self.experience_to_next_level:
            # Level up!
            self.experience_points -= self.experience_to_next_level
            self.seduction_level += 1
            self.experience_to_next_level = int(self.experience_to_next_level * 1.2)  # Augmente requis

            # Bonus level up
            self._apply_level_up_bonuses()
            return True
        return False

    def _apply_level_up_bonuses(self) -> None:
        """Applique bonus de level up"""
        # Amélioration success rate base
        self.success_rate = min(0.95, self.success_rate + 0.02)

        # Débloque nouvelles techniques selon niveau
        # (sera géré par le ProgressionSystem)
        pass

    def is_technique_on_cooldown(self, technique_id: str) -> bool:
        """Vérifie cooldown technique"""
        return technique_id in self.technique_cooldowns and self.technique_cooldowns[technique_id] > 0

    def update_cooldowns(self) -> None:
        """Met à jour cooldowns techniques"""
        expired = []
        for technique_id, cooldown in self.technique_cooldowns.items():
            if cooldown > 0:
                self.technique_cooldowns[technique_id] -= 1
            if self.technique_cooldowns[technique_id] <= 0:
                expired.append(technique_id)

        for technique_id in expired:
            del self.technique_cooldowns[technique_id]

    def get_available_techniques(self) -> List[SeductionTechnique]:
        """Retourne techniques utilisables"""
        available = []
        for technique in self.mastered_techniques.values():
            if not self.is_technique_on_cooldown(technique.technique_id):
                available.append(technique)
        return available

    def get_best_technique_for_context(self, context: Dict[str, Any]) -> Optional[str]:
        """Recommande meilleure technique selon contexte"""
        available = self.get_available_techniques()
        if not available:
            return None

        best_technique = None
        best_score = 0.0

        for technique in available:
            effectiveness = technique.effectiveness
            style_bonus = self._get_style_bonus(technique.category)
            situational_bonus = self._get_situational_bonus(context)

            total_score = effectiveness + style_bonus + situational_bonus
            if total_score > best_score:
                best_score = total_score
                best_technique = technique.technique_id

        return best_technique

    def get_progression_summary(self) -> Dict[str, Any]:
        """Résumé progression pour affichage"""
        return {
            "seduction_level": self.seduction_level,
            "experience_points": self.experience_points,
            "experience_to_next": self.experience_to_next_level,
            "progress_percentage": (self.experience_points / self.experience_to_next_level) * 100,
            "success_rate": self.success_rate,
            "techniques_mastered": len(self.mastered_techniques),
            "style": self.seduction_style
        }

    def to_dict(self) -> Dict[str, Any]:
        """Sérialisation pour sauvegarde"""
        return {
            "seduction_level": self.seduction_level,
            "seduction_style": self.seduction_style,
            "success_rate": self.success_rate,
            "experience_points": self.experience_points,
            "techniques_count": len(self.mastered_techniques),
            "cooldowns": self.technique_cooldowns
        }

    def __repr__(self) -> str:
        return f"SeductionComponent(level={self.seduction_level}, techniques={len(self.mastered_techniques)}, style={self.seduction_style})"
