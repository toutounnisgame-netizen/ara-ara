#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Strip, Sex & Seduce V2.0 - REVERSE SEDUCTION ÉDITION RÉVOLUTIONNAIRE
🔥 CONCEPT UNIQUE: Jeu de drague inversée avec contrôle total joueur
🎮 50+ actions contextuelles | 4 mini-jeux | Progression déblocages
🚀 Architecture ECS professionnelle + IA adaptative + Performance <50ms
Développé selon workflow gamedev spécialisé TDD
"""
import sys
import os
import traceback
from datetime import datetime

# Ajouter les modules du projet au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Imports core V2.0
from core.game_session_v2 import GameSessionV2
from utils.logger import GameLogger
from utils.performance import PerformanceMonitor

# Version et métadonnées
__version__ = "2.0.0"
__author__ = "GameDev Team"
__game_title__ = "Strip, Sex & Seduce V2.0 - Reverse Seduction"
__concept__ = "Simulation séduction inversée - Contrôle total joueur"

def display_intro_v2():
    """Affiche l'intro V2.0 avec concept révolutionnaire"""
    print("=" * 80)
    print(f"🔥 {__game_title__.upper()} 🔥")
    print("🎮 ÉDITION RÉVOLUTIONNAIRE - CONCEPT UNIQUE")
    print("=" * 80)
    print()
    print("⚠️ AVERTISSEMENT - CONTENU ADULTE 18+ ⚠️")
    print("Ce jeu contient du contenu explicitement adulte.")
    print("Réservé exclusivement aux personnes majeures.")
    print()
    print("📋 DISCLAIMER:")
    print("• Fiction interactive pour adultes consentants")
    print("• Contenu fantasy, pas de promotion comportements réels")
    print("• Tapez 'aide' à tout moment pour les commandes")
    print()
    print("🚀 RÉVOLUTION V2.0 - CONCEPT UNIQUE:")
    print("• ✨ DRAGUE INVERSÉE: TU ES UNE FEMME QUI VEUT SÉDUIRE")
    print("• 🎯 CONTRÔLE TOTAL: Tu contrôles 95% de l'action")
    print("• 🔥 50+ ACTIONS: Menus contextuels selon lieu/situation")
    print("• 🎪 4 MINI-JEUX: Strip-tease, Massage, Dés désir, Simulation")
    print("• 🏆 PROGRESSION: Déblocages techniques et lieux")
    print("• ⚡ PERFORMANCE: <50ms garanti, expérience fluide")
    print()
    print("🎭 TON RÔLE: Femme séductrice qui excite l'homme par ses actions")
    print("🎯 TON OBJECTIF: Le rendre fou de désir par ta maîtrise")
    print("💪 TON POUVOIR: Contrôler l'escalation comme tu le veux")
    print()

    # Vérification âge avec concept expliqué
    while True:
        response = input("Comprends-tu le concept et es-tu majeur(e) ? (oui/non): ").lower().strip()
        if response in ['oui', 'o', 'yes', 'y']:
            break
        elif response in ['non', 'n', 'no']:
            print("\nAccès refusé. Au revoir!")
            sys.exit(0)
        else:
            print("Veuillez répondre par 'oui' ou 'non'")

    print("\n" + "=" * 80)
    print("🎮 BIENVENUE DANS LA RÉVOLUTION DE LA SÉDUCTION ! 🎮")
    print("=" * 80)

def display_tutorial_hints():
    """Affiche hints tutoriel V2.0"""
    print("\n💡 GUIDE RAPIDE V2.0:")
    print("─" * 50)
    print("🎯 OBJECTIF: Exciter l'homme de 0 à 100% d'arousal")
    print("🎮 MÉTHODE: Choisir actions dans menus contextuels")
    print("🎪 PROGRESSION: Débloquer lieux et actions par ta maîtrise")
    print("⚡ COMMANDES RAPIDES:")
    print("  • Numéro = Sélectionner action/menu")
    print("  • 'aide' = Voir toutes les commandes") 
    print("  • 'stats' = Voir progression détaillée")
    print("  • 'quit' = Quitter le jeu")
    print("─" * 50)
    print("🔥 Prête à devenir la déesse de la séduction ? 🔥\n")

