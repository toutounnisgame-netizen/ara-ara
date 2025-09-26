"""
CORRECTIF ClothingComponent V2.0 - Ajouts méthodes manquantes
Méthodes complémentaires pour ClothingSystem
"""

def reset_to_initial_state(self):
    """Remet tous les vêtements à leur état initial"""

    for piece_name in self.pieces:
        self.pieces[piece_name]["state"] = "normale"
        self.pieces[piece_name]["last_modified"] = 0

    # Reset stats dérivées
    self.exposure_level = 0
    self.modification_history.clear()
    self.overall_description = self._generate_overall_description()

    self.mark_dirty()

def get_pieces_by_state(self, state: str) -> List[str]:
    """Retourne pièces dans un état donné"""

    return [piece for piece, data in self.pieces.items() 
            if data["state"] == state]

def get_most_exposed_pieces(self, limit: int = 3) -> List[Dict[str, Any]]:
    """Retourne pièces les plus modifiées/exposées"""

    # Tri par niveau modification (approximatif)
    exposure_scores = {
        "normale": 0,
        "legerement_deplacee": 1,
        "glissee": 1,
        "plis_froissee": 2,
        "remontee": 3,
        "retroussee": 3,
        "entrouverte": 4,
        "boutonne_partiellement": 4,
        "largement_ouverte": 6,
        "descendue_epaules": 5,
        "retiree": 8,
        "tombee": 7,
        "défait": 9,
        "complètement_ouverte": 8,
        "mise_de_cote": 9
    }

    pieces_with_scores = []
    for piece, data in self.pieces.items():
        score = exposure_scores.get(data["state"], 0)
        if score > 0:  # Seulement pièces modifiées
            pieces_with_scores.append({
                "piece": piece,
                "state": data["state"],
                "score": score,
                "last_modified": data["last_modified"]
            })

    # Tri par score décroissant
    pieces_with_scores.sort(key=lambda x: x["score"], reverse=True)

    return pieces_with_scores[:limit]

def _update_derived_stats(self):
    """Met à jour statistiques dérivées (exposition, etc.)"""

    # Calcul exposition selon pièces modifiées
    total_exposure = 0

    exposure_weights = {
        "robe": 25,           # Pièce majeure
        "chemisier": 20,      # Pièce importante
        "jupe": 15,           # Pièce moyenne
        "pantalon": 15,
        "soutien_gorge": 30,  # Pièce intime majeure
        "culotte": 35,        # Pièce intime maximale
        "bas": 5,             # Pièce mineure
        "chaussures": 2,      # Pièce très mineure
        "veste": 8,           # Pièce extérieure
        "bretelles_robe": 5   # Détail
    }

    state_multipliers = {
        "normale": 0,
        "legerement_deplacee": 0.2,
        "glissee": 0.3,
        "plis_froissee": 0.1,
        "remontee": 0.6,
        "retroussee": 0.7,
        "entrouverte": 0.5,
        "boutonne_partiellement": 0.4,
        "largement_ouverte": 0.8,
        "descendue_epaules": 0.6,
        "retiree": 1.0,       # Maximum
        "tombee": 0.9,
        "défait": 1.0,        # Maximum
        "complètement_ouverte": 0.9,
        "mise_de_cote": 0.95
    }

    for piece, data in self.pieces.items():
        piece_weight = exposure_weights.get(piece, 10)  # Default weight
        state_mult = state_multipliers.get(data["state"], 0)

        piece_contribution = piece_weight * state_mult
        total_exposure += piece_contribution

    # Normalisation approximative sur 100
    self.exposure_level = min(100, int(total_exposure))

    # Regénération description
    self.overall_description = self._generate_overall_description()

# CORRECTIFS CLOTHING COMPONENT pour compatibilité système V2.0
