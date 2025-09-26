#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Strip, Sex & Seduce V3.0 - ÉDITION OPTIMISÉE COMPLÈTE
Architecture ECS + IA Adaptative + Performance Garantie <50ms
Développé selon workflow gamedev spécialisé TDD
"""
import sys
import os
import traceback
from datetime import datetime

# Ajouter les modules du projet au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.game_session import GameSession
from utils.logger import GameLogger
from utils.performance import PerformanceMonitor

__version__ = "3.0.0"
__author__ = "GameDev Team"
__game_title__ = "Strip, Sex & Seduce"

def display_intro():
    """Affiche l'intro du jeu avec avertissement contenu adulte"""
    print("=" * 60)
    print(f"🔥 {__game_title__.upper()} V{__version__} 🔥")
    print("🎮 ÉDITION OPTIMISÉE COMPLÈTE")
    print("=" * 60)
    print()
    print("⚠️  AVERTISSEMENT - CONTENU ADULTE 18+ ⚠️")
    print("Ce jeu contient du contenu explicitement adulte.")
    print("Réservé exclusivement aux personnes majeures.")
    print()
    print("📋 DISCLAIMER:")
    print("• Fiction interactive pour adultes consentants")
    print("• Contenu fantasy, pas de promotion comportements réels")
    print("• Tapez 'aide' à tout moment pour les commandes")
    print()
    print("🆕 NOUVEAUTÉS V3.0:")
    print("• IA adaptative avec feedback visible")
    print("• Dialogues riches contextuels (CORRIGÉ)")
    print("• Escalation automatique entre lieux")
    print("• Performance optimisée <50ms garanti")
    print()

    # Vérification âge
    while True:
        response = input("Êtes-vous majeur(e) et acceptez-vous ce contenu ? (oui/non): ").lower().strip()
        if response in ['oui', 'o', 'yes', 'y']:
            break
        elif response in ['non', 'n', 'no']:
            print("\nAccès refusé. Au revoir!")
            sys.exit(0)
        else:
            print("Veuillez répondre par 'oui' ou 'non'")

    print("\n" + "=" * 60)

def main():
    """Fonction principale du jeu V3.0"""
    # Initialisation logging et monitoring
    logger = GameLogger()
    monitor = PerformanceMonitor()

    try:
        # Affichage intro
        display_intro()

        # Démarrage monitoring performance
        monitor.start_session()
        logger.info(f"Démarrage {__game_title__} V{__version__}")

        # Création session de jeu
        game = GameSession()
        print("🎮 Initialisation du jeu V3.0...")
        print("💡 Tapez 'aide' pour voir les commandes disponibles\n")

        # Lancement game loop principal
        game.run_game_loop()

    except KeyboardInterrupt:
        print("\n\n⚠️ Jeu interrompu par l'utilisateur")
        logger.info("Jeu interrompu par Ctrl+C")
    except Exception as e:
        print(f"\n❌ ERREUR CRITIQUE V3.0: {str(e)}")
        logger.error(f"Erreur critique: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
    finally:
        # Nettoyage et stats finales
        try:
            monitor.end_session()
            stats = monitor.get_session_stats()

            print(f"\n📊 STATISTIQUES SESSION V3.0:")
            print(f"⏱️  Durée: {stats.get('duration', 0):.1f} secondes")
            print(f"💾 Mémoire max: {stats.get('max_memory_mb', 0):.1f} MB")
            print(f"🎯 Actions: {stats.get('total_actions', 0)}")
            print(f"⚡ Performance: {stats.get('avg_response_ms', 0):.0f}ms moyenne")

            # Validation performance V3.0
            avg_response = stats.get('avg_response_ms', 0)
            if avg_response < 50:
                print("✅ Performance V3.0 VALIDÉE (<50ms)")
            else:
                print(f"⚠️ Performance dégradée: {avg_response:.0f}ms (objectif <50ms)")

            logger.info("Session V3.0 terminée proprement")

        except Exception as e:
            print(f"Erreur lors du nettoyage: {e}")

        print(f"\n👋 Merci d'avoir joué {__game_title__} V3.0 ! Au revoir!")

if __name__ == "__main__":
    main()
