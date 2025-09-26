"""
ActionComponent ÉTENDU - Support parameter description (optionnel)
Extension signature pour supporter description sans breaking change
"""

def add_action(self, action: str, success_rate: float = 0.5, description: str = None):
    """
    Ajoute action avec description optionnelle

    Args:
        action: Nom de l'action
        success_rate: Taux succès (0.0-1.0)  
        description: Description optionnelle (nouveau)
    """

    # Stockage action existant
    if hasattr(self, 'actions'):
        self.actions[action] = {
            'success_rate': success_rate,
            'uses': 0,
            'last_used': 0.0,
            'description': description or f"Action {action}"  # Description optionnelle
        }
    else:
        # Fallback si pas d'attribut actions
        if not hasattr(self, '_action_data'):
            self._action_data = {}

        self._action_data[action] = {
            'success_rate': success_rate,
            'description': description or f"Action {action}"
        }

def get_action_description(self, action: str) -> str:
    """Récupère description d'une action"""

    if hasattr(self, 'actions') and action in self.actions:
        return self.actions[action].get('description', f"Action {action}")
    elif hasattr(self, '_action_data') and action in self._action_data:
        return self._action_data[action].get('description', f"Action {action}")

    return f"Action {action} inconnue."

# EXTENSION ACTIONCOMPONENT compatible backward
