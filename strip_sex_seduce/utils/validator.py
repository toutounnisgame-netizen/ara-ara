"""
Validator - Validation données et sécurité
"""

from typing import Any, Dict, List

class GameValidator:
    @staticmethod
    def validate_stats(volonte: int, excitation: int) -> bool:
        return (0 <= volonte <= 100) and (0 <= excitation <= 100)

    @staticmethod
    def validate_location(location: str) -> bool:
        valid_locations = {"bar", "voiture", "salon", "chambre"}
        return location in valid_locations

    @staticmethod
    def sanitize_input(user_input: str) -> str:
        # Nettoyage basique input utilisateur
        return user_input.strip()[:100]  # Max 100 chars
