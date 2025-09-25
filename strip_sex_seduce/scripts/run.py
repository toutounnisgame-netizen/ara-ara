#!/usr/bin/env python3
"""Script de lancement du jeu"""

import sys
import os

# Ajout path projet
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import main

if __name__ == "__main__":
    main()
