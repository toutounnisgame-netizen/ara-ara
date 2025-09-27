#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GameSessionV2 - REVERSE SEDUCTION ÉDITION RÉVOLUTIONNAIRE
Point d'entrée principal pour la V2.0 avec tous les nouveaux systems
Hérite de GameSession existant et ajoute fonctionnalités V2.0
"""
from systems.menu_system import MenuSystem
from systems.inventory_system import InventorySystem
from systems.seduction_system import SeductionSystem
from systems.progression_system import ProgressionSystem
from systems.minigame_system import MiniGameSystem
from components.inventory import InventoryComponent
from components.action_menu import ActionMenuComponent
from components.seduction import SeductionComponent
from components.progression import ProgressionComponent
from typing import Dict, Any, Optional
import time

class GameSessionV2(GameSession):
    """
    GameSession V2.0 - REVERSE SEDUCTION
    Extension de GameSession avec nouveaux systems révolutionnaires
    """

    def __init__(self, config_path: str = "assets/config/settings.json"):
        # Initialisation classe parente
        super().__init__(config_path)

        # Ajout des nouveaux systems V2.0
        self._setup_v2_systems()

        # Ajout des nouveaux components aux entities
        self._setup_v2_components()

        # État V2.0
        self.reverse_seduction_mode = True
        self.active_minigame_session = None
        self.v2_features_enabled = True

        self.logger.info("GameSessionV2 initialisée - Mode Reverse Seduction activé")

    def _setup_v2_systems(self):
        """Configuration des nouveaux systems V2.0"""
        try:
            # MenuSystem - Gestion menus contextuels révolutionnaire  
            menu_system = MenuSystem()
            self.system_manager.add_system(menu_system, priority=10)

            # InventorySystem - Items érotiques et effets
            inventory_system = InventorySystem()
            self.system_manager.add_system(inventory_system, priority=11)

            # SeductionSystem - Mécaniques séduction avancées
            seduction_system = SeductionSystem()  
            self.system_manager.add_system(seduction_system, priority=12)

            # ProgressionSystem - Unlocks et achievements
            progression_system = ProgressionSystem()
            self.system_manager.add_system(progression_system, priority=13)

            # MiniGameSystem - 4 mini-jeux intégrés
            minigame_system = MiniGameSystem()
            self.system_manager.add_system(minigame_system, priority=14)

            self.logger.info("Systems V2.0 configurés avec succès")

        except Exception as e:
            self.logger.error(f"Erreur setup V2 systems: {e}")
            # Fallback vers systems de base si échec
            self.v2_features_enabled = False

    def _setup_v2_components(self):
        """Ajout des nouveaux components V2.0 aux entities"""
        try:
            # Player - Ajout components V2.0
            if not self.player.has_component(InventoryComponent):
                inventory_comp = InventoryComponent()
                # Items de démarrage
                inventory_comp.add_item("champagne", 1)
                inventory_comp.available_items.add("champagne")
                self.player.add_component(inventory_comp)

            if not self.player.has_component(ActionMenuComponent):
                menu_comp = ActionMenuComponent()
                self.player.add_component(menu_comp)

            if not self.player.has_component(SeductionComponent):
                seduction_comp = SeductionComponent()
                self.player.add_component(seduction_comp)

            if not self.player.has_component(ProgressionComponent):
                progression_comp = ProgressionComponent()
                # Actions de base débloquées
                progression_comp.unlock_action("dialogue_flirt", "starting_actions")
                progression_comp.unlock_action("contact_discret", "starting_actions") 
                progression_comp.unlock_action("deboutonner_chemisier", "starting_actions")
                self.player.add_component(progression_comp)

            self.logger.info("Components V2.0 ajoutés avec succès")

        except Exception as e:
            self.logger.error(f"Erreur setup V2 components: {e}")

    def run_reverse_seduction_loop(self):
        """Game loop principal V2.0 - REVERSE SEDUCTION"""
        self.logger.info("Démarrage Game Loop V2.0 - Reverse Seduction")

        if not self.v2_features_enabled:
            self.logger.warning("Features V2.0 désactivées, fallback vers GameSession classique")
            return self.run_game_loop()  # Fallback

        self.running = True
        self.performance_monitor.start_session()

        try:
            # Intro spécifique V2.0
            self._display_reverse_seduction_intro()

            while self.running:
                loop_start = time.perf_counter()

                # 1. Affichage état V2.0 enrichi
                self._display_v2_state()

                # 2. Gestion menus contextuels V2.0
                if self._handle_v2_menus():
                    continue

                # 3. Tour NPC (hérité)
                npc_action = self._process_npc_turn()
                if npc_action:
                    print(f"\n{npc_action['description']}")
                    if npc_action.get('adaptation_message'):
                        print(f"💭 {npc_action['adaptation_message']}")

                # 4. Input joueur V2.0
                player_input = self._get_v2_player_input()

                # 5. Traitement input V2.0
                if not self._process_v2_input(player_input):
                    continue

                # 6. Update systems V2.0
                self._update_systems()

                # 7. Check escalation (hérité mais amélioré)
                if self.config['gameplay']['auto_escalation']:
                    self._check_auto_escalation()

                # 8. Check conditions fin
                end_condition = self._check_end_conditions()
                if end_condition:
                    self._handle_game_end(end_condition)
                    break

                # 9. Performance tracking V2.0
                loop_end = time.perf_counter()
                loop_time = (loop_end - loop_start) * 1000
                self.performance_monitor.record_loop_time(loop_time)

                if loop_time > 100:  # Warning si >100ms
                    self.logger.warning(f"Loop V2.0 lent: {loop_time:.1f}ms")

                self.game_state.advance_turn()

        except KeyboardInterrupt:
            self.logger.info("Game Loop V2.0 interrompu par utilisateur")
            print("\n\n⚠️ Reverse Seduction interrompue...")
        except Exception as e:
            self.logger.error(f"Erreur critique Game Loop V2.0: {e}")
            print(f"\n❌ Erreur V2.0: {e}")
        finally:
            self._cleanup_session()

    def _display_reverse_seduction_intro(self):
        """Intro spécifique Reverse Seduction"""
        print("\n" + "="*70)
        print("🔥 BIENVENUE DANS LA RÉVOLUTION REVERSE SEDUCTION 🔥")  
        print("="*70)
        print("\n🎭 TU ES LA SÉDUCTRICE - TU CONTRÔLES TOUT !")
        print("🎯 TON OBJECTIF: Exciter cet homme de 0 à 100%")
        print("💫 TON POUVOIR: 50+ actions contextuelles disponibles")
        print("🎪 TES ARMES: Dialogue, physique, vêtements, items, mini-jeux")
        print("\n💡 RAPPEL: Tu peux taper un numéro pour choisir une action")
        print("   ou 'aide' pour voir toutes les commandes disponibles")
        print("\n🔥 Que la séduction commence ! 🔥\n")

    def _display_v2_state(self):
        """Affichage état V2.0 enrichi"""
        # Affichage de base (hérité)
        self._display_current_state()

        # Enrichissements V2.0
        progression_comp = self.player.get_component_of_type(ProgressionComponent)
        if progression_comp:
            progress = progression_comp.get_progression_summary()
            print(f"🏆 PROGRESSION: Niveau {progress['seduction_level']} | "
                  f"Points {progress['progression_points']} | "
                  f"Actions {progress['unlocked_actions']}/50+")

    def _handle_v2_menus(self) -> bool:
        """Gestion menus contextuels V2.0"""
        menu_system = self.system_manager.get_system("MenuSystem")
        if not menu_system:
            return False

        menu_comp = self.player.get_component_of_type(ActionMenuComponent)
        if not menu_comp or menu_comp.menu_state == "main":
            # Affichage menu principal V2.0
            available_actions = menu_system._generate_contextual_actions(
                self._build_v2_context(), 
                self.player.get_component_of_type(ProgressionComponent)
            )

            if available_actions:
                menu_display = menu_system.generate_menu_display(
                    "main", available_actions, self._build_v2_context()
                )
                print(menu_display)

        return False  # Continue le loop normalement

    def _get_v2_player_input(self) -> str:
        """Input joueur V2.0 avec hints"""
        print("\n🎯 TON CHOIX:")
        print("💬 1-9 = Action | 'aide' = Commandes | 'stats' = Progression")

        try:
            player_input = input("\n🔥 > ").strip()
            return player_input
        except (EOFError, KeyboardInterrupt):
            return "quit"

    def _process_v2_input(self, raw_input: str) -> bool:
        """Traitement input V2.0 avec nouveaux systems"""
        if not raw_input:
            return False

        # Gestion numérique pour menus
        if raw_input.isdigit():
            return self._handle_numeric_menu_selection(int(raw_input))

        # Commandes spéciales V2.0
        if raw_input.lower() in ["stats", "progression"]:
            self._display_v2_progression()
            return False
        elif raw_input.lower() in ["minijeu", "minigame"]:
            return self._handle_minigame_request()
        elif raw_input.lower() in ["items", "inventory"]:
            self._display_inventory()
            return False

        # Fallback vers traitement classique
        return self._process_player_input(raw_input)

    def _handle_numeric_menu_selection(self, choice: int) -> bool:
        """Gestion sélection numérique dans menus"""
        menu_system = self.system_manager.get_system("MenuSystem")
        if not menu_system:
            print("❌ System menu non disponible")
            return False

        # Simulation action selon choix
        actions_map = {
            1: "dialogue_flirt",
            2: "contact_discret", 
            3: "deboutonner_chemisier",
            4: "caresse_cuisse",
            5: "use_champagne",
            6: "strip_tease_partiel",
            7: "baiser_leger",
            8: "minigame_strip_tease",
            9: "simulation_sexuelle"
        }

        if choice in actions_map:
            action_id = actions_map[choice]
            result = self._execute_v2_action(action_id)
            if result:
                print(f"\n✨ {result['description']}")
                return True
        else:
            print(f"❓ Choix {choice} non reconnu")

        return False

    def _execute_v2_action(self, action_id: str) -> Optional[Dict[str, Any]]:
        """Exécution action V2.0 avec nouveaux systems"""
        seduction_system = self.system_manager.get_system("SeductionSystem")
        if not seduction_system:
            return None

        # Simulation action pour démonstration
        action_descriptions = {
            "dialogue_flirt": "Tu lui lances un regard enjôleur : 'Tu me plais beaucoup...'",
            "contact_discret": "Tu effleures sa main 'accidentellement', il frissonne...",
            "deboutonner_chemisier": "Tu déboutonnes lentement ton chemisier, il ne peut détacher ses yeux...",
            "caresse_cuisse": "Ta main se pose sur sa cuisse, il déglutit difficilement...",
            "use_champagne": "Vous trinquez, vos regards se croisent intensément...",
            "strip_tease_partiel": "Tu commences un strip-tease langoureux qui le rend fou...",
            "baiser_leger": "Tu l'embrasses tendrement, il gémit de plaisir...",
            "minigame_strip_tease": "🎪 Tu lances le mini-jeu strip-tease !",
            "simulation_sexuelle": "🔥 Vous faites l'amour avec une passion dévorante..."
        }

        return {
            "action": action_id,
            "description": action_descriptions.get(action_id, f"Tu exécutes l'action {action_id}"),
            "success": True
        }

    def _display_v2_progression(self):
        """Affichage progression V2.0 détaillée"""
        progression_comp = self.player.get_component_of_type(ProgressionComponent)
        if not progression_comp:
            print("❌ Système progression non disponible")
            return

        summary = progression_comp.get_progression_summary()

        print("\n" + "="*60)
        print("📈 PROGRESSION REVERSE SEDUCTION")
        print("="*60)
        print(f"🎭 Niveau Séduction: {summary.get('seduction_level', 0)}/10")
        print(f"🏆 Points Progression: {summary.get('progression_points', 0)}")
        print(f"🔓 Actions Débloquées: {summary.get('unlocked_actions', 0)}/50+")
        print(f"📍 Lieux Accessibles: {summary.get('unlocked_locations', 1)}/4")
        print(f"🏅 Achievements: {summary.get('achievements_earned', 0)}/8")
        print("="*60)

    def _handle_minigame_request(self) -> bool:
        """Gestion demande mini-jeu"""
        minigame_system = self.system_manager.get_system("MiniGameSystem")
        if not minigame_system:
            print("❌ Mini-jeux non disponibles")
            return False

        available_games = minigame_system.get_available_minigames(
            self.player, self._build_v2_context()
        )

        if not available_games:
            print("❌ Aucun mini-jeu disponible dans ce contexte")
            return False

        print("\n🎪 MINI-JEUX DISPONIBLES:")
        for i, game in enumerate(available_games, 1):
            print(f"{i}. {game['name']} - {game['description']}")

        return False

    def _display_inventory(self):
        """Affichage inventory V2.0"""
        inventory_comp = self.player.get_component_of_type(InventoryComponent)
        if not inventory_comp:
            print("❌ Inventory non disponible")
            return

        print("\n🍾 TON INVENTORY:")
        print("-" * 30)
        if inventory_comp.items:
            for item_id, quantity in inventory_comp.items.items():
                print(f"• {item_id}: {quantity}")
        else:
            print("Inventory vide")
        print("-" * 30)

    def _build_v2_context(self) -> Dict[str, Any]:
        """Construction contexte V2.0 enrichi"""
        context = {
            "location": self.current_environment.location if self.current_environment else "bar",
            "privacy_level": getattr(self.current_environment, 'privacy_level', 0.5),
            "turn_count": getattr(self.game_state, 'turn_count', 0),
            "reverse_seduction_mode": True,
            "v2_features": True
        }

        # Ajout stats depuis components
        stats_comp = self.player.get_component_of_type("StatsComponent")
        if stats_comp:
            context.update({
                "player_arousal": getattr(stats_comp, 'excitation', 0),
                "player_resistance": getattr(stats_comp, 'volonte', 100)
            })

        return context

    def get_v2_features_status(self) -> Dict[str, Any]:
        """Status features V2.0 pour debug"""
        return {
            "v2_enabled": self.v2_features_enabled,
            "reverse_seduction_mode": self.reverse_seduction_mode,
            "systems_count": len(self.system_manager),
            "active_minigame": self.active_minigame_session is not None,
            "player_components": len(self.player.components) if hasattr(self.player, 'components') else 0
        }
