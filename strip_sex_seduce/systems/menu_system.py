"""
MenuSystem V2.0 - Gestion menus contextuels et navigation
"""
from core.system import System
from core.entity import Entity
from components.action_menu import ActionMenuComponent, MenuAction
from components.stats import StatsComponent
from components.seduction import SeductionComponent
from components.progression import ProgressionComponent
from typing import List, Dict, Any, Optional
import json

class MenuSystem(System):
    """System pour gestion menus contextuels avancés"""

    def __init__(self):
        super().__init__("MenuSystem")
        self.menu_configs = {}
        self.action_catalog = {}
        self._load_menu_configurations()

    def _load_menu_configurations(self):
        """Charge configurations menus depuis assets"""
        try:
            with open("assets/config/actions_config.json", 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.action_catalog = config.get("actions", {})
                self.menu_configs = config.get("menus", {})
        except FileNotFoundError:
            # Configuration par défaut
            self.action_catalog = self._get_default_action_catalog()
            self.menu_configs = self._get_default_menu_config()

    def update(self, entities: List[Entity], delta_time: float = 0.0, **kwargs):
        """Update système menus"""
        player = kwargs.get("player")
        environment = kwargs.get("environment") 
        game_state = kwargs.get("game_state")

        if not player:
            return

        # Récupération components
        menu_comp = player.get_component_of_type(ActionMenuComponent)
        stats_comp = player.get_component_of_type(StatsComponent)
        seduction_comp = player.get_component_of_type(SeductionComponent)
        progression_comp = player.get_component_of_type(ProgressionComponent)

        if not menu_comp:
            return

        # Mise à jour actions disponibles selon contexte
        context = self._build_context(player, environment, game_state, stats_comp, seduction_comp)
        available_actions = self._generate_contextual_actions(context, progression_comp)

        menu_comp.update_available_actions(available_actions, context)

    def _build_context(self, player, environment, game_state, stats_comp, seduction_comp) -> Dict[str, Any]:
        """Construit contexte pour génération menus"""
        context = {
            "location": environment.location if environment else "bar",
            "privacy_level": getattr(environment, 'privacy_level', 0.5),
            "turn_count": getattr(game_state, 'turn_count', 0),
            "player_arousal": getattr(stats_comp, 'excitation', 0) if stats_comp else 0,
            "player_resistance": getattr(stats_comp, 'volonte', 100) if stats_comp else 100,
            "seduction_level": getattr(seduction_comp, 'seduction_level', 0) if seduction_comp else 0,
            "seduction_style": getattr(seduction_comp, 'seduction_style', 'balanced') if seduction_comp else 'balanced',
        }
        return context

    def _generate_contextual_actions(self, context: Dict[str, Any], progression_comp) -> List[str]:
        """Génère actions disponibles selon contexte"""
        available_actions = []

        # Actions de base toujours disponibles
        base_actions = ["compliment", "regard_insistant", "conversation_charme"]
        available_actions.extend(base_actions)

        # Actions selon niveau intimité/lieu
        location = context["location"]
        privacy = context["privacy_level"]

        if privacy > 0.3:  # Semi-privé
            available_actions.extend(["contact_epaule", "rapprochement_physique"])

        if privacy > 0.6:  # Privé
            available_actions.extend(["main_cuisse", "caresses_douces"])

        if privacy > 0.8:  # Très privé
            available_actions.extend(["caresses_intimes", "baiser_leger"])

        if privacy >= 1.0:  # Intimité complète
            available_actions.extend(["baiser_profond", "removal_vetement", "simulation_sexuelle"])

        # Filtre selon progression débloquée
        if progression_comp:
            unlocked_actions = progression_comp.unlocked_actions
            available_actions = [action for action in available_actions if action in unlocked_actions or action in base_actions]

        # Actions selon niveau séduction
        seduction_level = context["seduction_level"]
        if seduction_level >= 5:
            available_actions.extend(["seduction_avancee", "technique_speciale"])
        if seduction_level >= 10:
            available_actions.extend(["maitrise_totale", "multi_orgasme"])

        return list(set(available_actions))  # Remove duplicates

    def generate_menu_display(self, menu_type: str, available_actions: List[str], context: Dict[str, Any]) -> str:
        """Génère affichage menu pour console"""
        if menu_type == "main":
            return self._generate_main_menu_display(available_actions, context)
        elif menu_type == "dialogue":
            return self._generate_dialogue_menu_display(available_actions, context)
        elif menu_type == "physical":
            return self._generate_physical_menu_display(available_actions, context)
        elif menu_type == "clothing":
            return self._generate_clothing_menu_display(context)
        elif menu_type == "items":
            return self._generate_items_menu_display(context)
        else:
            return self._generate_generic_menu_display(menu_type, available_actions)

    def _generate_main_menu_display(self, available_actions: List[str], context: Dict[str, Any]) -> str:
        """Menu principal avec catégories"""
        menu_text = "\n🎯 TES ACTIONS DISPONIBLES:\n"
        menu_text += "─" * 60 + "\n"

        # Catégories dynamiques selon actions disponibles
        categories = []

        if any(action in available_actions for action in ["compliment", "conversation_charme", "flirt_direct"]):
            categories.append("1. 💬 DIALOGUE SEXY")

        if any(action in available_actions for action in ["contact_epaule", "caresses_douces", "baiser_leger"]):
            categories.append("2. 👋 ACTIONS PHYSIQUES")

        if context["privacy_level"] > 0.4:  # Vêtements uniquement si privé
            categories.append("3. 👗 VÊTEMENTS")

        if context["seduction_level"] >= 3:
            categories.append("4. 🎭 SÉDUCTION PRO")

        categories.append("5. 🍾 ITEMS")
        categories.append("6. 📍 CHANGER LIEU")
        categories.append("7. ❓ AIDE")
        categories.append("0. 🚪 QUITTER")

        # Mini-jeux si débloqués
        if context["privacy_level"] > 0.7 and context["seduction_level"] >= 5:
            menu_text += "\n🎲 MINI-JEUX SPÉCIAUX:\n"
            menu_text += "🎪 Strip-tease | 💆 Massage | 🎲 Dés désir | 🛏️ Simulation\n"

        for category in categories:
            menu_text += f"{category}\n"

        return menu_text

    def _generate_dialogue_menu_display(self, available_actions: List[str], context: Dict[str, Any]) -> str:
        """Menu dialogues sexy contextuels"""
        menu_text = "\n💬 MENU DIALOGUE - QUE LUI DIRE ?\n"
        menu_text += "═" * 50 + "\n"

        location = context["location"]
        arousal = context["player_arousal"]

        dialogue_options = []

        # Options selon lieu et niveau arousal
        if location == "bar":
            if arousal < 30:
                dialogue_options.extend([
                    '1. "Tu me plais beaucoup..." (flirt doux)',
                    '2. "J'ai chaud ici..." (excuse déshabillage)', 
                    '3. "Raconte-moi tes fantasmes..." (provocation)'
                ])
            else:
                dialogue_options.extend([
                    '1. "J'ai envie de toi..." (direct)',
                    '2. "Tu aimes mes seins ?" (exhibition)',
                    '3. "On pourrait aller ailleurs ?" (escalation)'
                ])

        elif location == "chambre":
            dialogue_options.extend([
                '1. "Prends-moi maintenant..." (invitation explicite)',
                '2. "Fais ce que tu veux de moi..." (soumission)',
                '3. "Montre-moi ta bite..." (provocation directe)',
                '4. "Baise-moi fort..." (demande explicite)'
            ])

        # Options génériques si pas spécifiques
        if not dialogue_options:
            dialogue_options.extend([
                '1. Compliment flatteur',
                '2. Question intime', 
                '3. Provocation légère',
                '4. Invitation directe'
            ])

        for option in dialogue_options:
            menu_text += f"{option}\n"

        menu_text += "\n0. ⬅️ RETOUR MENU PRINCIPAL\n"
        return menu_text

    def _generate_physical_menu_display(self, available_actions: List[str], context: Dict[str, Any]) -> str:
        """Menu actions physiques"""
        menu_text = "\n👋 MENU ACTIONS PHYSIQUES - COMMENT L'APPROCHER ?\n"
        menu_text += "═" * 55 + "\n"

        privacy = context["privacy_level"]
        physical_options = []

        if privacy <= 0.3:  # Public
            physical_options.extend([
                '1. Effleurer sa main "accidentellement"',
                '2. Se pencher pour montrer décolleté',
                '3. Croiser/décroiser jambes sensuellement',
                '4. "Trébucher" contre lui'
            ])
        elif privacy <= 0.6:  # Semi-privé
            physical_options.extend([
                '1. Poser main sur sa cuisse',
                '2. Massage spontané épaules/nuque', 
                '3. Déboutonner chemisier "il fait chaud"',
                '4. Contacts répétés corps contre corps'
            ])
        elif privacy <= 0.8:  # Privé
            physical_options.extend([
                '1. S'asseoir très près sur canapé',
                '2. Étirement sensuel provocant',
                '3. Caresses directes sur son torse',
                '4. Se déshabiller "pour être à l'aise"'
            ])
        else:  # Intimité complète
            physical_options.extend([
                '1. Strip-tease complet devant lui',
                '2. Caresses intimes directes',
                '3. Positions suggestives sur lit', 
                '4. Initiation contact sexuel direct'
            ])

        for option in physical_options:
            menu_text += f"{option}\n"

        menu_text += "\n0. ⬅️ RETOUR MENU PRINCIPAL\n"
        return menu_text

    def _generate_clothing_menu_display(self, context: Dict[str, Any]) -> str:
        """Menu vêtements interactif"""
        menu_text = "\n👗 MENU VÊTEMENTS - CONTRÔLE TON EXHIBITION\n"
        menu_text += "═" * 50 + "\n"

        # Actions vêtements contextuelles
        clothing_options = [
            '1. 👔 Déboutonner chemisier (révéler décolleté)',
            '2. 👗 Remonter jupe (montrer cuisses)',
            '3. 💄 Ajuster soutien-gorge (plus sexy)',
            '4. 👙 Jouer avec culotte (provocation)',
            '5. 🔥 Strip-tease partiel',
            '6. 🔥🔥 Déshabillage complet'
        ]

        # Options selon privacy level
        privacy = context["privacy_level"]
        if privacy < 0.5:
            clothing_options = clothing_options[:3]  # Actions discrètes seulement
        elif privacy < 0.8:
            clothing_options = clothing_options[:5]  # Pas de nudité complète

        for option in clothing_options:
            menu_text += f"{option}\n"

        menu_text += "\n💡 Plus tu es privée, plus d'options disponibles !\n"
        menu_text += "0. ⬅️ RETOUR MENU PRINCIPAL\n"
        return menu_text

    def _generate_items_menu_display(self, context: Dict[str, Any]) -> str:
        """Menu items érotiques"""
        menu_text = "\n🍾 MENU ITEMS - QUE VEUX-TU UTILISER ?\n"
        menu_text += "═" * 45 + "\n"

        item_options = [
            '1. 🍾 Champagne (ambiance + désinhibition)',
            '2. 🍫 Chocolat aphrodisiaque (+libido)',
            '3. 📱 Téléphone (photos/vidéos)',
            '4. 🎵 Musique (ambiance séduction)',
            '5. 💡 Éclairage tamisé (intimité)'
        ]

        # Items avancés selon privacy et arousal
        if context["privacy_level"] > 0.7 and context["player_arousal"] > 50:
            item_options.extend([
                '6. 🔮 Vibrator (démonstration désir)',
                '7. 🛡️ Préservatifs (préparation sexe)',
                '8. ⛓️ Menottes (jeu BDSM léger)'
            ])

        for option in item_options:
            menu_text += f"{option}\n"

        menu_text += "\n0. ⬅️ RETOUR MENU PRINCIPAL\n"
        return menu_text

    def _generate_generic_menu_display(self, menu_type: str, available_actions: List[str]) -> str:
        """Menu générique pour autres types"""
        menu_text = f"\n📋 MENU {menu_type.upper()}\n"
        menu_text += "═" * 30 + "\n"

        for i, action in enumerate(available_actions[:8], 1):  # Max 8 options
            action_name = action.replace("_", " ").title()
            menu_text += f"{i}. {action_name}\n"

        menu_text += "\n0. ⬅️ RETOUR MENU PRINCIPAL\n"
        return menu_text

    def handle_menu_selection(self, menu_comp: ActionMenuComponent, selection: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Traite sélection menu utilisateur"""
        current_menu = menu_comp.menu_state

        # Navigation menus
        if selection == "0" or selection.lower() in ["retour", "back"]:
            previous_menu = menu_comp.go_back()
            return {
                "action_type": "navigation", 
                "new_menu": previous_menu,
                "message": f"Retour au menu {previous_menu}"
            }

        # Sélections menu principal
        if current_menu == "main":
            return self._handle_main_menu_selection(menu_comp, selection)
        elif current_menu == "dialogue":
            return self._handle_dialogue_selection(menu_comp, selection, context)
        elif current_menu == "physical":
            return self._handle_physical_selection(menu_comp, selection, context)
        elif current_menu == "clothing":
            return self._handle_clothing_selection(menu_comp, selection, context)
        elif current_menu == "items":
            return self._handle_items_selection(menu_comp, selection, context)

        return {"action_type": "invalid", "message": "Sélection non reconnue"}

    def _handle_main_menu_selection(self, menu_comp: ActionMenuComponent, selection: str) -> Dict[str, Any]:
        """Gère sélections menu principal"""
        menu_mappings = {
            "1": "dialogue",
            "2": "physical", 
            "3": "clothing",
            "4": "seduction",
            "5": "items",
            "6": "location",
            "7": "aide"
        }

        if selection in menu_mappings:
            new_menu = menu_mappings[selection]
            menu_comp.set_menu_state(new_menu)
            return {
                "action_type": "navigation",
                "new_menu": new_menu,
                "message": f"Menu {new_menu} ouvert"
            }

        return {"action_type": "invalid", "message": "Choix non valide"}

    def _handle_dialogue_selection(self, menu_comp: ActionMenuComponent, selection: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Gère sélections dialogue"""
        dialogue_actions = {
            "1": "dialogue_flirt",
            "2": "dialogue_provocation",
            "3": "dialogue_invitation",
            "4": "dialogue_direct"
        }

        if selection in dialogue_actions:
            action_id = dialogue_actions[selection]
            menu_comp.record_action_selection(action_id, context)
            return {
                "action_type": "dialogue",
                "action_id": action_id,
                "message": f"Action dialogue: {action_id}"
            }

        return {"action_type": "invalid", "message": "Option dialogue non valide"}

    def _handle_physical_selection(self, menu_comp: ActionMenuComponent, selection: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Gère sélections actions physiques"""
        privacy = context["privacy_level"]

        if privacy <= 0.3:  # Public
            physical_actions = {"1": "contact_discret", "2": "exhibition_decollete", "3": "jeu_jambes", "4": "contact_accidentel"}
        elif privacy <= 0.6:  # Semi-privé
            physical_actions = {"1": "caresse_cuisse", "2": "massage_epaules", "3": "exhibition_moderee", "4": "contact_corps"}
        elif privacy <= 0.8:  # Privé
            physical_actions = {"1": "proximite_canapé", "2": "étirement_sensuel", "3": "caresse_directe", "4": "deshabillage_partiel"}
        else:  # Intimité complète
            physical_actions = {"1": "strip_tease_complet", "2": "caresse_intime", "3": "position_suggestive", "4": "initiation_sexuelle"}

        if selection in physical_actions:
            action_id = physical_actions[selection]
            menu_comp.record_action_selection(action_id, context)
            return {
                "action_type": "physical",
                "action_id": action_id,
                "privacy_level": privacy,
                "message": f"Action physique: {action_id}"
            }

        return {"action_type": "invalid", "message": "Action physique non valide"}

    def _handle_clothing_selection(self, menu_comp: ActionMenuComponent, selection: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Gère sélections vêtements"""
        clothing_actions = {
            "1": "deboutonner_chemisier",
            "2": "remonter_jupe", 
            "3": "ajuster_soutien_gorge",
            "4": "jouer_culotte",
            "5": "strip_tease_partiel",
            "6": "deshabillage_complet"
        }

        if selection in clothing_actions:
            action_id = clothing_actions[selection]
            menu_comp.record_action_selection(action_id, context)
            return {
                "action_type": "clothing",
                "action_id": action_id,
                "message": f"Action vêtement: {action_id}"
            }

        return {"action_type": "invalid", "message": "Action vêtement non valide"}

    def _handle_items_selection(self, menu_comp: ActionMenuComponent, selection: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Gère sélections items"""
        item_actions = {
            "1": "use_champagne",
            "2": "use_chocolat",
            "3": "use_telephone", 
            "4": "use_musique",
            "5": "use_eclairage",
            "6": "use_vibrator",
            "7": "use_preservatifs", 
            "8": "use_menottes"
        }

        if selection in item_actions:
            action_id = item_actions[selection]
            menu_comp.record_action_selection(action_id, context)
            return {
                "action_type": "item_usage",
                "action_id": action_id,
                "message": f"Utilisation item: {action_id}"
            }

        return {"action_type": "invalid", "message": "Item non valide"}

    def _get_default_action_catalog(self) -> Dict[str, Any]:
        """Catalogue actions par défaut"""
        return {
            "dialogue_flirt": {
                "name": "Flirt charmeur",
                "category": "dialogue",
                "energy_cost": 2,
                "arousal_impact": 5
            },
            "contact_discret": {
                "name": "Contact discret", 
                "category": "physical",
                "energy_cost": 3,
                "arousal_impact": 8
            }
            # ... autres actions
        }

    def _get_default_menu_config(self) -> Dict[str, Any]:
        """Configuration menus par défaut"""
        return {
            "main": {
                "title": "Menu Principal",
                "categories": ["dialogue", "physical", "clothing", "items"]
            }
            # ... autres configs
        }

    def get_menu_analytics(self) -> Dict[str, Any]:
        """Analytics utilisation menus"""
        return {
            "system_name": self.name,
            "catalogs_loaded": len(self.action_catalog),
            "menus_configured": len(self.menu_configs)
        }
