#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup.py pour Strip, Sex & Seduce V2.0 - Reverse Seduction
Installation et distribution du jeu révolutionnaire
"""

from setuptools import setup, find_packages

setup(
    name="strip-sex-seduce-v2",
    version="2.0.0",
    description="Révolution gameplay: Premier jeu drague inversée avec contrôle total",
    long_description="""
    Strip, Sex & Seduce V2.0 - Reverse Seduction

    CONCEPT RÉVOLUTIONNAIRE:
    - TU ES UNE FEMME qui veut séduire et exciter un homme
    - TU CONTRÔLES 95% de l'action et de l'escalation  
    - 50+ actions contextuelles selon situation et lieu
    - 4 mini-jeux intégrés (Strip-tease, Massage, Dés, Simulation)
    - Système progression avec déblocages automatiques
    - Performance optimisée <50ms et architecture ECS professionnelle

    Innovation unique dans le genre éroge adulte !
    """,
    author="GameDev Team",
    author_email="gamedev@example.com",
    url="https://github.com/toutounnisgame-netizen/ara-ara",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        # Aucune dépendance externe - Python stdlib uniquement
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0", 
            "flake8>=4.0.0",
            "mypy>=0.950",
            "memory-profiler>=0.60"
        ]
    },
    entry_points={
        "console_scripts": [
            "strip-sex-seduce=main:main",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Adults Only",
        "Topic :: Games/Entertainment :: Simulation",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9", 
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    keywords="adult game simulation seduction erotic interactive reverse control",
    project_urls={
        "Bug Reports": "https://github.com/toutounnisgame-netizen/ara-ara/issues",
        "Source": "https://github.com/toutounnisgame-netizen/ara-ara",
    },
)
