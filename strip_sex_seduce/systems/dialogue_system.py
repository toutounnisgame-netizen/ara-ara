"""
DialogueSystem V2.0 - Performance <50ms garanti
Correctif critique: Cache pré-calculé + sélection instantanée
"""

from core.system import System
from core.entity import Entity
from components.dialogue import DialogueComponent
from typing import List, Dict, Any
import random
import time

class DialogueSystem(System):
    """System dialogues ULTRA-OPTIMISÉ pour performance <50ms"""

    def __init__(self):
        super().__init__("DialogueSystem")

        # CACHE PRÉ-CALCULÉ - Performance critique <50ms
        self.action_descriptions = {
            # Actions base intensité 1-2
            "compliment": [
                "Il te sourit chaleureusement : 'Tu es vraiment magnifique ce soir...'",
                "Son regard s'attarde sur toi : 'Cette robe te va à merveille.'",
                "'J'adore ton parfum, il est... envoûtant.'",
                "'Tu illumines vraiment cette soirée, tu sais ?'",
                "Il s'approche légèrement : 'Tu as quelque chose de spécial...'"
            ],
            "regard_insistant": [
                "Ses yeux ne quittent pas les tiens, intensément...",
                "Il te regarde avec une attention troublante...",
                "Son regard glisse lentement sur ta silhouette...",
                "Il soutient ton regard avec un sourire énigmatique...",
                "Tu sens son regard qui te déshabille du regard..."
            ],
            "conversation_charme": [
                "Il engage une conversation pleine de charme et d'esprit...",
                "Sa voix devient plus grave, plus séductrice...",
                "'Raconte-moi... qu'est-ce qui te passionne vraiment ?'",
                "Il trouve toujours le mot juste pour te faire rire...",
                "La conversation dérive vers des sujets plus intimes..."
            ],

            # Actions escalation modérée intensité 3-4
            "contact_epaule": [
                "Sa main se pose doucement sur ton épaule nue...",
                "Ses doigts effleurent ta peau, traçant de petits cercles...",
                "Il se rapproche, sa main chaude sur ton épaule...",
                "Il laisse sa main s'attarder plus longtemps que nécessaire...",
                "Tu sens la chaleur de sa paume à travers le tissu..."
            ],
            "rapprochement_physique": [
                "Il se rapproche insensiblement de toi...",
                "L'espace entre vous se réduit progressivement...",
                "Il trouve des prétextes pour être plus près...",
                "Sa proximité devient troublante...",
                "Tu sens son souffle effleurer ton cou..."
            ],
            "main_cuisse": [
                "Sa main glisse lentement vers ta cuisse...",
                "Tu sens sa paume chaude sur ta jambe...",
                "Il caresse doucement ta cuisse du bout des doigts...",
                "Sa main remonte imperceptiblement...",
                "Tu frissonnes sous cette caresse inattendue..."
            ],

            # Actions escalation forte intensité 5+
            "baiser_leger": [
                "Il s'approche et dépose un baiser délicat sur tes lèvres...",
                "Ses lèvres effleurent les tiennes avec tendresse...",
                "Il t'embrasse doucement, savourant l'instant...",
                "Un baiser doux mais qui laisse présager plus...",
                "Ses lèvres trouvent les tiennes dans un baiser tendre..."
            ],
            "caresses": [
                "Ses mains explorent délicatement ton corps...",
                "Il caresse ta peau avec une douceur troublante...",
                "Ses doigts dessinent des chemins sur ta peau...",
                "Tu te perds sous ses caresses expertes...",
                "Chaque caresse éveille de nouveaux frissons..."
            ],
            "baiser_profond": [
                "Il t'embrasse avec passion, sa langue cherchant la tienne...",
                "Vos bouches se mélangent dans un baiser intense...",
                "Il approfondit le baiser, te coupant le souffle...",
                "Tu te laisses emporter par ce baiser dévorant...",
                "L'intensité de ce baiser vous fait perdre la tête..."
            ]
        }

        # CACHE CONTEXTUEL selon résistance - Performance optimisée
        self.resistance_modifiers = {
            "high_resistance": {
                "prefix": ["Malgré tes réticences, ", "Doucement, ", "Avec patience, "],
                "suffix": [" Tu essaies de reculer...", " Tu te crispes légèrement...", " Ton corps résiste..."]
            },
            "medium_resistance": {
                "prefix": ["", "Tendrement, ", "Délicatement, "],
                "suffix": [" Tu hésites un instant...", " Une partie de toi résiste encore...", " Tu te sens troublée..."]
            },
            "low_resistance": {
                "prefix": ["Naturellement, ", "Sans résistance, ", "Tu te laisses faire... "],
                "suffix": [" Tu ne résistes plus...", " Ton corps répond à ses gestes...", " Tu t'abandonnes..."]
            }
        }

        # CACHE lieux pour variation contextuelle
        self.location_contexts = {
            "bar": {
                "suffix": [" autour de vous, les autres clients...", " la musique couvre vos murmures..."],
                "constraints": "public"
            },
            "voiture": {
                "suffix": [" dans l'intimité de l'habitacle...", " les vitres teintées vous protègent..."],
                "constraints": "semi_private"
            },
            "salon": {
                "suffix": [" dans la pénombre du salon...", " l'atmosphère devient électrique..."],
                "constraints": "private"
            },
            "chambre": {
                "suffix": [" dans l'intimité de la chambre...", " plus rien ne peut vous arrêter..."],
                "constraints": "intimate"
            }
        }

        # Anti-répétition avec index circulaire
        self._last_used = {}
        self._generation_count = 0

    def update(self, entities: List[Entity], delta_time: float = 0.0, **kwargs):
        """Update minimal pour performance"""
        # Pas de traitement lourd ici pour maintenir <50ms
        pass

    def generate_npc_action_text(self, action: str, player, environment) -> str:
        """
        Génération ULTRA-RAPIDE <10ms avec cache

        Args:
            action: Action NPC à décrire
            player: Entity player pour contexte résistance
            environment: Entity environment pour contexte lieu

        Returns:
            Texte description immersive
        """
        start_time = time.perf_counter()

        # Récupération INSTANTANÉE depuis cache
        base_descriptions = self.action_descriptions.get(action, [f"Il {action}."])

        # Contexte résistance (performance optimisée)
        resistance_level = player.get_resistance_level()
        if resistance_level > 0.7:
            resistance_key = "high_resistance"
        elif resistance_level > 0.3:
            resistance_key = "medium_resistance"
        else:
            resistance_key = "low_resistance"

        # Sélection description avec évitement répétition
        last_idx = self._last_used.get(action, -1)
        available_indices = [i for i in range(len(base_descriptions)) if i != last_idx]

        if available_indices:
            chosen_idx = random.choice(available_indices)
            self._last_used[action] = chosen_idx
        else:
            chosen_idx = 0  # Fallback

        base_text = base_descriptions[chosen_idx]

        # Modification contextuelle légère (performance critique)
        resistance_mod = self.resistance_modifiers[resistance_key]
        location_name = environment.location if hasattr(environment, 'location') else 'bar'
        location_mod = self.location_contexts.get(location_name, self.location_contexts['bar'])

        # Construction finale RAPIDE
        final_text = base_text

        # Ajout modificateurs (50% chance pour éviter verbosité)
        if random.random() < 0.5:
            if random.random() < 0.3:  # Prefix resistance
                final_text = random.choice(resistance_mod["prefix"]) + final_text

            if random.random() < 0.3:  # Suffix resistance  
                final_text += random.choice(resistance_mod["suffix"])

        # Performance monitoring
        generation_time = (time.perf_counter() - start_time) * 1000
        self._generation_count += 1

        # Warning si > 10ms (critique)
        if generation_time > 10:
            print(f"⚠️ DialogueSystem: {generation_time:.1f}ms (target <10ms)")

        return final_text

    def generate_adaptation_message(self, old_strategy: str, new_strategy: str) -> str:
        """Messages adaptation IA visible - Cache pour performance"""

        adaptation_messages = {
            ("normal", "extra_patient"): "Tu le sens qui ralentit le rythme, devenant plus attentionné...",
            ("normal", "confident"): "Son assurance grandit, il semble plus déterminé...",
            ("normal", "aggressive"): "Il devient plus insistant, plus direct dans ses approches...",
            ("extra_patient", "normal"): "Il reprend un rythme plus naturel...",
            ("confident", "extra_patient"): "Face à ta résistance, il redevient plus prudent...",
            ("aggressive", "normal"): "Il modère son approche, se faisant plus subtil..."
        }

        return adaptation_messages.get((old_strategy, new_strategy), "")

    def get_performance_stats(self) -> Dict[str, Any]:
        """Stats performance pour debug"""
        return {
            "generations_count": self._generation_count,
            "cache_size": len(self.action_descriptions),
            "avg_actions_per_type": sum(len(descs) for descs in self.action_descriptions.values()) / len(self.action_descriptions)
        }

# PERFORMANCE OPTIMISÉE: <10ms génération, cache efficace, anti-répétition
