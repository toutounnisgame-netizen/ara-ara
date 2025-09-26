"""
INTÉGRATION GAME_SESSION V2.0 - Méthodes escalation automatique
À intégrer dans core/game_session.py existant
"""

def _check_location_transition(self):
    """Escalation automatique OPTIMISÉE avec seuils calibrés"""

    player_summary = self.player.get_current_state_summary()
    current_loc = self.current_environment.location

    # Stats actuelles pour décision
    volonte = player_summary.get("stats", {}).get("volonte", 100)
    excitation = player_summary.get("stats", {}).get("excitation", 0)
    resistance = player_summary.get("resistance", 1.0)
    arousal = player_summary.get("arousal", 0.0)

    # ESCALATION BAR → VOITURE (seuils optimisés V2.0)
    if (current_loc == "bar" and 
        (excitation >= 30 or arousal > 0.3) and  # Seuil excitation
        volonte < 80):  # Légère perte volonté

        print("\n🚗 " + ">"*10 + " TRANSITION VOITURE " + "<"*10)
        print(f"\n{self.npc.display_name} se penche vers toi avec un sourire charmeur :")
        print("'Il fait chaud ici... Et si on allait discuter dans ma voiture ?'")
        print("'J'ai une très belle vue sur la ville depuis le parking...'")

        # Choix automatique selon résistance
        if resistance < 0.7:
            print("\nTu te surprends à hocher la tête... 'D'accord, allons-y.'")
            transition_success = True
        elif resistance < 0.9:
            print("\nTu hésites un moment, puis finis par accepter... 'Bon... juste discuter.'")
            transition_success = True
        else:
            print("\n'Je préfère rester ici...' Mais il insiste avec tant de charme...")
            transition_success = resistance < 0.95

        if transition_success:
            print("\n🚗 Vous vous dirigez vers le parking...")
            print("L'habitacle vous isole du monde, créant une bulle d'intimité.")

            self.current_environment = self.environments["voiture"]
            self.game_state.change_location("voiture")
            self._display_location_atmosphere()

    # ESCALATION VOITURE → SALON (progression naturelle)
    elif (current_loc == "voiture" and
          (excitation >= 50 or arousal > 0.5) and
          volonte < 65):

        print("\n🏠 " + ">"*10 + " TRANSITION APPARTEMENT " + "<"*10)
        print(f"\n{self.npc.display_name} caresse doucement ta main :")
        print("'Mon appartement n'est qu'à deux minutes d'ici...'")
        print("'J'aimerais te montrer ma collection d'art... et partager un excellent vin.'")

        if resistance < 0.5:
            print("\nSans réfléchir vraiment, tu acquiesces...")
            print("'J'aimerais bien voir tes œuvres d'art.'")
            transition_success = True
        elif resistance < 0.7:
            print("\nTu hésites... mais sa proposition semble innocente...")
            print("'D'accord, mais juste un verre.'")
            transition_success = True
        else:
            print("\n'Je ne sais pas... c'est peut-être trop tôt...'")
            transition_success = resistance < 0.8

        if transition_success:
            print("\n🏠 Direction son appartement...")
            print("Le salon élégant respire le raffinement et l'intimité.")

            self.current_environment = self.environments["salon"]
            self.game_state.change_location("salon")
            self._display_location_atmosphere()

    # ESCALATION SALON → CHAMBRE (transition finale)
    elif (current_loc == "salon" and
          (excitation >= 70 or arousal > 0.7) and
          volonte < 50):

        print("\n🛏️ " + ">"*10 + " TRANSITION CHAMBRE " + "<"*10)
        print("\nL'atmosphère est devenue électrique entre vous...")
        print(f"{self.npc.display_name} se lève lentement et te tend la main :")
        print("'Viens... j'aimerais te montrer quelque chose de spécial.'")

        if resistance < 0.3:
            print("\nTon cœur bat si fort... Tu prends sa main sans hésiter.")
            print("'Oui... montre-moi.'")
            transition_success = True
        elif resistance < 0.5:
            print("\nTu trembles légèrement mais tu ne peux plus reculer...")
            print("Ta main trouve la sienne presque malgré toi.")
            transition_success = True
        else:
            print("\n'Je... je ne suis pas sûre...'")
            print("Mais ses yeux te hypnotisent...")
            transition_success = resistance < 0.6

        if transition_success:
            print("\n🛏️ Il te guide vers sa chambre...")
            print("La pièce respire la sensualité et l'intimité.")

            self.current_environment = self.environments["chambre"]
            self.game_state.change_location("chambre")
            self._display_location_atmosphere()

            # Achievement transition finale
            self.game_state.unlock_achievement("reached_bedroom")

