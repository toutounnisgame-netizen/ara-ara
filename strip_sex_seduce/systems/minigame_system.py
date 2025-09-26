"""
MiniGameSystem V2.0 - Framework mini-jeux intégrés
"""
from core.system import System
from core.entity import Entity
from components.stats import StatsComponent
from components.seduction import SeductionComponent
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import random
import json

@dataclass
class MiniGameResult:
    """Résultat d'un mini-jeu"""
    success: bool
    score: int
    performance_rating: str  # poor, good, excellent
    effects: Dict[str, int]
    narrative_result: str
    bonus_unlocks: List[str]

class MiniGameSystem(System):
    """System pour gestion mini-jeux intégrés"""

    def __init__(self):
        super().__init__("MiniGameSystem")
        self.active_minigames = {}  # Sessions mini-jeux actives
        self.minigame_configs = {}
        self._load_minigame_configs()

    def _load_minigame_configs(self):
        """Charge configurations mini-jeux"""
        try:
            with open("assets/minigames/minigame_config.json", 'r', encoding='utf-8') as f:
                self.minigame_configs = json.load(f)
        except FileNotFoundError:
            self.minigame_configs = self._get_default_minigame_configs()

    def update(self, entities: List[Entity], delta_time: float = 0.0, **kwargs):
        """Update mini-jeux actifs"""
        # Cleanup mini-jeux terminés
        expired_games = []
        for session_id, game_session in self.active_minigames.items():
            if game_session.get('status') == 'completed':
                expired_games.append(session_id)

        for session_id in expired_games:
            del self.active_minigames[session_id]

    def start_minigame(self, game_type: str, player_entity: Entity, npc_entity: Entity, context: Dict[str, Any]) -> Dict[str, Any]:
        """Démarre nouveau mini-jeu"""
        if game_type not in self.minigame_configs:
            return {"success": False, "error": f"Mini-jeu {game_type} non configuré"}

        # Vérification requirements
        requirements_check = self._check_minigame_requirements(game_type, player_entity, context)
        if not requirements_check["valid"]:
            return {"success": False, "error": requirements_check["reason"]}

        # Création session mini-jeu
        session_id = f"{game_type}_{datetime.now().timestamp()}"
        game_config = self.minigame_configs[game_type]

        game_session = {
            "session_id": session_id,
            "game_type": game_type,
            "player_entity": player_entity,
            "npc_entity": npc_entity,
            "context": context.copy(),
            "config": game_config.copy(),
            "status": "active",
            "current_step": 0,
            "player_inputs": [],
            "performance_metrics": {
                "timing_scores": [],
                "choice_scores": [],
                "bonus_points": 0
            },
            "start_time": datetime.now()
        }

        self.active_minigames[session_id] = game_session

        # Génération description démarrage
        start_description = self._generate_minigame_start_description(game_type, game_config, context)

        return {
            "success": True,
            "session_id": session_id,
            "game_type": game_type,
            "description": start_description,
            "instructions": game_config.get("instructions", "Suivez les instructions à l'écran")
        }

    def handle_minigame_input(self, session_id: str, player_input: str) -> Dict[str, Any]:
        """Traite input joueur dans mini-jeu"""
        if session_id not in self.active_minigames:
            return {"success": False, "error": "Session mini-jeu non trouvée"}

        game_session = self.active_minigames[session_id]
        if game_session["status"] != "active":
            return {"success": False, "error": "Mini-jeu non actif"}

        game_type = game_session["game_type"]

        # Traitement selon type mini-jeu
        if game_type == "strip_tease":
            return self._handle_strip_tease_input(game_session, player_input)
        elif game_type == "massage_sensuel":
            return self._handle_massage_input(game_session, player_input)
        elif game_type == "des_desir":
            return self._handle_dice_input(game_session, player_input)
        elif game_type == "simulation_sexuelle":
            return self._handle_simulation_input(game_session, player_input)
        else:
            return {"success": False, "error": f"Type mini-jeu {game_type} non implémenté"}

    def _check_minigame_requirements(self, game_type: str, player_entity: Entity, context: Dict[str, Any]) -> Dict[str, Any]:
        """Vérifie requirements pour mini-jeu"""
        config = self.minigame_configs.get(game_type, {})
        requirements = config.get("requirements", {})

        # Vérification privacy level
        min_privacy = requirements.get("min_privacy", 0.0)
        current_privacy = context.get("privacy_level", 0.5)
        if current_privacy < min_privacy:
            return {"valid": False, "reason": f"Privacy insuffisante pour {game_type}"}

        # Vérification arousal
        min_arousal = requirements.get("min_arousal", 0)
        stats_comp = player_entity.get_component_of_type(StatsComponent)
        current_arousal = getattr(stats_comp, 'excitation', 0) if stats_comp else 0
        if current_arousal < min_arousal:
            return {"valid": False, "reason": f"Arousal insuffisant pour {game_type}"}

        # Vérification level séduction
        min_seduction_level = requirements.get("min_seduction_level", 0)
        seduction_comp = player_entity.get_component_of_type(SeductionComponent)
        current_level = seduction_comp.seduction_level if seduction_comp else 0
        if current_level < min_seduction_level:
            return {"valid": False, "reason": f"Niveau séduction insuffisant pour {game_type}"}

        return {"valid": True}

    def _generate_minigame_start_description(self, game_type: str, config: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Génère description démarrage mini-jeu"""
        descriptions = config.get("start_descriptions", {})
        location = context.get("location", "default")

        # Description spécifique au lieu ou générique
        return descriptions.get(location, descriptions.get("default", f"Mini-jeu {game_type} commence..."))

    # ========== STRIP-TEASE INTERACTIF ==========
    def _handle_strip_tease_input(self, game_session: Dict[str, Any], player_input: str) -> Dict[str, Any]:
        """Gestion strip-tease interactif"""
        current_step = game_session["current_step"]
        config = game_session["config"]

        if current_step == 0:  # Choix musique
            return self._strip_tease_choose_music(game_session, player_input)
        elif current_step == 1:  # Choix séquence déshabillage
            return self._strip_tease_choose_sequence(game_session, player_input)
        elif current_step == 2:  # Exécution avec timing
            return self._strip_tease_execute(game_session, player_input)
        else:  # Fin
            return self._strip_tease_finale(game_session)

    def _strip_tease_choose_music(self, game_session: Dict[str, Any], choice: str) -> Dict[str, Any]:
        """Étape 1 strip-tease: choix musique"""
        music_options = {
            "1": {"type": "slow_sensuel", "tempo": "slow", "style_bonus": 15},
            "2": {"type": "upbeat_energique", "tempo": "fast", "style_bonus": 10},
            "3": {"type": "taquin_playful", "tempo": "variable", "style_bonus": 20}
        }

        if choice not in music_options:
            return {
                "success": False,
                "message": "Choix musique invalide. Options: 1=Sensuel, 2=Énergique, 3=Taquin",
                "continue": True
            }

        selected_music = music_options[choice]
        game_session["music_choice"] = selected_music
        game_session["current_step"] = 1

        return {
            "success": True,
            "message": f"🎵 Musique sélectionnée: {selected_music['type']}\n\n👗 SÉQUENCE DÉSHABILLAGE - Dans quel ordre ?\n1. Classique (haut → bas)\n2. Taquin (alternance)\n3. Surprise (ordre aléatoire)\n4. Personnalisé (tu choisis)",
            "continue": True
        }

    def _strip_tease_choose_sequence(self, game_session: Dict[str, Any], choice: str) -> Dict[str, Any]:
        """Étape 2: choix séquence déshabillage"""
        sequence_options = {
            "1": {"type": "classique", "sequence": ["chemisier", "jupe", "soutien_gorge", "culotte"]},
            "2": {"type": "taquin", "sequence": ["chemisier", "culotte", "jupe", "soutien_gorge"]},
            "3": {"type": "surprise", "sequence": ["soutien_gorge", "chemisier", "culotte", "jupe"]},
            "4": {"type": "personnalise", "sequence": ["chemisier", "jupe", "soutien_gorge", "culotte"]}  # Sera modifié
        }

        if choice not in sequence_options:
            return {
                "success": False,
                "message": "Séquence invalide. Choisis 1, 2, 3 ou 4.",
                "continue": True
            }

        selected_sequence = sequence_options[choice]
        game_session["sequence_choice"] = selected_sequence
        game_session["current_step"] = 2
        game_session["sequence_progress"] = 0

        return {
            "success": True,
            "message": f"🎭 Séquence choisie: {selected_sequence['type']}\n\n🎯 STRIP-TEASE COMMENCE !\n\n🎵 La musique démarre, tu commences ton show...\nIl te regarde, hypnotisé. Première pièce: {selected_sequence['sequence'][0]}\n\nTiming: 'lent' / 'normal' / 'rapide' / 'tease'",
            "continue": True
        }

    def _strip_tease_execute(self, game_session: Dict[str, Any], timing_choice: str) -> Dict[str, Any]:
        """Étape 3: exécution strip-tease"""
        valid_timings = ["lent", "normal", "rapide", "tease"]
        if timing_choice not in valid_timings:
            return {
                "success": False,
                "message": f"Timing invalide. Options: {', '.join(valid_timings)}",
                "continue": True
            }

        sequence = game_session["sequence_choice"]["sequence"]
        progress = game_session["sequence_progress"]
        current_piece = sequence[progress]

        # Calcul score timing
        timing_score = self._calculate_strip_timing_score(timing_choice, game_session["music_choice"]["tempo"])
        game_session["performance_metrics"]["timing_scores"].append(timing_score)

        # Génération narrative
        narrative = self._generate_strip_narrative(current_piece, timing_choice, timing_score)

        # Progression
        game_session["sequence_progress"] += 1

        if game_session["sequence_progress"] >= len(sequence):
            # Strip-tease terminé
            game_session["current_step"] = 3
            return self._strip_tease_finale(game_session)
        else:
            # Pièce suivante
            next_piece = sequence[game_session["sequence_progress"]]
            return {
                "success": True,
                "message": f"{narrative}\n\n▶️ PIÈCE SUIVANTE: {next_piece}\nTiming: 'lent' / 'normal' / 'rapide' / 'tease'",
                "continue": True,
                "score": timing_score
            }

    def _strip_tease_finale(self, game_session: Dict[str, Any]) -> Dict[str, Any]:
        """Finale strip-tease avec résultats"""
        # Calcul score total
        timing_scores = game_session["performance_metrics"]["timing_scores"]
        average_timing = sum(timing_scores) / len(timing_scores) if timing_scores else 50

        music_bonus = game_session["music_choice"]["style_bonus"]
        sequence_bonus = 10  # Bonus pour avoir terminé

        total_score = int(average_timing + music_bonus + sequence_bonus)
        total_score = min(100, max(0, total_score))

        # Rating performance
        if total_score >= 85:
            rating = "excellent"
            narrative = "🔥 STRIP-TEASE PARFAIT ! Il est complètement hypnotisé, son excitation est à son maximum. Tu es une déesse de la séduction !"
            effects = {"npc_arousal": 30, "player_confidence": 20, "seduction_xp": 25}
        elif total_score >= 65:
            rating = "good"
            narrative = "✨ Excellent strip-tease ! Il ne peut détacher ses yeux, son pantalon devient très serré..."
            effects = {"npc_arousal": 20, "player_confidence": 15, "seduction_xp": 15}
        else:
            rating = "poor"
            narrative = "👍 Strip-tease correct, mais tu peux faire mieux. Il apprécie mais n'est pas encore complètement conquis."
            effects = {"npc_arousal": 10, "player_confidence": 5, "seduction_xp": 8}

        # Finalisation session
        game_session["status"] = "completed"

        result = MiniGameResult(
            success=True,
            score=total_score,
            performance_rating=rating,
            effects=effects,
            narrative_result=narrative,
            bonus_unlocks=["strip_tease_mastered"] if total_score >= 85 else []
        )

        return {
            "success": True,
            "minigame_completed": True,
            "result": result,
            "message": f"{narrative}\n\n📊 Score: {total_score}/100 ({rating})"
        }

    def _calculate_strip_timing_score(self, timing_choice: str, music_tempo: str) -> int:
        """Calcule score timing strip-tease"""
        base_scores = {"lent": 70, "normal": 60, "rapide": 50, "tease": 80}
        base_score = base_scores.get(timing_choice, 50)

        # Bonus si timing correspond à tempo musique
        if (timing_choice == "lent" and music_tempo == "slow") or            (timing_choice == "rapide" and music_tempo == "fast") or            (timing_choice == "tease" and music_tempo == "variable"):
            base_score += 20

        # Variabilité
        return base_score + random.randint(-10, 10)

    def _generate_strip_narrative(self, piece: str, timing: str, score: int) -> str:
        """Génère narrative strip-tease"""
        narratives = {
            "chemisier": {
                "lent": "Tu déboutonnes lentement ton chemisier, révélant progressivement ta peau nacrée...",
                "normal": "Tu ouvres ton chemisier avec assurance, dévoilant ton décolleté...",
                "rapide": "D'un geste rapide, tu ouvres complètement ton chemisier...",
                "tease": "Tu joues avec les boutons, les ouvrant et refermant, le faisant languir..."
            },
            "jupe": {
                "lent": "Tu fais glisser ta jupe le long de tes hanches, centimètre par centimètre...",
                "normal": "Tu fais descendre ta jupe, révélant tes jambes parfaites...",
                "rapide": "Ta jupe tombe au sol d'un coup, le surprenant...",
                "tease": "Tu soulèves et baisses ta jupe, jouant avec son impatience..."
            }
            # Plus de narratives...
        }

        base_narrative = narratives.get(piece, {}).get(timing, f"Tu retires {piece} avec style {timing}")

        if score >= 80:
            return f"{base_narrative} Il gémit doucement, complètement captivé."
        elif score >= 60:
            return f"{base_narrative} Son regard brûlant suit chacun de tes mouvements."
        else:
            return f"{base_narrative} Il apprécie mais reste encore maître de lui."

    # ========== MASSAGE SENSUEL ==========
    def _handle_massage_input(self, game_session: Dict[str, Any], player_input: str) -> Dict[str, Any]:
        """Mini-jeu massage sensuel"""
        # Implémentation similaire au strip-tease mais pour massage
        # Zones: épaules -> dos -> cuisses -> torse -> zones intimes
        # Techniques: pression, mouvement, rythme
        # Score selon progression et technique

        return {
            "success": True,
            "message": "🤲 Mini-jeu massage en développement... Utilise 'quit' pour sortir.",
            "continue": True
        }

    # ========== DÉS DU DÉSIR ==========  
    def _handle_dice_input(self, game_session: Dict[str, Any], player_input: str) -> Dict[str, Any]:
        """Mini-jeu dés du désir"""
        if player_input.lower() == "lancer":
            # Jet des 4 dés
            action_die = random.choice(["baiser", "caresse", "lécher", "sucer", "pénétrer"])
            zone_die = random.choice(["cou", "seins", "cuisses", "sexe", "anus", "bouche"])
            intensity_die = random.choice(["doux", "normal", "intense", "sauvage"])
            duration_die = random.choice(["5sec", "30sec", "2min", "jusqu'orgasme"])

            result_text = f"🎲 RÉSULTAT DÉS:\n"
            result_text += f"ACTION: {action_die}\n"
            result_text += f"ZONE: {zone_die}\n" 
            result_text += f"INTENSITÉ: {intensity_die}\n"
            result_text += f"DURÉE: {duration_die}\n\n"
            result_text += "Accepter: 'ok' | Relancer: 'relancer' | Modifier: 'modifier' | Veto: 'veto'"

            game_session["dice_result"] = {
                "action": action_die,
                "zone": zone_die,
                "intensity": intensity_die,
                "duration": duration_die
            }

            return {"success": True, "message": result_text, "continue": True}

        return {"success": True, "message": "🎲 Dés du Désir prêts ! Tape 'lancer' pour commencer.", "continue": True}

    # ========== SIMULATION SEXUELLE ==========
    def _handle_simulation_input(self, game_session: Dict[str, Any], player_input: str) -> Dict[str, Any]:
        """Mini-jeu simulation sexuelle complète"""
        # Positions débloquées, contrôle rythme/intensité, multiple orgasmes

        return {
            "success": True,
            "message": "🛏️ Simulation sexuelle en développement... Plus complexe à implémenter.",
            "continue": True
        }

    def _get_default_minigame_configs(self) -> Dict[str, Any]:
        """Configurations mini-jeux par défaut"""
        return {
            "strip_tease": {
                "name": "Strip-tease Interactif",
                "description": "Séduction par le déshabillage contrôlé",
                "requirements": {
                    "min_privacy": 0.6,
                    "min_arousal": 40,
                    "min_seduction_level": 3
                },
                "max_score": 100,
                "instructions": "Choisis musique, séquence et timing pour un strip-tease parfait",
                "start_descriptions": {
                    "salon": "Dans l'intimité du salon, tu décides de lui offrir un spectacle privé...",
                    "chambre": "Dans sa chambre, tu vas le rendre fou avec ton strip-tease...",
                    "default": "Tu décides de te déshabiller sensuellement pour lui..."
                }
            },
            "massage_sensuel": {
                "name": "Massage Sensuel", 
                "description": "Escalation par le massage érotique",
                "requirements": {
                    "min_privacy": 0.7,
                    "min_arousal": 50,
                    "min_seduction_level": 4
                },
                "max_score": 100,
                "instructions": "Zones, techniques et progression pour massage parfait"
            },
            "des_desir": {
                "name": "Dés du Désir",
                "description": "Hasard contrôlé pour actions érotiques",
                "requirements": {
                    "min_privacy": 0.8,
                    "min_arousal": 60,
                    "min_seduction_level": 5
                },
                "max_score": 100,
                "instructions": "Lance les dés et négocie le résultat"
            },
            "simulation_sexuelle": {
                "name": "Simulation Sexuelle Complète",
                "description": "Simulation positions et orgasmes",
                "requirements": {
                    "min_privacy": 1.0,
                    "min_arousal": 80,
                    "min_seduction_level": 8
                },
                "max_score": 100,
                "instructions": "Contrôle positions, rythme et intensité"
            }
        }

    def get_available_minigames(self, player_entity: Entity, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Retourne mini-jeux disponibles selon contexte"""
        available = []

        for game_type, config in self.minigame_configs.items():
            requirements_check = self._check_minigame_requirements(game_type, player_entity, context)
            if requirements_check["valid"]:
                available.append({
                    "game_type": game_type,
                    "name": config.get("name", game_type),
                    "description": config.get("description", ""),
                    "max_score": config.get("max_score", 100)
                })

        return available

    def get_system_stats(self) -> Dict[str, Any]:
        """Statistiques système"""
        return {
            "system_name": self.name,
            "minigames_configured": len(self.minigame_configs),
            "active_sessions": len(self.active_minigames)
        }
