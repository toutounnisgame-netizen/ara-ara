#!/usr/bin/env python3
"""Script lancement tests"""

import sys
import os
import subprocess

# Path projet
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def run_tests():
    os.chdir(project_root)

    try:
        # Tests avec pytest si disponible
        result = subprocess.run(["python", "-m", "pytest", "tests/", "-v"], 
                              capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
    except FileNotFoundError:
        # Fallback unittest
        result = subprocess.run(["python", "-m", "unittest", "discover", "tests"], 
                              capture_output=True, text=True)
        print(result.stdout)

if __name__ == "__main__":
    run_tests()
