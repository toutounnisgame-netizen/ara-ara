"""
GameSession V3.0 - CONSOLIDÉ OPTIMISÉ
Toutes les corrections et améliorations intégrées dans un fichier unique
"""
from core.system import SystemManager
from core.entity import Entity
from entities.player import PlayerCharacter
from entities.npc import NPCMale
from entities.environment import Environment
from entities.game_state import GameState
from utils.performance import PerformanceMonitor
from utils.logger import GameLogger
from systems.stats_system import StatsSystem
from systems.clothing_system import ClothingSystem
from systems.ai_system import AISystem
from systems.dialogue_system import DialogueSystem
from systems.input_system import InputSystem
from typing import Dict, List, Any, Optional
import time
import json

class GameSession:
    """
    Orchestrateur principal V3.0 - CONSOLIDÉ OPTIMISÉ
    Intègre toutes les corrections et améliorations
    """

    def __init__(self, config_path: str = "assets/config/settings.json"):
        # Logging et monitoring
        self.logger = GameLogger()
        self.performance_monitor = PerformanceMonitor()

        # Configuration
        self.config = self._load_config(config_path)

        # Entities principales
        self.player = PlayerCharacter("Joueuse")
        self.npc = NPCMale()
        self.game_state = GameState()

        # Environments avec propriétés escalation
        self.environments = {
            "bar": Environment("bar", "Le Moonlight - Bar Lounge", 
                             privacy_level=0.2, escape_difficulty=0.1),
            "voiture": Environment("voiture", "Dans sa voiture", 
                                 privacy_level=0.6, escape_difficulty=0.3),
            "salon": Environment("salon", "Son appartement - Salon", 
                               privacy_level=0.8, escape_difficulty=0.5),
            "chambre": Environment("chambre", "Sa chambre", 
                                 privacy_level=1.0, escape_difficulty=0.7)
        }
        self.current_environment = self.environments["bar"]

        # Liste complète des entities
        self.entities = [
            self.player,
            self.npc,
            self.game_state,
            *self.environments.values()
        ]

        # Systems manager
        self.system_manager = SystemManager()
        self._setup_systems()

        # État du game loop
        self.running = False
        self.paused = False
        self.last_update_time = 0.0

        # Cache pour optimisation
        self._input_cache = {}
        self._response_cache = {}

        # Initialisation
        self.logger.info(f"GameSession V3.0 initialisée avec {len(self.entities)} entities")
        self.logger.info(f"Systems actifs: {len(self.system_manager)}")

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Charge la configuration depuis JSON"""
        default_config = {
            "game": {
                "title": "Strip, Sex & Seduce",
                "version": "3.0.0",
                "debug_mode": False
            },
            "performance": {
                "max_memory_mb": 5,
                "target_response_ms": 50,
                "cache_enabled": True
            },
            "gameplay": {
                "difficulty": "normal",
                "auto_save": False,
                "auto_escalation": True
            },
            "interface": {
                "show_stats": True,
                "show_help_hints": True,
                "rich_dialogues": True
            }
        }

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # Merge avec config par défaut
                for section in default_config:
                    if section not in config:
                        config[section] = default_config[section]
                    else:
                        for key, value in default_config[section].items():
                            if key not in config[section]:
                                config[section][key] = value
                return config
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.logger.warning(f"Erreur chargement config: {e}, utilisation config par défaut")
            return default_config

    def _setup_systems(self):
        """Configure tous les systems avec priorités optimisées"""
        # System de stats (priorité haute - doit s'exécuter en premier)
        stats_system = StatsSystem()
        self.system_manager.add_system(stats_system, priority=1)

        # System de vêtements (dépend des stats)
        clothing_system = ClothingSystem()
        self.system_manager.add_system(clothing_system, priority=2)

        # System IA (analyse l'état pour décider actions)
        ai_system = AISystem()
        self.system_manager.add_system(ai_system, priority=3)

        # System dialogues CORRIGÉ (génère textes selon état)
        dialogue_system = DialogueSystem()
        self.system_manager.add_system(dialogue_system, priority=4)

        # System input (traite les entrées utilisateur)
        input_system = InputSystem()
        self.system_manager.add_system(input_system, priority=5)

        self.logger.info("Systems V3.0 configurés avec priorités optimisées")

    def run_game_loop(self):
        """Lance le game loop principal optimisé"""
        self.logger.info("Démarrage game loop principal V3.0")
        self.running = True
        self.performance_monitor.start_session()

        try:
            # Affichage intro
            self._display_game_intro()

            # Game loop principal
            while self.running:
                loop_start = time.perf_counter()

                # 1. Affichage état actuel
                self._display_current_state()

                # 2. Tour NPC (action IA)
                npc_action = self._process_npc_turn()
                if npc_action:
                    # CORRIGÉ - Affichage texte riche au lieu de tuple debug
                    print(f"\n{npc_action['description']}")

                    # Affichage message adaptation IA si présent
                    if npc_action.get('adaptation_message'):
                        print(f"💭 {npc_action['adaptation_message']}")

                # 3. Input joueur
                player_input = self._get_player_input()

                # 4. Traitement input
                if not self._process_player_input(player_input):
                    continue  # Input invalide, recommencer

                # 5. Update de tous les systems
                self._update_systems()

                # 6. Check escalation automatique INTÉGRÉ
                if self.config['gameplay']['auto_escalation']:
                    self._check_auto_escalation()

                # 7. Check conditions de fin
                end_condition = self._check_end_conditions()
                if end_condition:
                    self._handle_game_end(end_condition)
                    break

                # 8. Nettoyage et optimisations
                self._cleanup_turn()

                # 9. Performance tracking
                loop_end = time.perf_counter()
                loop_time = (loop_end - loop_start) * 1000  # ms
                self.performance_monitor.record_loop_time(loop_time)

                # Check performance - pas critique mais informatif
                if loop_time > self.config["performance"]["target_response_ms"] * 2:
                    self.logger.warning(f"Performance lente: {loop_time:.1f}ms")

                self.game_state.advance_turn()

        except KeyboardInterrupt:
            self.logger.info("Jeu interrompu par l'utilisateur")
            print("\n\n⚠️ Jeu interrompu...")
        except Exception as e:
            self.logger.error(f"Erreur critique game loop: {e}")
            print(f"\n❌ Erreur critique: {e}")
        finally:
            self._cleanup_session()

    def _process_npc_turn(self) -> Optional[Dict[str, Any]]:
        """Traite le tour du NPC avec IA adaptative OPTIMISÉE"""
        # Contexte pour IA
        context = {
            "location": self.current_environment.location,
            "privacy_level": self.current_environment.privacy_level,
            "turn_count": self.game_state.turn_count,
            "last_action": getattr(self, '_last_npc_action', None),
            "last_success": getattr(self, '_last_action_success', False)
        }

        # IA choisit action
        chosen_action = self.npc.choose_next_action(
            self.player.get_resistance_level(),
            context
        )

        # CORRIGÉ - Récupération système dialogue pour génération texte RICHE
        dialogue_system = self.system_manager.get_system("DialogueSystem")
        if dialogue_system:
            description = dialogue_system.generate_npc_action_text(
                chosen_action,
                self.player,
                self.current_environment
            )

            # Message adaptation IA selon contexte
            adaptation_message = None
            if self.game_state.turn_count % 3 == 0:  # Periodiquement
                if context.get('last_success', False):
                    adaptation_message = dialogue_system.generate_adaptation_message("escalating")
                else:
                    adaptation_message = dialogue_system.generate_adaptation_message("becoming_patient")
        else:
            description = f"Il {chosen_action}."
            adaptation_message = None

        # Application des effets
        effects = self._apply_npc_action_effects(chosen_action)

        # Sauvegarde pour contexte suivant
        self._last_npc_action = chosen_action
        self._last_action_success = effects.get('success', False)

        return {
            'action': chosen_action,
            'description': description,
            'adaptation_message': adaptation_message,
            'effects': effects
        }

    def _apply_npc_action_effects(self, action: str) -> Dict[str, Any]:
        """Applique les effets d'une action NPC - OPTIMISÉ"""
        # Récupération système stats
        stats_system = self.system_manager.get_system("StatsSystem")
        if not stats_system:
            return {"success": False, "error": "StatsSystem non trouvé"}

        # Application des effets sur les stats joueur
        effects = stats_system.apply_npc_action(
            self.player,
            action,
            {
                "location": self.current_environment.location,
                "privacy": self.current_environment.privacy_level
            }
        )

        # Enregistrement pour analytics
        self.game_state.record_npc_action(
            action,
            effects.get('success', False),
            effects.get('escalation_level', 1)
        )

        return effects

    def _check_auto_escalation(self):
        """INTÉGRÉ - Vérification escalation automatique entre lieux"""
        player_summary = self.player.get_current_state_summary()
        current_loc = self.current_environment.location

        # Transition bar → voiture si excitation suffisante et volonté OK
        if (current_loc == "bar" and 
            player_summary["arousal"] > 0.3 and 
            player_summary["resistance"] < 0.8):
            print("\n🚗 >>> Il te propose de continuer dans sa voiture...")
            print("'Que dirais-tu d'aller faire un tour ? Il fait si beau ce soir...'")
            self.current_environment = self.environments["voiture"]
            self.game_state.change_location("voiture")
            return

        # Transition voiture → salon  
        elif (current_loc == "voiture" and
              player_summary["arousal"] > 0.6 and
              player_summary["resistance"] < 0.6):
            print("\n🏠 >>> Il t'emmène à son appartement...")
            print("'J'habite juste là, viens prendre un dernier verre chez moi.'")
            self.current_environment = self.environments["salon"]
            self.game_state.change_location("salon")
            return

        # Transition salon → chambre
        elif (current_loc == "salon" and
              player_summary["arousal"] > 0.8 and
              player_summary["resistance"] < 0.4):
            print("\n🛏️ >>> Il te guide vers sa chambre...")
            print("'Viens, nous serons plus... confortables dans ma chambre.'")
            self.current_environment = self.environments["chambre"]
            self.game_state.change_location("chambre")
            return

    def _get_player_input(self) -> str:
        """Récupère et valide l'input joueur"""
        # Affichage choix rapides
        print("\n💭 Actions rapides:")
        print("  r = résister  |  a = permettre  |  f = fuir  |  aide = commandes")

        # Input avec gestion erreurs
        try:
            player_input = input("\n> ").strip()

            # Cache pour éviter répétitions
            if player_input in self._input_cache:
                cache_count = self._input_cache[player_input]
                self._input_cache[player_input] = cache_count + 1
                if cache_count > 3:
                    print("💡 Vous répétez souvent cette action. Essayez autre chose ?")
            else:
                self._input_cache[player_input] = 1

            return player_input
        except (EOFError, KeyboardInterrupt):
            return "quit"

    def _process_player_input(self, raw_input: str) -> bool:
        """Traite l'input joueur avec toutes les corrections intégrées"""
        if not raw_input:
            return False

        # Récupération système input
        input_system = self.system_manager.get_system("InputSystem")
        if not input_system:
            print("❌ Système input non disponible")
            return False

        # Parse et validation
        parsed_input = input_system.parse_input(raw_input)
        if parsed_input["type"] == "invalid":
            print(f"❓ Commande non reconnue: '{raw_input}'. Tapez 'aide' pour voir les options.")
            return False

        # Traitement selon type
        if parsed_input["type"] == "command":
            return self._handle_player_command(parsed_input["value"])
        elif parsed_input["type"] == "choice":
            return self._handle_player_choice(parsed_input["value"])
        elif parsed_input["type"] == "quit":
            self.running = False
            return True

        return True

    def _handle_player_command(self, command: str) -> bool:
        """Gère les commandes joueur - SIGNATURE CORRIGÉE"""
        if command in ["aide", "help"]:
            self._display_help()
            return False  # Pas de tour consommé
        elif command in ["resist", "résister"]:
            return self._player_resist_action()
        elif command in ["allow", "permettre"]:
            return self._player_allow_action()
        elif command in ["flee", "fuir"]:
            return self._player_flee_action()
        elif command in ["look", "regarder"]:
            self._display_detailed_state()
            return False  # Pas de tour consommé
        elif command == "stats":
            self._display_detailed_stats()
            return False
        elif command == "quit":
            self.running = False
            return True

        return False

    def _player_resist_action(self) -> bool:
        """Traite une action de résistance du joueur - SIGNATURE CORRIGÉE"""
        # Récupération système stats
        stats_system = self.system_manager.get_system("StatsSystem")
        if not stats_system:
            return False

        # Tentative résistance avec signature CORRIGÉE
        resistance_result = stats_system.apply_player_resistance(
            self.player,
            "soft_resistance",
            {
                "location": self.current_environment.location,
                "privacy": getattr(self.current_environment, 'privacy_level', 0.5)
            }
        )

        if resistance_result.get("success", False):
            print("Tu essaies de résister doucement à ses avances...")
            if resistance_result.get("volonte_gained", 0) > 0:
                print("💪 Tu te sens un peu plus forte.")
        else:
            print("Tu n'arrives plus à résister efficacement...")

        # Enregistrement
        self.game_state.record_player_action(
            "resist",
            resistance_result.get("success", False),
            resistance_result.get("stats_before", {}),
            resistance_result.get("stats_after", {})
        )

        return True

    def _player_allow_action(self) -> bool:
        """Traite une action permissive du joueur"""
        print("Tu laisses faire, sans résister...")

        # Pas d'effets directs, mais influence l'IA NPC
        self.game_state.record_player_action(
            "allow", True, {}, {}
        )

        return True

    def _player_flee_action(self) -> bool:
        """Traite une tentative de fuite - OPTIMISÉE"""
        # Calcul chance de succès selon lieu et stats
        base_chance = 1.0 - self.current_environment.escape_difficulty

        # Modificateur selon volonté
        willpower_modifier = self.player.get_resistance_level() * 0.3

        # Chance finale
        success_chance = min(0.9, base_chance + willpower_modifier)

        import random
        success = random.random() < success_chance

        if success:
            print("✅ Tu réussis à t'échapper!")
            self.game_state.add_story_flag("escape_successful")
            self.running = False
        else:
            print("❌ Tu n'arrives pas à partir. Il te retient gentiment...")

        self.game_state.record_player_action("flee", success, {}, {})
        self.game_state.unlock_achievement("escape_attempted")

        return True

    def _display_game_intro(self):
        """Affiche l'introduction du jeu"""
        print("\n" + "="*60)
        print(f"🔥 {self.config['game']['title'].upper()} 🔥")
        print("="*60)
        print("\nVous êtes dans un bar élégant. Un homme charmant s'approche de vous...")
        print("💡 Tapez 'aide' à tout moment pour voir les commandes")
        print()

    def _display_current_state(self):
        """Affiche l'état actuel du jeu - OPTIMISÉ"""
        print("\n" + "-"*60)

        # Informations lieu
        print(f"📍 LIEU: {self.current_environment.display_name}")

        # Stats joueur - utilisation système stats pour affichage
        stats_system = self.system_manager.get_system("StatsSystem")
        if stats_system:
            stats_display = stats_system.get_stats_display_text(self.player)
            print(f"💪 VOLONTÉ: {stats_display['volonte']}  🔥 EXCITATION: {stats_display['excitation']}")

            # Affichage status si présent
            if stats_display.get('has_status', False):
                print(f"💫 ÉTAT: {stats_display['status']}")

        # État vêtements si modifié
        player_summary = self.player.get_current_state_summary()
        if player_summary.get('exposure', 0) > 0:
            clothing_desc = " | ".join(player_summary.get('clothing', []))
            print(f"👗 TENUE: {clothing_desc}")

        # Informations debug si activées
        if self.config['game']['debug_mode']:
            npc_state = self.npc.get_behavioral_state()
            print(f"🤖 DEBUG NPC: {npc_state.get('current_strategy', 'N/A')} "
                  f"(succès: {npc_state.get('success_rate', 0):.0%})")

        print("-"*60)

    def _display_help(self):
        """Affiche l'aide complète"""
        print("""
╔══════════════════════════════════════════════════════════╗
║ 🆘 AIDE - COMMANDES V3.0                                ║
╠══════════════════════════════════════════════════════════╣
║ ACTIONS PRINCIPALES:                                     ║
║ • r, résister → Résister à l'action NPC                 ║
║ • a, permettre → Laisser faire l'action                 ║
║ • f, fuir → Tenter de quitter la situation              ║
║                                                          ║
║ INFORMATIONS:                                            ║
║ • regarder → Observer l'environnement                   ║
║ • stats → Voir statistiques détaillées                  ║
║ • aide → Afficher cette aide                            ║
║                                                          ║
║ SYSTÈME:                                                 ║
║ • quit → Quitter le jeu                                 ║
║                                                          ║
║ NOUVEAUTÉS V3.0:                                        ║
║ • Dialogues riches contextuels                          ║
║ • Escalation automatique entre lieux                    ║
║ • IA adaptive avec feedback visible                     ║
║ • Performance optimisée <50ms                           ║
╚══════════════════════════════════════════════════════════╝
        """)

    def _update_systems(self):
        """Met à jour tous les systems"""
        # Calcul delta time
        current_time = time.perf_counter()
        delta_time = current_time - self.last_update_time
        self.last_update_time = current_time

        # Contexte global pour systems
        context = {
            "player": self.player,
            "npc": self.npc,
            "environment": self.current_environment,
            "game_state": self.game_state,
            "config": self.config
        }

        # Update tous les systems
        try:
            self.system_manager.update_all(self.entities, delta_time, **context)
        except Exception as e:
            self.logger.error(f"Erreur update systems: {e}")
            self.game_state.debug_info["error_count"] += 1

    def _check_end_conditions(self) -> Optional[str]:
        """Vérifie les conditions de fin de partie"""
        return self.game_state.check_end_conditions()

    def _handle_game_end(self, end_type: str):
        """Gère la fin de partie - ENRICHIE"""
        print("\n" + "="*60)
        if end_type == "submission_complete":
            print("🔥 FIN: CESSION TOTALE")
            print("Tu ne peux plus résister à ses avances...")
        elif end_type == "resistance_victory":
            print("💪 FIN: RÉSISTANCE VICTORIEUSE")
            print("Tu as réussi à maintenir tes limites malgré ses efforts.")
        elif end_type == "escape_success":
            print("🏃‍♀️ FIN: FUITE RÉUSSIE")
            print("Tu as réussi à t'échapper de la situation.")
        elif end_type == "time_limit":
            print("⏰ FIN: LIMITE DE TEMPS")
            print("La soirée se termine...")
        elif end_type == "max_escalation":
            print("🌟 FIN: ESCALATION MAXIMALE")
            print("Vous avez atteint l'intimité maximale...")
        print("="*60)

        # Affichage statistiques finales
        self._display_final_statistics()

    def _display_final_statistics(self):
        """Affiche les statistiques finales - ENRICHIES"""
        session_summary = self.game_state.get_session_summary()
        print("\n📊 STATISTIQUES FINALES:")
        print("-"*40)
        print(f"⏱️  Durée: {session_summary['session_info']['duration_seconds']//60:.0f} min")
        print(f"🎮 Tours joués: {session_summary['session_info']['turns']}")
        print(f"📍 Lieux visités: {session_summary['progression']['locations_visited']}/4")
        print(f"🏆 Achievements: {session_summary['achievements']['unlocked']}/{session_summary['achievements']['total']}")

        # Performance V3.0
        perf_stats = self.performance_monitor.get_session_stats()
        print(f"💾 Mémoire max: {perf_stats.get('max_memory_mb', 0):.1f} MB")
        print(f"⚡ Temps moyen: {perf_stats.get('avg_response_ms', 0):.0f} ms")

        # Stats dialogue système
        dialogue_system = self.system_manager.get_system("DialogueSystem")
        if dialogue_system:
            cache_stats = dialogue_system.get_cache_stats()
            print(f"🗣️ Cache dialogues: {cache_stats['hit_rate']:.1%} hit rate")

    def _cleanup_turn(self):
        """Nettoyage fin de tour"""
        # Limite cache input pour mémoire
        if len(self._input_cache) > 50:
            # Garde seulement les 30 plus récents
            items = list(self._input_cache.items())
            self._input_cache = dict(items[-30:])

    def _cleanup_session(self):
        """Nettoyage fin de session"""
        try:
            # Statistiques finales monitoring
            self.performance_monitor.end_session()

            # Log session summary
            summary = self.game_state.get_session_summary()
            self.logger.info(f"Session V3.0 terminée: {summary}")
        except Exception as e:
            self.logger.error(f"Erreur cleanup session: {e}")

        print("\n👋 Merci d'avoir joué Strip, Sex & Seduce V3.0 !")

    def _display_detailed_state(self):
        """Affiche état détaillé pour debug"""
        if not self.config['game']['debug_mode']:
            print("Mode debug non activé")
            return

        print("\n🔍 ÉTAT DÉTAILLÉ V3.0:")
        print(f"Player: {self.player}")
        print(f"NPC: {self.npc}")
        print(f"Environment: {self.current_environment}")
        print(f"Game State: {self.game_state}")

    def _display_detailed_stats(self):
        """Affiche statistiques détaillées"""
        summary = self.game_state.get_session_summary()
        print("\n📈 STATISTIQUES DÉTAILLÉES V3.0:")
        for section, data in summary.items():
            print(f"\n{section.upper()}:")
            if isinstance(data, dict):
                for key, value in data.items():
                    print(f"  {key}: {value}")
            else:
                print(f"  {data}")

        # Ajout stats systems
        dialogue_system = self.system_manager.get_system("DialogueSystem")
        if dialogue_system:
            cache_stats = dialogue_system.get_cache_stats()
            print(f"\nDIALOGUE SYSTEM PERFORMANCE:")
            for key, value in cache_stats.items():
                print(f"  {key}: {value}")

    def __repr__(self) -> str:
        return (f"GameSession V3.0 (running={self.running}, "
                f"turn={self.game_state.turn_count}, "
                f"location={self.current_environment.location})")
