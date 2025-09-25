"""
DialogueSystem V2.0 - Cache Ultra Performance <10ms
Génération dialogues contextuels avec cache pré-calculé
"""

from core.system import System
from core.entity import Entity
from typing import List, Dict, Any, Optional
import json
import random
import time

class DialogueSystem(System):
    """System dialogues avec cache ultra-performance <10ms garanti"""

    def __init__(self):
        super().__init__("DialogueSystem")

        # CACHE PERFORMANCE CRITIQUE
        self._dialogue_cache = {}
        self._cache_hits = 0
        self._cache_misses = 0
        self._generation_times = []

        # DIALOGUE BASE TEMPLATES - PRÉ-CALCULÉ
        self._base_templates = {
            "compliment": {
                "bar": [
                    "Il te sourit chaleureusement : 'Tu as un regard vraiment captivant...'",
                    "'Tu es magnifique ce soir', murmure-t-il en se rapprochant.",
                    "Il lève son verre vers toi : 'À la plus belle femme de ce bar.'"
                ],
                "voiture": [
                    "Dans l'intimité de la voiture : 'J'adore ta façon de sourire.'",
                    "'Tu sens divinement bon', dit-il en ajustant le rétroviseur.",
                    "Sa main effleure la tienne : 'Tu me troubles vraiment...'"
                ],
                "salon": [
                    "Dans son salon, il te contemple : 'Tu es encore plus belle à la lumière douce.'",
                    "'Cette ambiance te va à merveille', dit-il en s'approchant.",
                    "Il caresse doucement ta joue : 'Parfaite...'"
                ],
                "chambre": [
                    "Dans l'intimité de la chambre : 'Tu es absolument désirable...'",
                    "Il trace le contour de ton visage : 'Magnifique...'",
                    "'Je n'arrive plus à te résister', souffle-t-il."
                ]
            },
            "conversation_charme": {
                "bar": [
                    "Il se penche vers ton oreille : 'Raconte-moi tes secrets...'",
                    "'Tu as l'air mystérieuse... j'aimerais te découvrir.'",
                    "Sa voix devient plus grave : 'Qu'est-ce qui te fait vibrer ?'"
                ],
                "voiture": [
                    "En conduisant, il te lance des regards : 'Tu me distrais dangereusement...'",
                    "'J'adore ton rire', dit-il en caressant le volant.",
                    "Il pose sa main libre près de la tienne : 'Dis-moi ce qui te plaît...'"
                ],
                "salon": [
                    "Sur le canapé, il se rapproche : 'J'aimerais mieux te connaître...'",
                    "'Tu as une énergie magnétique', murmure-t-il à ton oreille.",
                    "Il joue avec une mèche de tes cheveux : 'Fascinante...'"
                ],
                "chambre": [
                    "Il s'assoit près de toi : 'Raconte-moi tes fantasmes...'",
                    "'Tu es exactement comme je t'imaginais', souffle-t-il.",
                    "Ses doigts tracent des cercles sur ta main : 'Parfaite intimité...'"
                ]
            },
            "regard_insistant": {
                "bar": [
                    "Son regard s'attarde sur tes lèvres de façon troublante.",
                    "Il te fixe intensément, un sourire énigmatique aux lèvres.",
                    "Ses yeux ne te quittent pas, créant une tension palpable."
                ],
                "voiture": [
                    "Dans le rétroviseur, son regard croise le tien longuement.",
                    "À chaque feu rouge, il tourne vers toi un regard brûlant.",
                    "Ses yeux parcourent ton corps avec une intensité troublante."
                ],
                "salon": [
                    "Il te dévore du regard depuis l'autre bout du canapé.",
                    "Son regard intense te met mal à l'aise et t'excite à la fois.",
                    "Il observe chacun de tes mouvements avec fascination."
                ],
                "chambre": [
                    "Son regard ardent ne quitte plus tes formes.",
                    "Il te contemple avec un désir non dissimulé.",
                    "Ses yeux brûlants parcourent ton corps lentement."
                ]
            },
            "contact_epaule": {
                "bar": [
                    "Sa main se pose 'innocemment' sur ton épaule en parlant.",
                    "Il effleure ton épaule en passant derrière toi.",
                    "Un contact prolongé de sa main sur ton épaule nue."
                ],
                "voiture": [
                    "En changeant de vitesse, sa main frôle ton épaule.",
                    "Il ajuste ton siège et sa main s'attarde sur ton épaule.",
                    "Un massage 'amical' de tes épaules tendues."
                ],
                "salon": [
                    "Il pose son bras sur le dossier, touchant tes épaules.",
                    "En te montrant quelque chose, il caresse ton épaule.",
                    "Sa main glisse de ton épaule vers ton dos."
                ],
                "chambre": [
                    "Il masse tendrement tes épaules dénudées.",
                    "Ses mains expertes pétrissent tes épaules tendues.",
                    "Un toucher possessif sur tes épaules frémissantes."
                ]
            }
        }

        # PRÉ-CALCUL CACHE INITIAL
        self._precompute_cache()

    def _precompute_cache(self):
        """Pré-calcule les dialogues les plus courants pour cache ultra-rapide"""

        common_actions = ["compliment", "conversation_charme", "regard_insistant", "contact_epaule"]
        locations = ["bar", "voiture", "salon", "chambre"]

        for action in common_actions:
            for location in locations:
                cache_key = f"{action}_{location}_standard"
                if action in self._base_templates and location in self._base_templates[action]:
                    templates = self._base_templates[action][location]
                    self._dialogue_cache[cache_key] = random.choice(templates)

        print(f"💾 Cache pré-calculé: {len(self._dialogue_cache)} dialogues")

    def generate_npc_action_text(self, action: str, player: Entity, 
                                environment: Entity, context: Dict = None) -> str:
        """
        Génération ultra-rapide <10ms avec cache intelligent
        """
        start_time = time.perf_counter()

        # CACHE KEY CONSTRUCTION
        location = environment.location if hasattr(environment, 'location') else 'bar'

        # Tentative cache ultra-rapide
        cache_key = f"{action}_{location}_standard"

        if cache_key in self._dialogue_cache:
            self._cache_hits += 1
            result = self._dialogue_cache[cache_key]
        else:
            # Génération rapide fallback
            self._cache_misses += 1
            result = self._generate_fallback_text(action, location)

            # Cache pour prochaines fois
            self._dialogue_cache[cache_key] = result

        # Performance tracking
        end_time = time.perf_counter()
        generation_time = (end_time - start_time) * 1000  # ms
        self._generation_times.append(generation_time)

        # Garde seulement les 20 derniers temps pour moyenne
        if len(self._generation_times) > 20:
            self._generation_times = self._generation_times[-10:]

        return result

    def _generate_fallback_text(self, action: str, location: str) -> str:
        """Génération fallback rapide si pas en cache"""

        # Templates de base par action
        fallback_templates = {
            "compliment": f"Il te fait un compliment dans ce {location}.",
            "conversation_charme": f"Il engage une conversation charmeuse.",
            "regard_insistant": f"Il te regarde intensément.",
            "contact_epaule": f"Il touche ton épaule délicatement.",
            "rapprochement_physique": f"Il se rapproche de toi.",
            "main_cuisse": f"Sa main effleure ta cuisse.",
            "caresses_douces": f"Il te caresse tendrement."
        }

        return fallback_templates.get(action, f"Il {action} avec toi.")

    def get_performance_stats(self) -> Dict[str, Any]:
        """Stats performance pour monitoring"""

        avg_time = sum(self._generation_times) / len(self._generation_times) if self._generation_times else 0
        max_time = max(self._generation_times) if self._generation_times else 0

        cache_rate = self._cache_hits / max(1, self._cache_hits + self._cache_misses)

        return {
            "avg_generation_ms": round(avg_time, 2),
            "max_generation_ms": round(max_time, 2),
            "cache_hit_rate": round(cache_rate * 100, 1),
            "cache_size": len(self._dialogue_cache),
            "total_generations": self._cache_hits + self._cache_misses
        }

    def update(self, entities: List[Entity], delta_time: float = 0.0, **kwargs):
        """Update system - maintenance cache si nécessaire"""

        # Pas d'update critique nécessaire pour performance
        pass

# DIALOGUE SYSTEM V2.0: Performance <10ms + cache intelligent + fallbacks
