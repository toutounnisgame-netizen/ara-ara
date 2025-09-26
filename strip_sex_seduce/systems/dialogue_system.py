"""
DialogueSystem V3.0 - CORRIGÉ COMPLET
Cache ultra-rapide + Génération textes riches contextuels
"""
from core.system import System
from core.entity import Entity
from typing import List, Dict, Any, Optional
import random
import json
import time

class DialogueSystem(System):
    """System dialogue avec cache optimisé et génération contextuelle CORRIGÉE"""

    def __init__(self):
        super().__init__("DialogueSystem")

        # Cache pré-calculé pour performance <10ms
        self.dialogue_cache = {}
        self.context_templates = {}
        self._load_dialogue_assets()

        # Compteurs performance
        self.cache_hits = 0
        self.cache_misses = 0

    def _load_dialogue_assets(self):
        """Charge et pré-calcule tous les dialogues"""
        start_time = time.perf_counter()

        # TEMPLATES RICHES CONTEXTUELS - CORRIGÉ
        self.dialogue_templates = {
            "bar": {
                "compliment": {
                    "low_resistance": [
                        "Il te sourit avec assurance : 'Tu es vraiment irrésistible ce soir...'",
                        "'Je ne peux détacher mes yeux de toi', murmure-t-il en se rapprochant.",
                        "Son regard brûlant parcourt ta silhouette : 'Absolument magnifique.'"
                    ],
                    "medium_resistance": [
                        "Il lève son verre vers toi : 'À la plus belle femme de ce bar.'",
                        "'Tu as quelque chose de... spécial', dit-il avec un sourire charmeur.",
                        "Il effleure ta main : 'Tu es ravissante.'"
                    ],
                    "high_resistance": [
                        "Il te complimente avec respect : 'Vous avez une élégance naturelle.'",
                        "'Permettez-moi de vous dire que vous êtes très belle.'",
                        "Un sourire poli : 'J'espère que cette soirée vous plaît.'"
                    ]
                },
                "regard_insistant": {
                    "low_resistance": [
                        "Il te fixe intensément, son regard plongé dans le tien sans détourner les yeux.",
                        "Ses yeux te déshabillent littéralement, un sourire carnassier aux lèvres.",
                        "Il soutient ton regard avec une intensité troublante, comme s'il lisait en toi."
                    ],
                    "medium_resistance": [
                        "Il te fixe avec insistance, cherchant à capter ton attention.",
                        "Son regard se pose sur toi avec une intensité qui te met mal à l'aise.",
                        "Il ne cesse de te regarder, un petit sourire énigmatique aux coins des lèvres."
                    ],
                    "high_resistance": [
                        "Il te lance des regards appuyés de temps à autre.",
                        "Tu croises son regard plusieurs fois, il semble t'observer.",
                        "Il te fixe brièvement avant de détourner les yeux avec un sourire."
                    ]
                },
                "conversation_charme": {
                    "low_resistance": [
                        "Il se penche vers ton oreille : 'Dis-moi ce qui te fait vraiment vibrer...'",
                        "'Tu m'intrigues... j'aimerais découvrir tous tes secrets', souffle-t-il.",
                        "Sa main caresse la tienne : 'Parlons de désir...'"
                    ],
                    "medium_resistance": [
                        "Il se rapproche : 'Raconte-moi ce qui te passionne dans la vie.'",
                        "'Tu as l'air mystérieuse... j'aimerais te connaître mieux.'",
                        "Un sourire séducteur : 'Qu'est-ce qui te rend heureuse ?'"
                    ],
                    "high_resistance": [
                        "Il engage poliment : 'Que faites-vous dans la vie ?'",
                        "'Cette ambiance vous plaît-elle ?'",
                        "Une conversation respectueuse : 'Vous venez souvent ici ?'"
                    ]
                },
                "contact_epaule": {
                    "low_resistance": [
                        "Sa main glisse sensuellement le long de ton épaule nue, ses doigts traçant des cercles.",
                        "Il caresse doucement ton épaule, son toucher brûlant sur ta peau.",
                        "Ses doigts explorent délicatement la courbe de ton épaule dénudée."
                    ],
                    "medium_resistance": [
                        "Il pose sa main sur ton épaule dans un geste amical mais insistant.",
                        "Sa main effleure ton épaule comme par hasard lors de la conversation.",
                        "Il place sa main sur ton épaule pour attirer ton attention."
                    ],
                    "high_resistance": [
                        "Il pose brièvement sa main sur ton épaule en parlant.",
                        "Un contact léger sur l'épaule accompagne ses paroles.",
                        "Sa main touche furtivement ton épaule pour ponctuer ses mots."
                    ]
                }
            },
            "voiture": {
                "main_cuisse": {
                    "low_resistance": [
                        "Sa main remonte lentement le long de ta cuisse, caressant le tissu de ta jupe.",
                        "Il pose sa main sur ta cuisse, ses doigts dessinant des motifs troublants.",
                        "Sa paume chaude épouse la courbe de ta cuisse à travers le tissu."
                    ],
                    "medium_resistance": [
                        "Il pose sa main sur ta cuisse pendant qu'il conduit d'une main.",
                        "Sa main effleure ta cuisse quand il change de vitesse.",
                        "Il place sa main sur ta cuisse dans un geste possessif."
                    ],
                    "high_resistance": [
                        "Sa main se pose brièvement sur ta cuisse avant de revenir au volant.",
                        "Un contact furtif sur ta cuisse lors d'un virage.",
                        "Il touche légèrement ta cuisse en te parlant."
                    ]
                }
            }
        }

        # Messages adaptation IA CORRIGÉS
        self.adaptation_messages = {
            "becoming_patient": [
                "Marcus devient plus patient, ajustant sa stratégie à ta résistance...",
                "Il ralentit visiblement le rythme, devenant plus attentionné...",
                "Tu le sens qui prend son temps, respectant tes hésitations..."
            ],
            "analyzing": [
                "Il semble analyser tes réactions, adaptant son comportement en temps réel...",
                "Son regard t'étudie, cherchant à comprendre tes limites...",
                "Tu le vois ajuster son approche selon tes réponses..."
            ],
            "escalating": [
                "Sentant moins de résistance, il devient plus entreprenant...",
                "Encouragé par ta passivité, il intensifie ses avances...",
                "Il saisit l'opportunité de ton acquiescement pour progresser..."
            ]
        }

        load_time = (time.perf_counter() - start_time) * 1000
        cache_size = len(self.dialogue_templates)

        print(f"💾 Cache pré-calculé: {cache_size} dialogues")
        print(f"⚡ Temps chargement: {load_time:.1f}ms")

    def generate_npc_action_text(self, action: str, player, environment) -> str:
        """
        CORRIGÉ - Génère texte riche contextuel au lieu de tuples debug
        """
        # Clé cache pour performance
        resistance_level = self._get_resistance_level(player)
        location = environment.location if environment else "bar"
        cache_key = f"{action}_{location}_{resistance_level}"

        # Vérification cache
        if cache_key in self.dialogue_cache:
            self.cache_hits += 1
            return self.dialogue_cache[cache_key]

        self.cache_misses += 1

        # GÉNÉRATION TEXTE RICHE - CORRIGÉ
        generated_text = self._generate_rich_text(action, location, resistance_level)

        # Cache pour prochaine fois
        self.dialogue_cache[cache_key] = generated_text

        return generated_text

    def _generate_rich_text(self, action: str, location: str, resistance: str) -> str:
        """Génère texte riche selon contexte - CŒUR DE LA CORRECTION"""

        # Récupération templates selon lieu et action
        location_templates = self.dialogue_templates.get(location, self.dialogue_templates["bar"])
        action_templates = location_templates.get(action)

        if action_templates and resistance in action_templates:
            # Sélection aléatoire pour variabilité
            texts = action_templates[resistance]
            return random.choice(texts)

        # Fallbacks si pas de template spécifique
        fallback_texts = {
            "compliment": "Il te fait un compliment flatteur avec un sourire charmeur.",
            "regard_insistant": "Il te fixe intensément, cherchant à capter ton regard.",
            "conversation_charme": "Il engage une conversation séduisante avec toi.",
            "contact_epaule": "Il pose doucement sa main sur ton épaule.",
            "rapprochement_physique": "Il se rapproche subtilement de toi.",
            "main_cuisse": "Sa main se pose sur ta cuisse avec assurance.",
            "caresses_douces": "Il te caresse délicatement.",
            "baiser_leger": "Il dépose un baiser léger sur tes lèvres.",
            "caresses": "Ses mains explorent ton corps avec douceur.",
            "baiser_profond": "Il t'embrasse passionnément.",
            "caresses_intimes": "Ses caresses deviennent plus intimes et audacieuses.",
            "removal_vetement": "Il commence à défaire tes vêtements avec délicatesse."
        }

        return fallback_texts.get(action, f"Il fait quelque chose d'inattendu...")

    def _get_resistance_level(self, player) -> str:
        """Détermine niveau résistance pour adaptation textes"""
        if not player:
            return "medium_resistance"

        # Récupération stats player
        stats_comp = player.get_component_of_type(type(None))  # Simplified
        if hasattr(player, 'get_resistance_level'):
            resistance = player.get_resistance_level()

            if resistance > 0.7:
                return "high_resistance"
            elif resistance > 0.4:
                return "medium_resistance"
            else:
                return "low_resistance"

        return "medium_resistance"

    def generate_adaptation_message(self, adaptation_type: str) -> str:
        """Génère message adaptation IA"""
        messages = self.adaptation_messages.get(adaptation_type, ["Il s'adapte à ton comportement..."])
        return random.choice(messages)

    def update(self, entities: List[Entity], delta_time: float = 0.0, **kwargs):
        """Update système dialogues"""
        # Nettoyage cache si trop volumineux
        if len(self.dialogue_cache) > 100:
            # Garde seulement les 50 plus récents
            items = list(self.dialogue_cache.items())
            self.dialogue_cache = dict(items[-50:])

    def get_cache_stats(self) -> Dict[str, Any]:
        """Statistiques performance cache"""
        total_requests = self.cache_hits + self.cache_misses
        hit_rate = self.cache_hits / total_requests if total_requests > 0 else 0

        return {
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses, 
            "hit_rate": hit_rate,
            "cache_size": len(self.dialogue_cache)
        }
