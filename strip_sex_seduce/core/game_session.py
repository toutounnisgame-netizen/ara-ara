"""
GameSession - Orchestrateur principal du jeu ECS
Game loop central qui coordonne tous les systems et entities
"""

from core.system import SystemManager
from core.entity import Entity
from entities.player import PlayerCharacter
from entities.npc import NPCMale
from entities.environment import Environment
from entities.game_state import GameState
from utils.performance import PerformanceMonitor
from utils.logger import GameLogger

# Import systems (seront implémentés après)
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
    Classe principale orchestrant le jeu ECS
    Responsable du game loop et coordination des systems
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

        # Environments disponibles
        self.environments = {
            "bar": Environment("bar"),
            "voiture": Environment("voiture"),
            "salon": Environment("salon"),
            "chambre": Environment("chambre")
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
        self.logger.info(f"GameSession initialisée avec {len(self.entities)} entities")
        self.logger.info(f"Systems actifs: {len(self.system_manager)}")

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Charge la configuration depuis JSON"""
        default_config = {
            "game": {
                "title": "Strip, Sex & Seduce",
                "version": "1.0.0",
                "debug_mode": False
            },
            "performance": {
                "max_memory_mb": 5,
                "target_response_ms": 50,
                "cache_enabled": True
            },
            "gameplay": {
                "difficulty": "normal",
                "auto_save": False
            },
            "interface": {
                "show_stats": True,
                "show_help_hints": True
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
        """Configure tous les systems avec priorités"""

        # System de stats (priorité haute - doit s'exécuter en premier)
        stats_system = StatsSystem()
        self.system_manager.add_system(stats_system, priority=1)

        # System de vêtements (dépend des stats)
        clothing_system = ClothingSystem()
        self.system_manager.add_system(clothing_system, priority=2)

        # System IA (analyse l'état pour décider actions)
        ai_system = AISystem()
        self.system_manager.add_system(ai_system, priority=3)

        # System dialogues (génère textes selon état)
        dialogue_system = DialogueSystem()
        self.system_manager.add_system(dialogue_system, priority=4)

        # System input (traite les entrées utilisateur)
        input_system = InputSystem()
        self.system_manager.add_system(input_system, priority=5)

        self.logger.info("Systems configurés avec priorités")

    def run_game_loop(self):
        """Lance le game loop principal"""
        self.logger.info("Démarrage game loop principal")
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
                    print(f"\n{npc_action['description']}")

                # 3. Input joueur
                player_input = self._get_player_input()

                # 4. Traitement input
                if not self._process_player_input(player_input):
                    continue  # Input invalide, recommencer

                # 5. Update de tous les systems
                self._update_systems()

                # 6. Check conditions de fin
                end_condition = self._check_end_conditions()
                if end_condition:
                    self._handle_game_end(end_condition)
                    break

                # 7. Nettoyage et optimisations
                self._cleanup_turn()

                # 8. Performance tracking
                loop_end = time.perf_counter()
                loop_time = (loop_end - loop_start) * 1000  # ms
                self.performance_monitor.record_loop_time(loop_time)

                # Check performance critique
                if loop_time > self.config["performance"]["target_response_ms"]:
                    self.logger.warning(f"Performance dégradée: {loop_time:.1f}ms")

                self.game_state.advance_turn()

        except KeyboardInterrupt:
            self.logger.info("Jeu interrompu par l'utilisateur")
            print("\n\n⚠️  Jeu interrompu...")

        except Exception as e:
            self.logger.error(f"Erreur critique game loop: {e}")
            print(f"\n❌ Erreur critique: {e}")

        finally:
            self._cleanup_session()

    def _display_game_intro(self):
        """Affiche l'introduction du jeu"""
        print("\n" + "="*60)
        print(f"🔥 {self.config['game']['title'].upper()} 🔥")
        print("="*60)
        print("\nVous êtes dans un bar élégant. Un homme charmant s'approche de vous...")
        print("💡 Tapez 'aide' à tout moment pour voir les commandes")
        print()

    def _display_current_state(self):
        """Affiche l'état actuel du jeu"""
        print("\n" + "-"*60)

        # Informations lieu
        print(f"📍 LIEU: {self.current_environment.display_name}")

        # Stats joueur
        player_summary = self.player.get_current_state_summary()
        print(f"💪 VOLONTÉ: {player_summary['stats']['volonte']}/100  "
              f"🔥 EXCITATION: {player_summary['stats']['excitation']}/100")

        # État vêtements si modifié
        if player_summary['exposure'] > 0:
            clothing_desc = " | ".join(player_summary['clothing'])
            print(f"👗 TENUE: {clothing_desc}")

        # Informations debug si activées
        if self.config['game']['debug_mode']:
            npc_state = self.npc.get_behavioral_state()
            print(f"🤖 DEBUG NPC: {npc_state['current_strategy']} "
                  f"(taux succès: {npc_state['success_rate']:.0%})")

        print("-"*60)

    def _process_npc_turn(self) -> Optional[Dict[str, Any]]:
        """Traite le tour du NPC avec IA adaptative"""

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

        # Récupération système dialogue pour génération texte
        dialogue_system = self.system_manager.get_system("DialogueSystem")
        if dialogue_system:
            description = dialogue_system.generate_npc_action_text(
                chosen_action,
                self.player,
                self.current_environment
            )
        else:
            description = f"Il {chosen_action}."

        # Application des effets
        effects = self._apply_npc_action_effects(chosen_action)

        # Sauvegarde pour contexte suivant
        self._last_npc_action = chosen_action
        self._last_action_success = effects.get('success', False)

        return {
            'action': chosen_action,
            'description': description,
            'effects': effects
        }

    def _apply_npc_action_effects(self, action: str) -> Dict[str, Any]:
        """Applique les effets d'une action NPC"""

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
        """
        Traite l'input joueur

        Returns:
            True si input valide et traité
        """
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
        """Gère les commandes joueur"""

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
        """Traite une action de résistance du joueur"""

        # Récupération système stats
        stats_system = self.system_manager.get_system("StatsSystem")
        if not stats_system:
            return False

        # Tentative résistance
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
        """Traite une tentative de fuite"""

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

    def _display_help(self):
        """Affiche l'aide complète"""
        print("""
╔══════════════════════════════════════════════════════════╗
║                    🆘 AIDE - COMMANDES                    ║
╠══════════════════════════════════════════════════════════╣
║ ACTIONS PRINCIPALES:                                     ║
║ • r, résister    → Résister à l'action NPC              ║
║ • a, permettre   → Laisser faire l'action               ║
║ • f, fuir        → Tenter de quitter la situation       ║
║                                                          ║
║ INFORMATIONS:                                            ║
║ • regarder       → Observer l'environnement             ║
║ • stats          → Voir statistiques détaillées         ║
║ • aide           → Afficher cette aide                  ║
║                                                          ║
║ SYSTÈME:                                                 ║
║ • quit           → Quitter le jeu                       ║
║                                                          ║
║ STATS AFFICHÉES:                                        ║
║ • Volonté: Votre résistance (plus haut = plus difficile)║
║ • Excitation: Votre niveau d'arousal                    ║
║ • Tenue: État de vos vêtements si modifiés             ║
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
        """Gère la fin de partie"""

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

        print("="*60)

        # Affichage statistiques finales
        self._display_final_statistics()

    def _display_final_statistics(self):
        """Affiche les statistiques finales"""
        session_summary = self.game_state.get_session_summary()

        print("\n📊 STATISTIQUES FINALES:")
        print("-"*40)
        print(f"⏱️  Durée: {session_summary['session_info']['duration_seconds']//60:.0f} min")
        print(f"🎮 Tours joués: {session_summary['session_info']['turns']}")
        print(f"📍 Lieux visités: {session_summary['progression']['locations_visited']}/4")
        print(f"🏆 Achievements: {session_summary['achievements']['unlocked']}/{session_summary['achievements']['total']}")

        # Performance
        perf_stats = self.performance_monitor.get_session_stats()
        print(f"💾 Mémoire max: {perf_stats.get('max_memory_mb', 0):.1f} MB")
        print(f"⚡ Temps moyen: {perf_stats.get('avg_response_ms', 0):.0f} ms")

    def _cleanup_turn(self):
        """Nettoyage fin de tour"""

        # Limite cache input pour mémoire
        if len(self._input_cache) > 50:
            # Garde seulement les 30 plus récents
            items = list(self._input_cache.items())
            self._input_cache = dict(items[-30:])

        # Check transition lieu automatique
        self._check_location_transition()

    def _check_location_transition(self):
        """Vérifie si transition automatique de lieu"""

        player_summary = self.player.get_current_state_summary()

        # Transition bar -> voiture si excitation suffisante
        if (self.current_environment.location == "bar" and 
            player_summary["arousal"] > 0.4):
            print("\n🚗 >>> Il te propose de continuer dans sa voiture...")
            self.current_environment = self.environments["voiture"]
            self.game_state.change_location("voiture")

        # Transition voiture -> salon
        elif (self.current_environment.location == "voiture" and
              player_summary["arousal"] > 0.7):
            print("\n🏠 >>> Il t'emmène à son appartement...")
            self.current_environment = self.environments["salon"]
            self.game_state.change_location("salon")

        # Transition salon -> chambre
        elif (self.current_environment.location == "salon" and
              player_summary["resistance"] < 0.4):
            print("\n🛏️ >>> Il te guide vers sa chambre...")
            self.current_environment = self.environments["chambre"]
            self.game_state.change_location("chambre")

    def _cleanup_session(self):
        """Nettoyage fin de session"""

        try:
            # Statistiques finales monitoring
            self.performance_monitor.end_session()

            # Log session summary
            summary = self.game_state.get_session_summary()
            self.logger.info(f"Session terminée: {summary}")

        except Exception as e:
            self.logger.error(f"Erreur cleanup session: {e}")

        print("\n👋 Merci d'avoir joué!")

    # Méthodes debug et développement
    def _display_detailed_state(self):
        """Affiche état détaillé pour debug"""
        if not self.config['game']['debug_mode']:
            print("Mode debug non activé")
            return

        print("\n🔍 ÉTAT DÉTAILLÉ:")
        print(f"Player: {self.player}")
        print(f"NPC: {self.npc}")
        print(f"Environment: {self.current_environment}")
        print(f"Game State: {self.game_state}")

    def _display_detailed_stats(self):
        """Affiche statistiques détaillées"""
        summary = self.game_state.get_session_summary()
        print("\n📈 STATISTIQUES DÉTAILLÉES:")

        for section, data in summary.items():
            print(f"\n{section.upper()}:")
            if isinstance(data, dict):
                for key, value in data.items():
                    print(f"  {key}: {value}")
            else:
                print(f"  {data}")

    def __repr__(self) -> str:
        return (f"GameSession(running={self.running}, "
                f"turn={self.game_state.turn_count}, "
                f"location={self.current_environment.location})")