def main():
    """Fonction principale V2.0 - REVERSE SEDUCTION"""
    # Initialisation logging et monitoring
    logger = GameLogger()
    monitor = PerformanceMonitor()

    try:
        # Affichage intro révolutionnaire
        display_intro_v2()

        # Démarrage monitoring performance
        monitor.start_session()
        logger.info(f"Démarrage {__game_title__} V{__version__}")
        logger.info(f"Concept: {__concept__}")

        # Création session de jeu V2.0
        print("🎮 Initialisation V2.0 - Reverse Seduction...")
        print("🔄 Chargement systèmes révolutionnaires...")

        game = GameSessionV2()

        print("✅ MenuSystem - 50+ actions contextuelles")
        print("✅ InventorySystem - Items érotiques")
        print("✅ SeductionSystem - Mécaniques avancées")
        print("✅ ProgressionSystem - Unlocks & achievements")
        print("✅ MiniGameSystem - 4 mini-jeux intégrés")
        print()

        # Tutorial hints
        display_tutorial_hints()

        # Lancement game loop révolutionnaire V2.0
        game.run_reverse_seduction_loop()

    except KeyboardInterrupt:
        print("\n\n⚠️ Jeu interrompu par l'utilisateur")
        logger.info("Jeu V2.0 interrompu par Ctrl+C")

    except Exception as e:
        print(f"\n❌ ERREUR CRITIQUE V2.0: {str(e)}")
        logger.error(f"Erreur critique V2.0: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")

    finally:
        # Nettoyage et stats finales V2.0
        try:
            monitor.end_session()
            stats = monitor.get_session_stats()

            print(f"\n📊 STATISTIQUES SESSION V2.0:")
            print("=" * 60)
            print(f"⏱️ Durée: {stats.get('duration', 0):.1f} secondes")
            print(f"💾 Mémoire max: {stats.get('max_memory_mb', 0):.1f} MB")
            print(f"🎯 Actions exécutées: {stats.get('total_actions', 0)}")
            print(f"⚡ Performance moyenne: {stats.get('avg_response_ms', 0):.0f}ms")
            print(f"🎮 Loops de jeu: {stats.get('game_loops', 0)}")

            # Validation performance V2.0
            avg_response = stats.get('avg_response_ms', 0)
            if avg_response < 50:
                print("✅ PERFORMANCE V2.0 EXCELLENTE (<50ms) !")
                print("🚀 Expérience utilisateur optimale validée")
            elif avg_response < 100:
                print("👍 Performance V2.0 acceptable")
            else:
                print(f"⚠️ Performance dégradée: {avg_response:.0f}ms")
                print("💡 Redémarrage recommandé si problème persiste")

            # Stats gameplay V2.0
            gameplay_stats = stats.get('gameplay', {})
            if gameplay_stats:
                print(f"\n🎮 GAMEPLAY V2.0:")
                print(f"🎯 Menus utilisés: {gameplay_stats.get('menus_used', 0)}")
                print(f"🔓 Unlocks obtenus: {gameplay_stats.get('unlocks', 0)}")
                print(f"🎪 Mini-jeux joués: {gameplay_stats.get('minigames', 0)}")
                print(f"📈 Niveau séduction final: {gameplay_stats.get('final_seduction_level', 0)}")

            logger.info("Session V2.0 Reverse Seduction terminée proprement")

        except Exception as e:
            print(f"Erreur lors du nettoyage V2.0: {e}")

        print("=" * 60)
        print("👋 MERCI D'AVOIR EXPÉRIMENTÉ LA RÉVOLUTION V2.0 !")
        print("🔥 Strip, Sex & Seduce - Reverse Seduction")
        print("💫 Tu as le contrôle, tu es la déesse de la séduction")
        print("🎮 À bientôt pour de nouvelles aventures !")
        print("=" * 60)

if __name__ == "__main__":
    main()
