"""
CORRECTIF GAME_SESSION.PY - Compatibilité signatures V2.0
Résolution erreurs signatures méthodes dans game loop
"""

def _player_resist_action(self) -> bool:
    """Traite une action de résistance du joueur - SIGNATURE CORRIGÉE"""

    # Récupération système stats
    stats_system = self.system_manager.get_system("StatsSystem")
    if not stats_system:
        return False

    # SIGNATURE CORRIGÉE V2.0: (player, resistance_type, context)
    resistance_result = stats_system.apply_player_resistance(
        self.player,
        "soft_resistance",  # resistance_type en string
        {                   # context en Dict séparé
            "location": self.current_environment.location,
            "privacy": self.current_environment.privacy_level
        }
    )

    if resistance_result.get("success", False):
        print("Tu essaies de résister doucement à ses avances...")
        if resistance_result.get("message"):
            print(resistance_result["message"])

        # Indication gain volonté si présent
        if "volonte_gained" in resistance_result or resistance_result.get("visible_change", False):
            print("💪 Tu te sens un peu plus forte.")
    else:
        print("Tu n'arrives plus à résister efficacement...")
        if resistance_result.get("message"):
            print(resistance_result["message"])

    # Enregistrement analytics
    self.game_state.record_player_action(
        "resist", 
        resistance_result.get("success", False),
        resistance_result.get("stats_before", {}),
        resistance_result.get("stats_after", {})
    )

    return True

def _handle_player_command(self, command: str) -> bool:
    """Gère les commandes joueur - SIGNATURES CORRIGÉES"""

    if command in ["aide", "help"]:
        self._display_help()
        return False  # Pas de tour consommé

    elif command in ["resist", "résister", "r"]:
        return self._player_resist_action()

    elif command in ["allow", "permettre", "a"]:
        return self._player_allow_action()

    elif command in ["flee", "fuir", "f"]:
        return self._player_flee_action()

    elif command in ["look", "regarder", "l"]:
        self._display_detailed_state()
        return False  # Pas de tour consommé

    elif command == "stats":
        self._display_detailed_stats()
        return False

    elif command == "quit":
        self.running = False
        return True

    return False

def _process_npc_turn(self) -> Optional[Dict[str, Any]]:
    """Traite le tour du NPC avec IA adaptative - SIGNATURES CORRIGÉES"""

    # Contexte pour IA
    context = {
        "location": self.current_environment.location,
        "privacy_level": self.current_environment.privacy_level,
        "turn_count": self.game_state.turn_count,
        "last_action": getattr(self, '_last_npc_action', None),
        "last_success": getattr(self, '_last_action_success', False)
    }

    # IA choisit action - GESTION NOUVELLE SIGNATURE
    npc_choice = self.npc.choose_next_action(
        self.player.get_resistance_level(),
        context
    )

    # GESTION RETOUR tuple ou string
    if isinstance(npc_choice, tuple):
        chosen_action, adaptation_message = npc_choice
    else:
        chosen_action = npc_choice
        adaptation_message = None

    # Affichage message adaptation IA si présent
    if adaptation_message:
        print(f"\n🤖 {adaptation_message}")

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
        'effects': effects,
        'adaptation_message': adaptation_message
    }

def _handle_player_choice(self, choice: str) -> bool:
    """Gère les choix joueur typés - NOUVEAU"""

    if choice in ["resist", "résister", "r"]:
        return self._player_resist_action()
    elif choice in ["allow", "permettre", "a"]:
        return self._player_allow_action()
    elif choice in ["flee", "fuir", "f"]:
        return self._player_flee_action()

    return False

# CORRECTIFS SIGNATURES GAME_SESSION pour compatibilité V2.0 complète
