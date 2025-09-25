"""
CORRECTIF GAME_SESSION.PY V2.0 - Partie escalation automatique
Ajout méthodes pour progression lieux fluide + transitions immersives
"""

def _check_location_transition(self):
    """Escalation automatique AMÉLIORÉE avec seuils optimisés"""

    player_summary = self.player.get_current_state_summary()
    current_loc = self.current_environment.location

    # Récupération stats actuelles pour décision
    volonte = player_summary.get("stats", {}).get("volonte", 100)
    excitation = player_summary.get("stats", {}).get("excitation", 0)
    resistance = player_summary.get("resistance", 1.0)
    arousal = player_summary.get("arousal", 0.0)

    # ESCALATION BAR → VOITURE (seuils optimisés)
    if (current_loc == "bar" and 
        (excitation >= 25 or arousal > 0.25) and  # Seuil plus bas
        volonte < 85):  # Un peu de volonté perdue

        print("\n🚗 " + ">"*10 + " TRANSITION VOITURE " + "<"*10)
        print(f"\n{self.npc.display_name} se penche vers toi avec un sourire charmeur :")
        print("'Il fait chaud ici... Et si on allait discuter dans ma voiture ?'")
        print("'J'ai une très belle vue sur la ville depuis le parking...'")

        # Choix joueur pour immersion
        print("\n💭 Comment réagis-tu ?")
        print("1. Accepter de le suivre")
        print("2. Hésiter mais céder")  
        print("3. Refuser poliment")

        # Simulation choix selon stats (automatique pour fluidité)
        if resistance < 0.7:  # Faible résistance = acceptation
            print("\nTu te surprends à hocher la tête... 'D'accord, allons-y.'")
            transition_success = True
        elif resistance < 0.9:  # Résistance moyenne = hésitation puis cession
            print("\nTu hésites un moment, puis finis par accepter... 'Bon... juste discuter.'")
            transition_success = True
        else:  # Forte résistance = refus mais insistance
            print("\n'Je préfère rester ici...' Mais il insiste avec tant de charme...")
            transition_success = resistance < 0.95  # Chance minime

        if transition_success:
            print("\n🚗 Vous vous dirigez vers le parking...")
            print("Il t'ouvre galamment la portière passager.")
            print("L'habitacle sent bon le cuir et son parfum masculin.")

            self.current_environment = self.environments["voiture"]
            self.game_state.change_location("voiture")

            # Bonus immersion
            print("\nDans l'intimité relative de la voiture, l'atmosphère change...")

        else:
            print("\nTu réussis à décliner son invitation pour l'instant.")

    # ESCALATION VOITURE → SALON (progression naturelle)
    elif (current_loc == "voiture" and
          (excitation >= 45 or arousal > 0.45) and
          volonte < 70):

        print("\n🏠 " + ">"*10 + " TRANSITION APPARTEMENT " + "<"*10)
        print(f"\n{self.npc.display_name} caresse doucement ta main :")
        print("'Mon appartement n'est qu'à deux minutes d'ici...'")
        print("'J'ai une très belle collection d'art que j'aimerais te montrer.'")
        print("'Et un excellent vin que nous pourrions partager...'")

        # Résolution selon résistance
        if resistance < 0.5:
            print("\nSans réfléchir vraiment, tu acquiesces...")
            print("'J'aimerais bien voir tes œuvres d'art.'")
            transition_success = True
        elif resistance < 0.7:
            print("\nTu hésites... Une partie de toi sait que c'est risqué...")
            print("Mais sa proposition semble innocente... 'D'accord, mais juste un verre.'")
            transition_success = True
        else:
            print("\n'Je ne sais pas... c'est peut-être trop tôt...'")
            print("Il sourit avec compréhension mais continue ses caresses...")
            transition_success = resistance < 0.8

        if transition_success:
            print("\n🏠 Direction son appartement...")
            print("L'ascenseur semble durer une éternité, vos regards se croisent...")
            print("Il t'ouvre la porte sur un salon élégamment décoré.")

            self.current_environment = self.environments["salon"]
            self.game_state.change_location("salon")

            print("\n'Fais comme chez toi', dit-il en préparant deux verres...")

    # ESCALATION SALON → CHAMBRE (transition intime)
    elif (current_loc == "salon" and
          (excitation >= 65 or arousal > 0.65) and  
          volonte < 50):

        print("\n🛏️ " + ">"*10 + " TRANSITION CHAMBRE " + "<"*10)
        print("\nL'atmosphère est devenue électrique entre vous...")
        print(f"{self.npc.display_name} se lève lentement et te tend la main :")
        print("'Viens... j'aimerais te montrer quelque chose de spécial.'")
        print("Son regard intense ne laisse aucun doute sur ses intentions...")

        # Résolution finale selon résistance critique
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
            print("Mais il s'approche, ses lèvres près de tes cheveux :")
            print("'Tu n'as rien à craindre avec moi...'")
            transition_success = resistance < 0.6  # Dernière chance résistance

        if transition_success:
            print("\n🛏️ Il te guide vers sa chambre...")
            print("La pièce est tamisée, un grand lit domine l'espace...")
            print("Tu réalises que vous avez franchi un point de non-retour...")

            self.current_environment = self.environments["chambre"]
            self.game_state.change_location("chambre")

            # Achievement transition finale
            self.game_state.unlock_achievement("reached_bedroom")

        else:
            print("\nTu trouves la force de reculer... 'Pas encore...'")
            print("Il respecte ta décision mais tu vois la déception dans ses yeux.")

