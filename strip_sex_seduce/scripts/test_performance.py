#!/usr/bin/env python3
"""
Test Performance V2.0 - Validation <50ms garanti
"""

import sys
import os
import time

# Setup path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from systems.dialogue_system import DialogueSystem
from systems.stats_system import StatsSystem
from entities.player import PlayerCharacter
from entities.npc import NPCMale
from entities.environment import Environment

def test_dialogue_performance():
    """Test performance dialogue system < 10ms"""

    print("🧪 TEST PERFORMANCE DIALOGUE SYSTEM")
    print("-" * 40)

    dialogue_system = DialogueSystem()
    player = PlayerCharacter("Test")
    environment = Environment("bar")

    # Test 100 générations
    total_time = 0
    max_time = 0

    for i in range(100):
        start = time.perf_counter()

        text = dialogue_system.generate_npc_action_text(
            "compliment", player, environment
        )

        end = time.perf_counter()
        generation_time = (end - start) * 1000  # ms

        total_time += generation_time
        max_time = max(max_time, generation_time)

    avg_time = total_time / 100

    print(f"Temps moyen: {avg_time:.2f}ms")
    print(f"Temps maximum: {max_time:.2f}ms")
    print(f"Objectif <10ms: {'✅ RÉUSSI' if max_time < 10 else '❌ ÉCHEC'}")

    return max_time < 10

def test_stats_responsiveness():
    """Test réactivité stats system"""

    print("\n🧪 TEST RÉACTIVITÉ STATS")
    print("-" * 40)

    stats_system = StatsSystem()
    player = PlayerCharacter("Test")

    # État initial
    initial_volonte = player.get_component_of_type(type(None))  # Simplified

    # Application action
    result = stats_system.apply_npc_action(
        player, "compliment", {"location": "bar"}
    )

    success = result.get("visible_change", False)
    print(f"Changement visible: {'✅ OUI' if success else '❌ NON'}")

    return success

def main():
    """Test performance global"""

    print("🚀 TESTS PERFORMANCE V2.0")
    print("=" * 50)

    results = []

    # Test dialogue
    results.append(test_dialogue_performance())

    # Test stats
    results.append(test_stats_responsiveness())

    # Résultat global
    all_passed = all(results)

    print("\n" + "=" * 50)
    print(f"RÉSULTAT GLOBAL: {'✅ TOUS TESTS RÉUSSIS' if all_passed else '❌ ÉCHECS DÉTECTÉS'}")

    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
