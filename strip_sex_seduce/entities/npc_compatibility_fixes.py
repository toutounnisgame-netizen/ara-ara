"""
NPC.PY - Correctif compatibilité méthodes manquantes
Ajout méthodes de base pour éviter crashes
"""

def choose_next_action(self, player_resistance: float, 
                      context: Dict[str, Any]) -> str:
    """
    Choix action NPC basique compatible

    Args:
        player_resistance: Niveau résistance 0.0-1.0
        context: Contexte environnement

    Returns:
        str: Action choisie
    """

    # Adaptation actions selon résistance - logique basique
    if player_resistance > 0.7:
        # Résistance forte - actions douces
        actions = ["compliment", "conversation_charme", "regard_insistant"]
    elif player_resistance > 0.4:
        # Résistance modérée - escalation légère
        actions = ["contact_epaule", "rapprochement_physique"]
    elif player_resistance > 0.2:
        # Faible résistance - escalation modérée
        actions = ["main_cuisse", "caresses_douces"]
    else:
        # Très faible résistance - escalation forte
        actions = ["baiser_leger", "caresses"]

    # Modification selon lieu
    location = context.get("location", "bar")
    if location == "bar" and player_resistance < 0.5:
        # En public, limitation escalation
        actions = ["compliment", "conversation_charme", "contact_epaule"]

    # Sélection finale aléatoire pondérée
    import random
    return random.choice(actions)

def get_behavioral_state(self) -> Dict[str, Any]:
    """État comportemental basique pour compatibilité"""

    return {
        "name": getattr(self, 'display_name', 'Marcus'),
        "personality_type": getattr(self, 'personality_type', 'mixed'),
        "interaction_count": getattr(self, 'interaction_count', 0),
        "success_rate": 0.5,
        "current_escalation": 2,
        "recent_actions": [],
        "adaptations_made": 0,
        "current_strategy": "normal",
        "escalation_rate": 1.0,
        "dominant_traits": ["adaptability", "charm"]
    }

@property
def display_name(self) -> str:
    """Nom d'affichage du NPC"""
    return getattr(self, '_display_name', 'Marcus')

@display_name.setter  
def display_name(self, value: str):
    """Setter nom d'affichage"""
    self._display_name = value

# CORRECTIFS NPC BASIQUES pour éviter AttributeError