def _display_location_atmosphere(self):
    """Affiche ambiance immersive du lieu actuel"""

    location = self.current_environment.location

    atmosphere_descriptions = {
        "bar": [
            "🍸 L'ambiance du bar est feutrée, la musique jazz crée une atmosphère intime.",
            "Des couples discutent à voix basse aux tables environnantes.",
            "L'éclairage tamisé danse sur vos visages."
        ],
        "voiture": [
            "🚗 Dans l'habitacle, vous êtes isolés du monde extérieur.", 
            "Les sièges en cuir sentent bon, l'espace confiné augmente la proximité.",
            "Par la vitre teintée, les lumières de la ville défilent lentement."
        ],
        "salon": [
            "🏠 Le salon élégant respire le raffinement et l'intimité.",
            "Des bougies projettent des ombres dansantes sur les murs.",
            "Le canapé moelleux vous invite à vous rapprocher l'un de l'autre."
        ],
        "chambre": [
            "🛏️ Dans la chambre, l'atmosphère est chargée de possibilités...",
            "Le grand lit domine la pièce, éclairé par une lumière douce.",
            "Ici, tous les masques tombent, seuls vos désirs comptent."
        ]
    }

    descriptions = atmosphere_descriptions.get(location, ["Vous êtes dans un lieu indéterminé."])

    print("\n" + "~" * 50)
    for desc in descriptions:
        print(desc)
    print("~" * 50)

def _handle_escalation_resistance(self, resistance_level: float) -> Dict[str, Any]:
    """Gestion résistance joueur aux transitions avec feedback"""

    if resistance_level > 0.8:
        messages = [
            "Tu sens que tu perds le contrôle de la situation...",
            "Une partie de toi veut résister, mais c'est de plus en plus difficile...",
            "Tu essaies de garder tes distances, mais il est si persuasif..."
        ]
        outcome = "high_resistance"

    elif resistance_level > 0.5:
        messages = [
            "Tu es partagée entre envie et appréhension...",
            "Ton corps et ta raison se livrent un combat intérieur...",
            "Tu te surprends à céder petit à petit à ses avances..."
        ]
        outcome = "moderate_resistance"

    else:
        messages = [
            "Tu ne peux plus nier l'attraction que tu ressens...",
            "Tes dernières inhibitions s'envolent progressivement...",
            "Tu t'abandonnes à ses caresses expertes..."
        ]
        outcome = "low_resistance"

    import random
    chosen_message = random.choice(messages)
    print(f"\n💭 {chosen_message}")

    return {"outcome": outcome, "message": chosen_message}

# MÉTHODES À AJOUTER à GameSession pour escalation fluide
