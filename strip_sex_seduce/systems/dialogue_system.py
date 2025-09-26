
"""
CORRECTIF FINAL DialogueSystem V3.1 - IMMERSION PARFAITE
Remplace le contenu COMPLET de systems/dialogue_system.py
"""
from core.system import System
from core.entity import Entity
from typing import List, Dict, Any, Optional
import random
import json
import time

class DialogueSystem(System):
    """DialogueSystem V3.1 - CORRIGÉ POUR IMMERSION PARFAITE"""

    def __init__(self):
        super().__init__("DialogueSystem")

        # Cache pré-calculé pour performance
        self.dialogue_cache = {}
        self.context_templates = {}
        self._load_dialogue_assets()

        # Compteurs performance
        self.cache_hits = 0
        self.cache_misses = 0

    def _load_dialogue_assets(self):
        """Charge et pré-calcule TOUS les dialogues - COMPLET V3.1"""
        start_time = time.perf_counter()

        # TEMPLATES RICHES CONTEXTUELS COMPLETS
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
                },
                "rapprochement_physique": {
                    "low_resistance": [
                        "Il se rapproche de toi jusqu'à sentir la chaleur de son corps.",
                        "Il diminue l'espace entre vous deux, vous enveloppant de son aura.",
                        "Il se penche vers toi, si proche que tu peux sentir son parfum."
                    ],
                    "medium_resistance": [
                        "Il se rapproche subtilement pendant votre conversation.",
                        "Il réduit discrètement la distance qui vous sépare.",
                        "Il se penche légèrement vers toi pour mieux t'entendre."
                    ],
                    "high_resistance": [
                        "Il se rapproche respectueusement pour la conversation.",
                        "Il maintient une distance polie mais se rapproche légèrement.",
                        "Il se penche poliment pour mieux vous écouter."
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
                },
                "caresses_douces": {
                    "low_resistance": [
                        "Ses doigts tracent des cercles délicats sur ta peau exposée.",
                        "Il te caresse tendrement, explorant chaque centimètre accessible.",
                        "Ses mains expertes trouvent tous tes points sensibles."
                    ],
                    "medium_resistance": [
                        "Il te caresse doucement le bras et l'épaule.",
                        "Ses doigts effleurent délicatement ta peau.",
                        "Il te caresse avec une tendresse calculée."
                    ],
                    "high_resistance": [
                        "Il effleure légèrement ton bras.",
                        "Un contact doux et respectueux sur ta main.",
                        "Il caresse brièvement ta joue."
                    ]
                }
            },
            "salon": {
                "caresses": {
                    "low_resistance": [
                        "Ses mains explorent librement ton corps, découvrant chaque courbe.",
                        "Il te caresse avec une passion grandissante, ses gestes devenant plus audacieux.",
                        "Ses caresses deviennent plus intimes et pressantes."
                    ],
                    "medium_resistance": [
                        "Il te caresse tendrement, testant tes limites.",
                        "Ses mains explorent doucement tes formes.",
                        "Il intensifie graduellement ses caresses."
                    ],
                    "high_resistance": [
                        "Il te caresse délicatement les mains et les bras.",
                        "Ses caresses restent respectueuses et douces.",
                        "Il limite ses gestes à des zones acceptables."
                    ]
                },
                "baiser_leger": {
                    "low_resistance": [
                        "Il t'embrasse passionnément, ses lèvres dévorant les tiennes.",
                        "Votre baiser s'intensifie, plein de désir et de promesses.",
                        "Il t'embrasse avec une fougue qui te fait chavirer."
                    ],
                    "medium_resistance": [
                        "Il dépose un baiser tendre sur tes lèvres.",
                        "Vos lèvres se rencontrent dans un baiser doux.",
                        "Il t'embrasse délicatement, testant ta réaction."
                    ],
                    "high_resistance": [
                        "Il effleure tes lèvres d'un baiser léger.",
                        "Un baiser chaste et respectueux.",
                        "Il dépose un doux baiser sur ta joue."
                    ]
                }
            },
            "chambre": {
                "baiser_profond": {
                    "low_resistance": [
                        "Il t'embrasse avec une passion dévorante, vous perdant tous deux dans l'intensité du moment.",
                        "Vos lèvres se mêlent dans un baiser passionné qui enflamme tous vos sens.",
                        "Il t'embrasse profondément, ses mains s'emmêlant dans tes cheveux."
                    ],
                    "medium_resistance": [
                        "Il t'embrasse tendrement mais avec conviction.",
                        "Votre baiser exprime toute la tension accumulée.",
                        "Il t'embrasse avec une douceur persuasive."
                    ],
                    "high_resistance": [
                        "Il t'embrasse doucement, respectant ton hésitation.",
                        "Un baiser tendre qui exprime ses sentiments.",
                        "Il t'embrasse avec patience et délicatesse."
                    ]
                },
                "caresses_intimes": {
                    "low_resistance": [
                        "Ses mains explorent intimement ton corps, ne rencontrant aucune résistance.",
                        "Il te caresse avec une audace croissante, découvrant tes zones les plus sensibles.",
                        "Ses caresses deviennent de plus en plus intimes et passionnées."
                    ],
                    "medium_resistance": [
                        "Il te caresse intimement, guettant tes réactions.",
                        "Ses mains deviennent plus audacieuses, testant tes limites.",
                        "Il intensifie ses caresses, cherchant ton acceptation."
                    ],
                    "high_resistance": [
                        "Il te caresse avec respect, restant dans les limites.",
                        "Ses caresses restent douces et non intrusives.",
                        "Il respecte ta réticence tout en exprimant son désir."
                    ]
                },
                "removal_vetement": {
                    "low_resistance": [
                        "Il défait délicatement tes vêtements, révélant ta peau nacrée.",
                        "Ses mains expertes libèrent ton corps de ses entraves textiles.",
                        "Il dévêt lentement, savourant chaque révélation."
                    ],
                    "medium_resistance": [
                        "Il commence à défaire quelques boutons, observant ta réaction.",
                        "Il glisse délicatement une bretelle de ton épaule.",
                        "Il suggère timidement de retirer un vêtement."
                    ],
                    "high_resistance": [
                        "Il effleure le tissu de tes vêtements sans les défaire.",
                        "Il respecte ta pudeur tout en exprimant son désir.",
                        "Il se contente de caresses par-dessus tes vêtements."
                    ]
                }
            }
        }

        # Messages adaptation IA COMPLETS
        self.adaptation_messages = {
            "becoming_patient": [
                "Marcus devient plus patient, ajustant sa stratégie à ta résistance...",
                "Il ralentit visiblement le rythme, devenant plus attentionné...",
                "Tu le sens qui prend son temps, respectant tes hésitations...",
                "Il adapte son approche, devenant plus doux face à ta résistance..."
            ],
            "analyzing": [
                "Il semble analyser tes réactions, adaptant son comportement en temps réel...",
                "Son regard t'étudie, cherchant à comprendre tes limites...",
                "Tu le vois ajuster son approche selon tes réponses...",
                "Il observe attentivement tes signaux pour adapter sa stratégie..."
            ],
            "escalating": [
                "Sentant moins de résistance, il devient plus entreprenant...",
                "Encouragé par ta passivité, il intensifie ses avances...",
                "Il saisit l'opportunité de ton acquiescement pour progresser...",
                "Voyant ta réceptivité, il ose davantage..."
            ]
        }

        # ACTIONS NPC COMPLÈTES - MAPPING EXACT
        self.npc_actions_mapping = {
            # Actions génériques qui peuvent apparaître
            "default_action": "regard_insistant",
            "unknown_action": "compliment",
            "generic_action": "conversation_charme",

            # Actions spécifiques par niveau
            "level_1": ["compliment", "regard_insistant", "conversation_charme"],
            "level_2": ["contact_epaule", "rapprochement_physique"],
            "level_3": ["main_cuisse", "caresses_douces"],
            "level_4": ["caresses", "baiser_leger"],
            "level_5": ["baiser_profond", "caresses_intimes", "removal_vetement"]
        }

        load_time = (time.perf_counter() - start_time) * 1000
        cache_size = sum(len(location_data) for location_data in self.dialogue_templates.values())

        print(f"💾 Cache pré-calculé: {cache_size} dialogues")
        print(f"⚡ Temps chargement: {load_time:.1f}ms")

    def generate_npc_action_text(self, action: str, player, environment) -> str:
        """
        CORRIGÉ V3.1 - Génère texte riche contextuel avec mapping complet
        """
        # Normalisation action si inconnue
        normalized_action = self._normalize_action(action)

        # Détermination contexte
        resistance_level = self._get_resistance_level(player)
        location = environment.location if environment else "bar"

        # Clé cache pour performance
        cache_key = f"{normalized_action}_{location}_{resistance_level}"

        # Vérification cache
        if cache_key in self.dialogue_cache:
            self.cache_hits += 1
            return self.dialogue_cache[cache_key]

        self.cache_misses += 1

        # GÉNÉRATION TEXTE RICHE - MAPPING COMPLET
        generated_text = self._generate_rich_text(normalized_action, location, resistance_level)

        # Cache pour prochaine fois
        self.dialogue_cache[cache_key] = generated_text

        return generated_text

    def _normalize_action(self, action) -> str:
        """Normalise les actions NPC - SIMPLE FIX V3.1.1"""

        # FIX: Convertir tout en string de façon sécurisée
        if isinstance(action, (tuple, list)):
            action_str = str(action[0]) if len(action) > 0 else "compliment"
        else:
            action_str = str(action)

        # Sécurité supplémentaire
        if not action_str or action_str == "None":
            return "compliment"

        # Actions directes connues
        known_actions = [
            "compliment", "regard_insistant", "conversation_charme",
            "contact_epaule", "rapprochement_physique", "main_cuisse",
            "caresses_douces", "caresses", "baiser_leger", "baiser_profond",
            "caresses_intimes", "removal_vetement"
        ]

        if action_str in known_actions:
            return action_str

        # Mapping des actions similaires ou génériques
        action_mappings = {
            "regarder": "regard_insistant",
            "complimenter": "compliment",
            "parler": "conversation_charme",
            "toucher": "contact_epaule",
            "se_rapprocher": "rapprochement_physique",
            "caresser": "caresses_douces",
            "embrasser": "baiser_leger",
            "default": "compliment"  # Action par défaut
        }

        # Chercher mapping partiel de façon sûre
        try:
            lowered = action_str.lower()
            for key, mapped_action in action_mappings.items():
                if key in lowered:
                    return mapped_action
        except Exception:
            pass

        # Si rien trouvé, utiliser action par défaut
        return "compliment"

    def _generate_rich_text(self, action: str, location: str, resistance: str) -> str:
        """Génère texte riche selon contexte - MAPPING COMPLET V3.1"""

        # Récupération templates selon lieu et action
        location_templates = self.dialogue_templates.get(location, self.dialogue_templates["bar"])
        action_templates = location_templates.get(action)

        if action_templates and resistance in action_templates:
            # Sélection aléatoire pour variabilité
            texts = action_templates[resistance]
            return random.choice(texts)

        # Fallback avec action dans lieu par défaut si pas dans lieu actuel
        if location != "bar":
            bar_templates = self.dialogue_templates["bar"]
            if action in bar_templates and resistance in bar_templates[action]:
                texts = bar_templates[action][resistance]
                return random.choice(texts)

        # Fallback ultime avec actions connues
        fallback_by_location = {
            "bar": {
                "compliment": "Il te fait un compliment flatteur avec un sourire charmeur.",
                "regard_insistant": "Il te fixe intensément, cherchant à capter ton regard.",
                "conversation_charme": "Il engage une conversation séduisante avec toi.",
                "contact_epaule": "Il pose doucement sa main sur ton épaule.",
                "rapprochement_physique": "Il se rapproche subtilement de toi."
            },
            "voiture": {
                "main_cuisse": "Sa main se pose sur ta cuisse avec assurance.",
                "caresses_douces": "Il te caresse délicatement.",
                "compliment": "Il te complimente tout en conduisant."
            },
            "salon": {
                "caresses": "Ses mains explorent ton corps avec douceur.",
                "baiser_leger": "Il dépose un baiser léger sur tes lèvres.",
                "compliment": "Il te fait un compliment dans l'intimité du salon."
            },
            "chambre": {
                "baiser_profond": "Il t'embrasse passionnément.",
                "caresses_intimes": "Ses caresses deviennent plus intimes et audacieuses.",
                "removal_vetement": "Il commence à défaire tes vêtements avec délicatesse.",
                "compliment": "Il murmure des compliments à ton oreille."
            }
        }

        location_fallbacks = fallback_by_location.get(location, fallback_by_location["bar"])
        return location_fallbacks.get(action, f"Il te fait un geste tendre et séducteur.")

    def _get_resistance_level(self, player) -> str:
        """Détermine niveau résistance pour adaptation textes"""
        if not player:
            return "medium_resistance"

        # Récupération stats player - essai multiple méthodes
        try:
            # Méthode 1: get_resistance_level direct
            if hasattr(player, 'get_resistance_level'):
                resistance = player.get_resistance_level()

                if resistance > 0.7:
                    return "high_resistance"
                elif resistance > 0.4:
                    return "medium_resistance"
                else:
                    return "low_resistance"

            # Méthode 2: via stats component
            stats_comp = player.get_component_of_type(type(None))
            if hasattr(player, 'stats') and hasattr(player.stats, 'volonte'):
                volonte = player.stats.volonte
                if volonte > 70:
                    return "high_resistance"
                elif volonte > 40:
                    return "medium_resistance"
                else:
                    return "low_resistance"

        except Exception:
            pass

        return "medium_resistance"  # Safe fallback

    def generate_adaptation_message(self, adaptation_type: str) -> str:
        """Génère message adaptation IA"""
        messages = self.adaptation_messages.get(adaptation_type, ["Il s'adapte à ton comportement..."])
        return random.choice(messages)

    def update(self, entities: List[Entity], delta_time: float = 0.0, **kwargs):
        """Update système dialogues"""
        # Nettoyage cache si trop volumineux
        if len(self.dialogue_cache) > 200:  # Augmenté pour plus d'efficacité
            # Garde seulement les 100 plus récents
            items = list(self.dialogue_cache.items())
            self.dialogue_cache = dict(items[-100:])

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
