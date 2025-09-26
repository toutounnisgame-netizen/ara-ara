#!/usr/bin/env python3
"""
Validation Installation V2.0 - Vérification correctifs
"""

import sys
import os
import importlib

# Setup path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def check_file_exists(filepath):
    """Vérifie existence fichier"""
    return os.path.exists(filepath)

def check_module_import(module_name):
    """Vérifie import module"""
    try:
        importlib.import_module(module_name)
        return True
    except ImportError:
        return False

def validate_installation():
    """Validation installation complète"""

    print("🔍 VALIDATION INSTALLATION V2.0")
    print("=" * 50)

    # Fichiers critiques
    critical_files = [
        "systems/dialogue_system.py",
        "systems/stats_system.py", 
        "systems/ai_system.py",
        "systems/clothing_system.py",
        "entities/npc.py",
        "entities/environment.py",
        "assets/config/balance.json",
        "assets/dialogues/bar.json"
    ]

    print("📁 VÉRIFICATION FICHIERS:")
    all_files_ok = True

    for file_path in critical_files:
        exists = check_file_exists(file_path)
        status = "✅" if exists else "❌"
        print(f"  {status} {file_path}")
        all_files_ok = all_files_ok and exists

    # Modules critiques
    critical_modules = [
        "systems.dialogue_system",
        "systems.stats_system",
        "entities.npc",
        "entities.environment"
    ]

    print("\n📦 VÉRIFICATION IMPORTS:")
    all_imports_ok = True

    for module_name in critical_modules:
        imports_ok = check_module_import(module_name)
        status = "✅" if imports_ok else "❌"
        print(f"  {status} {module_name}")
        all_imports_ok = all_imports_ok and imports_ok

    # Résultat global
    all_ok = all_files_ok and all_imports_ok

    print("\n" + "=" * 50)
    print(f"INSTALLATION: {'✅ VALIDÉE' if all_ok else '❌ PROBLÈMES DÉTECTÉS'}")

    if not all_ok:
        print("\n🔧 ACTIONS CORRECTIVES:")
        if not all_files_ok:
            print("  • Vérifier copie de tous les fichiers")
        if not all_imports_ok:
            print("  • Restart Python interpreter")
            print("  • Vérifier PYTHONPATH")

    return all_ok

if __name__ == "__main__":
    success = validate_installation()
    sys.exit(0 if success else 1)