def _display_location_atmosphere(self):
    """Affichage atmosphère immersive du lieu actuel"""

    atmosphere = self.current_environment.get_random_atmosphere_description()
    print(f"\n💭 {atmosphere}")

def _process_npc_turn(self) -> Optional[Dict[str, Any]]:
    """MISE À JOUR: Traitement tour NPC avec feedback adaptation"""

    # Contexte pour IA
    context = {
        "location": self.current_environment.location,
        "privacy_level": self.current_environment.privacy_level,
        "turn_count": self.game_state.turn_count,
        "last_action": getattr(self, '_last_npc_action', None),
        "last_success": getattr(self, '_last_action_success', False)
    }

    # IA choisit action avec adaptation visible
    npc_result = self.npc.choose_next_action(
        self.player.get_resistance_level(),
        context
    )

    # Gestion retour tuple (action, message_adaptation)
    if isinstance(npc_result, tuple):
        chosen_action, adaptation_message = npc_result
    else:
        chosen_action = npc_result
        adaptation_message = None

    # Affichage message adaptation IA si présent
    adaptation_display = ""
    if adaptation_message:
        adaptation_display = f", {adaptation_message}"

    # Génération texte action
    dialogue_system = self.system_manager.get_system("DialogueSystem")
    if dialogue_system:
        description = dialogue_system.generate_npc_action_text(
            chosen_action, self.player, self.current_environment
        )
    else:
        description = f"Il {chosen_action}."

    # Application effets avec système clothing
    effects = self._apply_npc_action_effects(chosen_action)

    # NOUVELLE: Application modifications vêtements si pertinent
    clothing_result = self._apply_clothing_effects(chosen_action, effects.get("escalation_level", 1))

    # Sauvegarde pour contexte suivant
    self._last_npc_action = chosen_action
    self._last_action_success = effects.get('success', False)

    return {
        'action': chosen_action,
        'description': description,
        'effects': effects,
        'adaptation_message': adaptation_message,
        'clothing_change': clothing_result
    }

def _apply_clothing_effects(self, action: str, escalation_level: int) -> Dict[str, Any]:
    """Application effets vêtements avec système V2.0"""

    clothing_system = self.system_manager.get_system("ClothingSystem")
    if not clothing_system:
        return {"success": False}

    # Application modification vêtements
    result = clothing_system.apply_clothing_action(
        self.player,
        action,
        escalation_level,
        self.current_environment.location
    )

    # Affichage description si modification
    if result.get("success", False) and result.get("visible_change", False):
        print(f"\n👗 {result['description']}")

    return result

def _display_current_state(self):
    """MISE À JOUR: Affichage état avec vêtements si modifiés"""

    print("\n" + "-"*60)

    # Informations lieu
    print(f"📍 LIEU: {self.current_environment.display_name}")

    # Stats joueur
    player_summary = self.player.get_current_state_summary()
    stats_display = f"💪 VOLONTÉ: {player_summary['stats']['volonte']}/100  🔥 EXCITATION: {player_summary['stats']['excitation']}/100"
    print(stats_display)

    # NOUVEAU: État vêtements si modifiés
    if player_summary['exposure'] > 0 or player_summary['clothing']:
        clothing_system = self.system_manager.get_system("ClothingSystem")
        if clothing_system:
            clothing_display = clothing_system.get_clothing_display_text(self.player)
            if clothing_display:
                print(clothing_display)

    print("-"*60)

# INTÉGRATION GAME_SESSION: Escalation automatique + vêtements + atmosphere
