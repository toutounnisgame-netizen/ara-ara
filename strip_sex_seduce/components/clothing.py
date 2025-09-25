"""
ClothingComponent - Gestion détaillée vêtements avec historique
Système complexe sans memory leaks pour gameplay immersif
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from core.component import Component

@dataclass
class ClothingComponent(Component):
    """
    Component gérant l'état détaillé des vêtements
    Chaque pièce a des propriétés spécifiques et un historique
    """

    # Configuration détaillée par pièce de vêtement
    pieces: Dict[str, Dict[str, Any]] = field(default_factory=lambda: {
        "chemisier": {
            "status": "boutonne",        # boutonne/deboutonne/retire
            "buttons_open": 0,           # Nombre boutons ouverts (0-6)
            "visibility": "normal",      # normal/partial/exposed
            "access": "blocked",         # blocked/limited/open
            "fabric_state": "intact",    # intact/froisse/dechire
            "history": []                # Historique modifications
        },
        "jupe": {
            "status": "en_place",        # en_place/releve/retire
            "position": "normale",       # normale/remontee/baisse
            "length": "genou",           # genou/cuisse/mini
            "access": "limited",         # limited/partial/full
            "zipper_state": "ferme",     # ferme/ouvert/coince
            "history": []
        },
        "soutien_gorge": {
            "status": "attache",         # attache/detache/retire
            "visibility": "cache",       # cache/visible/expose
            "support": "full",           # full/partial/none
            "clasp_state": "ferme",      # ferme/ouvert
            "cups_position": "place",    # place/deplace/retire
            "history": []
        },
        "culotte": {
            "status": "en_place",        # en_place/descend/retire
            "visibility": "cache",       # cache/apercu/visible
            "position": "normale",       # normale/baisse/cheville
            "access": "blocked",         # blocked/partial/open
            "side_state": "place",       # place/tire/dechire
            "history": []
        }
    })

    # État général
    initial_outfit: str = "conservatrice"  # conservatrice/suggestive/provocante
    total_exposure: int = 0                # Niveau exposition global (0-100)
    disheveled_state: int = 0              # Niveau désordre général (0-100)

    # Métadonnées
    modification_count: int = 0            # Nombre total modifications
    last_modified: str = ""                # Dernière pièce modifiée
    modification_speed: float = 1.0        # Vitesse modifications (NPC trait)

    def __post_init__(self):
        """Initialisation après création"""
        super().__init__()
        self._update_derived_stats()

    def modify_piece(self, piece: str, property: str, value: Any, 
                    source: str = "unknown") -> bool:
        """
        Modifie une propriété d'une pièce avec historique
        Memory-safe avec nettoyage automatique historique

        Args:
            piece: Nom de la pièce (chemisier, jupe, etc.)
            property: Propriété à modifier
            value: Nouvelle valeur
            source: Source de la modification

        Returns:
            True si modification réussie
        """
        if piece not in self.pieces:
            return False

        piece_data = self.pieces[piece]
        old_value = piece_data.get(property)

        # Application modification
        piece_data[property] = value

        # Ajout à l'historique avec limite pour éviter memory leaks
        history_entry = {
            "property": property,
            "old_value": old_value,
            "new_value": value,
            "source": source,
            "modification_index": self.modification_count
        }

        piece_data["history"].append(history_entry)

        # Nettoyage historique si trop volumineux (memory management)
        if len(piece_data["history"]) > 20:  # Limite à 20 entrées
            piece_data["history"] = piece_data["history"][-15:]  # Garde les 15 plus récentes

        # Mise à jour métadonnées
        self.modification_count += 1
        self.last_modified = piece

        # Recalcul stats dérivées
        self._update_derived_stats()
        self.mark_dirty()

        return True

    def get_exposure_level(self) -> int:
        """
        Calcule le niveau d'exposition global (0-100)
        Algorithme équilibré pour gameplay immersif
        """
        exposure = 0

        # Chemisier contribution
        chemisier = self.pieces["chemisier"]
        if chemisier["status"] == "deboutonne":
            exposure += min(20, chemisier["buttons_open"] * 4)
        elif chemisier["status"] == "retire":
            exposure += 40

        # Jupe contribution
        jupe = self.pieces["jupe"]
        if jupe["position"] == "remontee":
            exposure += 25
        elif jupe["status"] == "retire":
            exposure += 35

        # Sous-vêtements contribution
        soutien_gorge = self.pieces["soutien_gorge"]
        if soutien_gorge["visibility"] == "visible":
            exposure += 20
        elif soutien_gorge["status"] == "retire":
            exposure += 30

        culotte = self.pieces["culotte"]
        if culotte["visibility"] == "apercu":
            exposure += 15
        elif culotte["visibility"] == "visible":
            exposure += 30
        elif culotte["status"] == "retire":
            exposure += 40

        return min(100, exposure)

    def get_access_level(self, target_area: str) -> str:
        """
        Évalue le niveau d'accès à une zone spécifique

        Args:
            target_area: "chest", "legs", "intimate"

        Returns:
            "blocked", "limited", "partial", "open"
        """
        if target_area == "chest":
            chemisier_access = self.pieces["chemisier"]["access"]
            soutien_gorge_access = self.pieces["soutien_gorge"].get("access", "blocked")

            # Logique combinée
            if chemisier_access == "blocked":
                return "blocked"
            elif chemisier_access == "limited" and soutien_gorge_access == "blocked":
                return "limited"
            elif chemisier_access == "open" and soutien_gorge_access == "blocked":
                return "partial"
            else:
                return "open"

        elif target_area == "legs":
            return self.pieces["jupe"]["access"]

        elif target_area == "intimate":
            jupe_access = self.pieces["jupe"]["access"]
            culotte_access = self.pieces["culotte"]["access"]

            if jupe_access == "limited" or culotte_access == "blocked":
                return "blocked"
            elif jupe_access == "partial" and culotte_access == "limited":
                return "limited"
            elif jupe_access == "full" and culotte_access == "partial":
                return "partial"
            else:
                return "open"

        return "blocked"

    def get_disheveled_level(self) -> int:
        """Calcule le niveau de désordre général (0-100)"""
        disheveled = 0

        for piece_name, piece_data in self.pieces.items():
            # Chaque modification ajoute au désordre
            if piece_data["status"] != "en_place" and piece_data["status"] != "boutonne":
                disheveled += 15

            # État du tissu
            if piece_data.get("fabric_state") == "froisse":
                disheveled += 10
            elif piece_data.get("fabric_state") == "dechire":
                disheveled += 25

        return min(100, disheveled)

    def _update_derived_stats(self):
        """Met à jour les statistiques dérivées"""
        self.total_exposure = self.get_exposure_level()
        self.disheveled_state = self.get_disheveled_level()

    def get_piece_description(self, piece: str) -> str:
        """Génère une description textuelle de l'état d'une pièce"""
        if piece not in self.pieces:
            return f"{piece}: état inconnu"

        piece_data = self.pieces[piece]
        status = piece_data["status"]

        descriptions = {
            "chemisier": {
                "boutonne": "chemisier correctement boutonné",
                "deboutonne": f"chemisier déboutonné ({piece_data.get('buttons_open', 0)} boutons)",
                "retire": "chemisier retiré"
            },
            "jupe": {
                "en_place": "jupe en place",
                "releve": "jupe relevée",
                "retire": "jupe retirée"
            },
            "soutien_gorge": {
                "attache": "soutien-gorge attaché",
                "detache": "soutien-gorge détaché",
                "retire": "soutien-gorge retiré"
            },
            "culotte": {
                "en_place": "culotte en place",
                "descend": "culotte descendue",
                "retire": "culotte retirée"
            }
        }

        return descriptions.get(piece, {}).get(status, f"{piece}: {status}")

    def get_overall_description(self) -> List[str]:
        """Retourne une description générale de la tenue"""
        descriptions = []

        for piece in ["chemisier", "jupe", "soutien_gorge", "culotte"]:
            piece_desc = self.get_piece_description(piece)
            if "en place" not in piece_desc and "boutonné" not in piece_desc:
                descriptions.append(piece_desc)

        if not descriptions:
            descriptions.append("tenue intacte")

        return descriptions

    def reset_to_initial(self):
        """Remet tous les vêtements à leur état initial"""
        for piece_name, piece_data in self.pieces.items():
            if piece_name == "chemisier":
                piece_data.update({
                    "status": "boutonne",
                    "buttons_open": 0,
                    "visibility": "normal",
                    "access": "blocked"
                })
            else:
                piece_data["status"] = "en_place"
                if "position" in piece_data:
                    piece_data["position"] = "normale"
                if "access" in piece_data:
                    piece_data["access"] = "blocked" if piece_name == "culotte" else "limited"

        self._update_derived_stats()
        self.mark_dirty()

    def to_dict(self) -> Dict[str, Any]:
        """Sérialisation complète du component"""
        base_dict = super().to_dict()

        # Sérialisation sans historique complet pour performance
        pieces_summary = {}
        for piece_name, piece_data in self.pieces.items():
            pieces_summary[piece_name] = {
                k: v for k, v in piece_data.items() 
                if k != "history"  # Exclut historique détaillé
            }
            pieces_summary[piece_name]["history_count"] = len(piece_data["history"])

        base_dict.update({
            "pieces": pieces_summary,
            "total_exposure": self.total_exposure,
            "disheveled_state": self.disheveled_state,
            "modification_count": self.modification_count,
            "last_modified": self.last_modified,
            "overall_description": self.get_overall_description()
        })

        return base_dict

    def __repr__(self) -> str:
        return f"ClothingComponent(exposure:{self.total_exposure}%, modifications:{self.modification_count})"
