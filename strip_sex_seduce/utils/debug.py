"""
Debug - Outils développement et debug
"""

from typing import Any, Dict
import json

class DebugTools:
    @staticmethod
    def dump_entity_state(entity) -> Dict[str, Any]:
        """Dump complet état entity pour debug"""
        try:
            return entity.to_dict()
        except:
            return {"error": "Cannot serialize entity"}

    @staticmethod
    def print_performance_report(system_manager):
        """Affiche rapport performance systems"""
        report = system_manager.get_performance_report()

        print("\n=== PERFORMANCE REPORT ===")
        for system_name, stats in report.items():
            print(f"{system_name}:")
            print(f"  Calls: {stats['total_calls']}")
            print(f"  Avg time: {stats['avg_time']*1000:.2f}ms")
            print(f"  Last time: {stats['last_update_time']*1000:.2f}ms")
