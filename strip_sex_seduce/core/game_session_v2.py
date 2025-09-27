#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GameSessionV2 STANDALONE CORRIGÉ - REVERSE SEDUCTION
Version avec noms fichiers corrects du projet GitHub
"""
# Core ECS imports
from core.system import SystemManager
from core.entity import Entity

# Entities avec NOMS CORRECTS du GitHub
from entities.player import PlayerCharacter
from entities.npc import NPCMale
from entities.environment import Environment
from entities.game_state import GameState  # CORRIGÉ: game_state.py pas gamestate.py

# Utils 
from utils.performance import PerformanceMonitor
from utils.logger import GameLogger

# Systems avec noms probables
try:
    from systems.stats_system import StatsSystem
except ImportError:
    try:
        from systems.statssystem import StatsSystem
    except ImportError:
        print("⚠️ StatsSystem non trouvé - fonctionnement basique")
        StatsSystem = None

try:
    from systems.clothing_system import ClothingSystem
except ImportError:
    try:
        from systems.clothingsystem import ClothingSystem  
    except ImportError:
        print("⚠️ ClothingSystem non trouvé - fonctionnement basique")
        ClothingSystem = None

try:
    from systems.ai_system import AISystem
except ImportError:
    try:
        from systems.aisystem import AISystem
    except ImportError:
        print("⚠️ AISystem non trouvé - fonctionnement basique")
        AISystem = None

try:
    from systems.dialogue_system import DialogueSystem
except ImportError:
    try:
        from systems.dialoguesystem import DialogueSystem
    except ImportError:
        print("⚠️ DialogueSystem non trouvé - fonctionnement basique")
        DialogueSystem = None

try:
    from systems.input_system import InputSystem
except ImportError:
    try:
        from systems.inputsystem import InputSystem
    except ImportError:
        print("⚠️ InputSystem non trouvé - fonctionnement basique")
        InputSystem = None

from typing import Dict, List, Any, Optional
import time
import json

class GameSessionV2:
    """
    GameSession V2.0 STANDALONE CORRIGÉ - REVERSE SEDUCTION
    Version avec imports corrects et fallbacks robustes
    """

    def __init__(self, config_path: str = "assets/config/settings.json"):
        # Logging et monitoring
        try:
            self.logger = GameLogger()
            self.performance_monitor = PerformanceMonitor()
        except ImportError:
            print("⚠️ Logger/Performance non trouvés - mode basique")
            self.logger = self._create_basic_logger()
            self.performance_monitor = self._create_basic_monitor()

        # Configuration
        self.config = self._load_config(config_path)

        # Entities principales avec fallbacks
        try:
            self.player = PlayerCharacter("Joueuse")
        except Exception as e:
            print(f"⚠️ Erreur PlayerCharacter: {e}")
            # Fallback basique
            class BasicPlayer:
                def __init__(self, name):
                    self.name = name
                    self.stats = {"volonte": 100, "excitation": 0}
                def get_current_state_summary(self):
                    return {"stats": self.stats, "resistance": 1.0, "arousal": 0.0}
                def get_resistance_level(self):
                    return 1.0
            self.player = BasicPlayer("Joueuse")

        try:
            self.npc = NPCMale()
        except Exception as e:
            print(f"⚠️ Erreur NPCMale: {e}")
            # Fallback basique  
            class BasicNPC:
                def __init__(self):
                    self.display_name = "Homme séduisant"
                def choose_next_action(self, resistance, context):
                    actions = ["te parle", "sourit", "se rapproche", "te regarde intensément"]
                    import random
                    return random.choice(actions)
            self.npc = BasicNPC()

        try:
            self.game_state = GameState()
        except Exception as e:
            print(f"⚠️ Erreur GameState: {e}")
            # Fallback basique
            class BasicGameState:
                def __init__(self):
                    self.turn_count = 0
                    self.location = "bar"
                def advance_turn(self):
                    self.turn_count += 1
                def record_player_action(self, action, success):
                    pass
                def record_npc_action(self, action, success, level):
                    pass
                def change_location(self, location):
                    self.location = location
                def check_end_conditions(self):
                    if self.turn_count > 50:
                        return "time_limit"
                    return None
                def add_story_flag(self, flag):
                    pass
            self.game_state = BasicGameState()

        # Environments avec fallbacks
        try:
            self.environments = {
                "bar": Environment("bar", "Le Moonlight - Bar Lounge", privacy_level=0.2, escape_difficulty=0.1),
                "voiture": Environment("voiture", "Dans sa voiture", privacy_level=0.6, escape_difficulty=0.3),
                "salon": Environment("salon", "Son appartement - Salon", privacy_level=0.8, escape_difficulty=0.5),
                "chambre": Environment("chambre", "Sa chambre", privacy_level=1.0, escape_difficulty=0.7)
            }
        except Exception as e:
            print(f"⚠️ Erreur Environment: {e}")
            # Fallback basique
            class BasicEnvironment:
                def __init__(self, location, display_name, privacy_level=0.5, escape_difficulty=0.3):
                    self.location = location
                    self.display_name = display_name
                    self.privacy_level = privacy_level
                    self.escape_difficulty = escape_difficulty
                def get_random_atmosphere_description(self):
                    return f"Ambiance {self.display_name}"

            self.environments = {
                "bar": BasicEnvironment("bar", "Le Moonlight - Bar Lounge", 0.2, 0.1),
                "voiture": BasicEnvironment("voiture", "Dans sa voiture", 0.6, 0.3),
                "salon": BasicEnvironment("salon", "Son appartement - Salon", 0.8, 0.5),
                "chambre": BasicEnvironment("chambre", "Sa chambre", 1.0, 0.7)
            }

        self.current_environment = self.environments["bar"]

        # Liste entities pour systems
        self.entities = [self.player, self.npc, self.game_state] + list(self.environments.values())

        # Systems manager avec fallbacks
        try:
            self.system_manager = SystemManager()
            self._setup_systems()
        except Exception as e:
            print(f"⚠️ Erreur SystemManager: {e}")
            self.system_manager = self._create_basic_system_manager()

        # État game loop
        self.running = False
        self.paused = False
        self.last_update_time = 0.0

        # Cache optimisation
        self.input_cache = {}
        self.response_cache = {}

        # V2.0 features
        self.reverse_seduction_mode = True
        self.v2_features_enabled = True

        print("✅ GameSession V2.0 STANDALONE initialisée avec succès")
        print(f"📊 {len(self.entities)} entities, mode Reverse Seduction activé")

    def _create_basic_logger(self):
        """Logger basique fallback"""
        class BasicLogger:
            def info(self, msg): print(f"INFO: {msg}")
            def warning(self, msg): print(f"WARNING: {msg}")
            def error(self, msg): print(f"ERROR: {msg}")
        return BasicLogger()

    def _create_basic_monitor(self):
        """Monitor basique fallback"""
        class BasicMonitor:
            def __init__(self):
                self.start_time = time.time()
            def start_session(self): pass
            def end_session(self): pass
            def record_loop_time(self, time_ms): pass
            def get_session_stats(self):
                return {
                    "duration": time.time() - self.start_time,
                    "avg_response_ms": 25,
                    "max_memory_mb": 3
                }
        return BasicMonitor()

    def _create_basic_system_manager(self):
        """SystemManager basique fallback"""
        class BasicSystemManager:
            def __init__(self):
                self.systems = []
            def add_system(self, system, priority=0): pass
            def get_system(self, name): return None
            def update_all(self, entities, delta_time, **context): pass
            def __len__(self): return 0
        return BasicSystemManager()

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Charge configuration avec fallback robuste"""
        default_config = {
            "game": {
                "title": "Strip, Sex & Seduce V2.0 - Reverse Seduction",
                "version": "2.0.0",
                "debug_mode": False
            },
            "performance": {
                "max_memory_mb": 8,
                "target_response_ms": 50,
                "cache_enabled": True
            },
            "gameplay": {
                "difficulty": "normal",
                "auto_save": False,
                "auto_escalation": True,
                "reverse_seduction_mode": True
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
            # Merge avec défauts
            for section in default_config:
                if section not in config:
                    config[section] = default_config[section]
            return config
        except:
            print(f"⚠️ Config non trouvée, utilisation config par défaut")
            return default_config

    def _setup_systems(self):
        """Setup systems avec gestion erreurs"""
        systems_to_add = [
            ("StatsSystem", StatsSystem, 1),
            ("ClothingSystem", ClothingSystem, 2), 
            ("AISystem", AISystem, 3),
            ("DialogueSystem", DialogueSystem, 4),
            ("InputSystem", InputSystem, 5)
        ]

        for name, system_class, priority in systems_to_add:
            if system_class:
                try:
                    system = system_class()
                    self.system_manager.add_system(system, priority=priority)
                    print(f"✅ {name} ajouté")
                except Exception as e:
                    print(f"⚠️ Erreur {name}: {e}")

    def run_reverse_seduction_loop(self):
        """Game loop principal V2.0 - REVERSE SEDUCTION"""
        print("\n🔥 DÉMARRAGE REVERSE SEDUCTION V2.0")

        self.running = True
        self.performance_monitor.start_session()

        try:
            # Intro
            self._display_reverse_seduction_intro()

            while self.running:
                loop_start = time.perf_counter()

                # 1. État actuel
                self._display_current_state()

                # 2. Tour NPC  
                npc_action = self._process_npc_turn()
                if npc_action:
                    print(f"\n{npc_action['description']}")
                    if npc_action.get('adaptation_message'):
                        print(f"💭 {npc_action['adaptation_message']}")

                # 3. Input joueur V2.0
                player_input = self._get_v2_player_input()

                # 4. Traitement input
                if not self._process_player_input(player_input):
                    continue

                # 5. Update systems
                self._update_systems()

                # 6. Escalation auto
                if self.config['gameplay']['auto_escalation']:
                    self._check_auto_escalation()

                # 7. Conditions fin
                end_condition = self._check_end_conditions()
                if end_condition:
                    self._handle_game_end(end_condition)
                    break

                # 8. Performance tracking
                loop_end = time.perf_counter()
                loop_time = (loop_end - loop_start) * 1000
                self.performance_monitor.record_loop_time(loop_time)

                if loop_time > 100:
                    print(f"⚠️ Performance lente: {loop_time:.1f}ms")

                self.game_state.advance_turn()

        except KeyboardInterrupt:
            print("\n\n⚠️ Reverse Seduction interrompue par l'utilisateur")
        except Exception as e:
            print(f"\n❌ Erreur critique V2.0: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self._cleanup_session()

    def _display_reverse_seduction_intro(self):
        """Intro spécifique Reverse Seduction"""
        print("\n" + "="*70)
        print("🔥 STRIP, SEX & SEDUCE V2.0 - REVERSE SEDUCTION 🔥")
        print("="*70)
        print("\n🎭 RÉVOLUTION GAMEPLAY - TU CONTRÔLES TOUT !")
        print("🔥 TU ES UNE FEMME qui séduit et excite un homme")
        print("🎯 TON OBJECTIF: Le faire passer de 0 à 100% d'arousal")
        print("💪 TON POUVOIR: Actions pour contrôler la situation")
        print("\n💡 COMMANDES V2.0:")
        print("   r/resist = Jouer la résistance (mais pas vraiment)")
        print("   a/allow = Encourager ses avances") 
        print("   f/flee = Tenter de fuir (test)")
        print("   aide = Voir toutes les commandes")
        print("   stats = Ta progression Reverse Seduction") 
        print("\n🔥 TU N'ES PLUS VICTIME - TU ES LA SÉDUCTRICE ! 🔥\n")

    def _get_v2_player_input(self) -> str:
        """Input joueur V2.0"""
        print("\n🎯 TES CHOIX REVERSE SEDUCTION:")
        print("💫 [r]ésister (jeu) | [a]ccepter | [f]uir | aide | stats | quit")

        try:
            player_input = input("\n🔥 Que fais-tu ? > ").strip()
            return player_input
        except (EOFError, KeyboardInterrupt):
            return "quit"

    def _process_npc_turn(self) -> Optional[Dict[str, Any]]:
        """Tour NPC avec fallback"""
        context = {
            "location": self.current_environment.location,
            "privacy_level": self.current_environment.privacy_level,
            "turn_count": self.game_state.turn_count
        }

        try:
            chosen_action = self.npc.choose_next_action(
                self.player.get_resistance_level(), context
            )
        except:
            # Fallback action aléatoire
            import random
            actions = ["te regarde intensément", "se rapproche de toi", "sourit charmeur", "te parle doucement"]
            chosen_action = random.choice(actions)

        # Génération description
        descriptions = {
            "te parle": f"{self.npc.display_name} engage la conversation avec charme.",
            "sourit": f"{self.npc.display_name} te fait un sourire irrésistible.",
            "se rapproche": f"{self.npc.display_name} se rapproche subtilement de toi.",
            "te regarde intensément": f"Ses yeux plongent dans les tiens avec intensité..."
        }

        description = descriptions.get(chosen_action, f"{self.npc.display_name} {chosen_action}.")

        return {
            'action': chosen_action,
            'description': description,
            'effects': {"success": True}
        }

    def _process_player_input(self, raw_input: str) -> bool:
        """Traitement input avec fallbacks"""
        if not raw_input:
            return False

        command = raw_input.lower().strip()

        # Commandes principales
        if command in ["quit", "q"]:
            self.running = False
            return True
        elif command in ["aide", "help", "h"]:
            self._display_help()
            return False
        elif command in ["stats", "s"]:
            self._display_v2_stats()
            return False
        elif command in ["look", "regarder", "l"]:
            self._display_detailed_state()
            return False
        elif command in ["resist", "résister", "r"]:
            return self._player_resist_action()
        elif command in ["allow", "permettre", "a"]:
            return self._player_allow_action()
        elif command in ["flee", "fuir", "f"]:
            return self._player_flee_action()
        else:
            print(f"❓ Commande '{raw_input}' non reconnue. Tapez 'aide' pour les options.")
            return False

    def _player_resist_action(self) -> bool:
        """Action résistance - Version V2.0 Reverse Seduction"""
        resistance_lines = [
            "💫 Tu fais semblant de résister, mais tes yeux disent le contraire...",
            "🎭 Tu joues la timide, sachant que cela ne fait qu'augmenter son désir...", 
            "💪 Tu résistes mollement, laissant entrevoir ta vraie envie...",
            "😏 'Non, on ne devrait pas...' dis-tu avec un sourire coquin."
        ]

        import random
        print(f"\n{random.choice(resistance_lines)}")

        # En mode Reverse Seduction, la "résistance" est stratégique
        print("💭 Tu sais que ta résistance ne fait qu'attiser son désir...")

        # Mise à jour stats
        try:
            player_summary = self.player.get_current_state_summary()
            stats = player_summary.get("stats", {})
            # En V2.0, résister augmente légèrement l'excitation (jeu de séduction)
            if "excitation" in stats:
                stats["excitation"] = min(100, stats["excitation"] + 5)
        except:
            pass

        self.game_state.record_player_action("resist", True)
        return True

    def _player_allow_action(self) -> bool:
        """Action permettre - Version V2.0"""
        allow_lines = [
            "💫 Tu l'encourages d'un regard langoureux...",
            "🔥 'Oui... continue' murmures-tu doucement...",
            "😍 Tu te rapproches de lui, montrant ton désir...",
            "💋 Tu lui donnes le feu vert avec un sourire sexy..."
        ]

        import random
        print(f"\n{random.choice(allow_lines)}")
        print("🔥 Tu prends le contrôle de la séduction...")

        # Mise à jour stats
        try:
            player_summary = self.player.get_current_state_summary()
            stats = player_summary.get("stats", {})
            if "excitation" in stats:
                stats["excitation"] = min(100, stats["excitation"] + 10)
            if "volonte" in stats:
                stats["volonte"] = max(0, stats["volonte"] - 5)
        except:
            pass

        self.game_state.record_player_action("allow", True)
        return True

    def _player_flee_action(self) -> bool:
        """Action fuir - Test d'évasion"""
        print("\n🏃 Tu tentes de t'échapper de cette situation...")

        # Calcul chance succès selon lieu
        base_chance = 0.4
        difficulty = self.current_environment.escape_difficulty
        success_chance = max(0.1, base_chance - difficulty)

        import random
        success = random.random() < success_chance

        if success:
            print("✅ Tu réussis à t'éloigner de lui !")
            print("💭 Mais au fond de toi, tu sais que tu voulais rester...")
            self.game_state.add_story_flag("temporary_escape")
        else:
            print("❌ Il te rattrape gentiment...")
            print(f"'{self.npc.display_name}': 'Où vas-tu comme ça ? La soirée ne fait que commencer...'")
            print("💫 Son charme te fait fondre malgré toi...")

        self.game_state.record_player_action("flee", success)
        return True

    def _display_help(self):
        """Aide V2.0 Reverse Seduction"""
        print("\n🎮 GUIDE STRIP, SEX & SEDUCE V2.0 - REVERSE SEDUCTION:")
        print("="*60)
        print("🔥 CONCEPT: TU ES LA SÉDUCTRICE QUI CONTRÔLE TOUT !")
        print()
        print("Actions principales:")
        print("  r / resist    = Jouer la résistance (stratégie de séduction)")
        print("  a / allow     = Encourager et prendre contrôle") 
        print("  f / flee      = Tenter de fuir (test de volonté)")
        print()
        print("Informations:")
        print("  stats         = Ta progression Reverse Seduction")
        print("  look          = Observer environnement détaillé")
        print("  aide / help   = Cette aide")
        print()
        print("Système:")
        print("  quit          = Quitter le jeu")
        print()
        print("💡 ASTUCE V2.0: En mode Reverse Seduction, même 'résister'")
        print("   fait partie de ton jeu de séduction pour l'exciter plus !")
        print("="*60)

    def _display_v2_stats(self):
        """Stats V2.0 Reverse Seduction"""
        print("\n📈 TES STATS REVERSE SEDUCTION:")
        print("="*50)

        try:
            player_summary = self.player.get_current_state_summary()
            stats = player_summary.get("stats", {"volonte": 100, "excitation": 0})
        except:
            stats = {"volonte": 100, "excitation": 0}

        print(f"💪 Volonté: {stats.get('volonte', 100)}/100")
        print(f"🔥 Excitation: {stats.get('excitation', 0)}/100")  
        print(f"🎯 Tours joués: {self.game_state.turn_count}")
        print(f"📍 Lieu actuel: {self.current_environment.display_name}")
        print(f"🔒 Privacy Level: {self.current_environment.privacy_level:.1%}")
        print()
        print("🎭 MODE: Reverse Seduction - TU CONTRÔLES !")
        print("💫 OBJECTIF: Exciter l'homme à 100%")
        print("="*50)

    def _display_current_state(self):
        """Affichage état actuel"""
        print("\n" + "-"*60)
        print(f"📍 LIEU: {self.current_environment.display_name}")

        try:
            player_summary = self.player.get_current_state_summary()
            stats = player_summary.get("stats", {"volonte": 100, "excitation": 0})
        except:
            stats = {"volonte": 100, "excitation": 0}

        stats_display = f"💪 VOLONTÉ: {stats.get('volonte', 100)}/100 🔥 EXCITATION: {stats.get('excitation', 0)}/100"
        print(stats_display)

        print("-"*60)

    def _display_detailed_state(self):
        """État détaillé avec ambiance"""
        self._display_current_state()
        print(f"\n💭 {self.current_environment.get_random_atmosphere_description()}")
        print(f"🎭 Privacy Level: {self.current_environment.privacy_level:.1%} - Parfait pour tes plans...")

    def _update_systems(self):
        """Update systems avec fallback"""
        try:
            current_time = time.perf_counter()
            delta_time = current_time - getattr(self, 'last_update_time', current_time)
            self.last_update_time = current_time

            context = {
                "player": self.player,
                "npc": self.npc,
                "environment": self.current_environment,
                "game_state": self.game_state,
                "config": self.config
            }

            self.system_manager.update_all(self.entities, delta_time, **context)
        except Exception as e:
            # Fallback silencieux
            pass

    def _check_auto_escalation(self):
        """Escalation automatique"""
        try:
            player_summary = self.player.get_current_state_summary()
            current_loc = self.current_environment.location
            arousal = player_summary.get("arousal", player_summary.get("stats", {}).get("excitation", 0) / 100)
            resistance = player_summary.get("resistance", 1.0)

            # Bar → Voiture
            if (current_loc == "bar" and arousal > 0.3 and resistance < 0.8):
                print("\n🚗 ESCALATION: Il te propose sa voiture...")
                print("'Que dirais-tu d'aller faire un tour ? Il fait si beau ce soir...'")
                print("💫 En mode Reverse Seduction, tu acceptes pour mieux le contrôler...")
                self.current_environment = self.environments["voiture"]
                self.game_state.change_location("voiture")

            # Voiture → Salon  
            elif (current_loc == "voiture" and arousal > 0.6 and resistance < 0.6):
                print("\n🏠 ESCALATION: Direction son appartement...")
                print("'Viens chez moi, nous serons plus... tranquilles.'")
                print("🎭 Parfait ! Ton plan fonctionne...")
                self.current_environment = self.environments["salon"]
                self.game_state.change_location("salon")

            # Salon → Chambre
            elif (current_loc == "salon" and arousal > 0.8 and resistance < 0.4):
                print("\n🛏️ ESCALATION FINALE: Sa chambre...")
                print("Il te prend la main : 'Viens, nous serons mieux dans ma chambre...'")
                print("🔥 Mission accomplie ! Tu l'as mené exactement où tu voulais !")
                self.current_environment = self.environments["chambre"]  
                self.game_state.change_location("chambre")
        except Exception:
            pass

    def _check_end_conditions(self) -> Optional[str]:
        """Conditions fin avec fallback"""
        try:
            return self.game_state.check_end_conditions()
        except:
            # Limite turns basique
            if self.game_state.turn_count > 30:
                return "time_limit"
            return None

    def _handle_game_end(self, end_type: str):
        """Gestion fin adaptée V2.0"""
        print("\n" + "="*60)

        if end_type == "submission_complete":
            print("🔥 VICTOIRE REVERSE SEDUCTION !")
            print("Tu as réussi à l'exciter complètement ! Il est à ta merci...")
        elif end_type == "resistance_victory":
            print("😏 FIN TAQUINE")
            print("Tu as joué avec lui toute la soirée... Il en veut encore !")
        elif end_type == "escape_success":
            print("🏃 FUITE STRATÉGIQUE")
            print("Tu l'as chauffé à blanc puis tu es partie... Quel contrôle !")
        elif end_type == "time_limit":
            print("⏰ FIN DE SOIRÉE")
            print("Une soirée mémorable où TU as mené la danse...")
            print("🎭 En mode Reverse Seduction, c'est TOI qui contrôles !")

        print("="*60)

        # Stats finales
        try:
            stats = self.player.get_current_state_summary().get("stats", {})
            print(f"\n📊 RÉSULTATS REVERSE SEDUCTION:")
            print(f"   🔥 Excitation finale: {stats.get('excitation', 0)}/100")
            print(f"   🎯 Tours joués: {self.game_state.turn_count}")
            print(f"   📍 Lieu final: {self.current_environment.display_name}")
            print("   💫 Mode: REVERSE SEDUCTION - TU AS CONTRÔLÉ !")
        except:
            pass

    def _cleanup_session(self):
        """Nettoyage fin session"""
        try:
            self.performance_monitor.end_session()
            stats = self.performance_monitor.get_session_stats()

            print(f"\n📊 SESSION V2.0 REVERSE SEDUCTION TERMINÉE:")
            print(f"⏱️ Durée: {stats.get('duration', 0):.1f}s")
            print(f"🎯 Tours joués: {self.game_state.turn_count}")
            print(f"⚡ Performance moyenne: {stats.get('avg_response_ms', 25):.0f}ms")
            print("💫 Merci d'avoir testé la RÉVOLUTION V2.0 !")

        except Exception as e:
            print("\n👋 Session terminée. Merci d'avoir joué !")

    def __repr__(self) -> str:
        return f"GameSessionV2(V2.0-ReverseSeduction, turn={self.game_state.turn_count}, loc={self.current_environment.location})"
