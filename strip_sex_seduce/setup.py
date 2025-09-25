#!/usr/bin/env python3
"""
Setup script for Strip, Sex & Seduce
"""

from setuptools import setup, find_packages
import os

# Lecture README pour description
def read_readme():
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()

setup(
    name="strip-sex-seduce",
    version="1.0.0",
    description="Jeu narratif interactif adulte avec architecture ECS",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="GameDev Team",
    author_email="dev@example.com",
    url="https://github.com/toutounnisgame-netizen/ara-ara/tree/main/strip_sex_seduce",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'assets': ['**/*.json'],
    },
    python_requires='>=3.8',
    install_requires=[
        # Aucune dépendance externe - Python pur
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'black>=22.0.0',
            'flake8>=4.0.0',
            'mypy>=0.950',
        ]
    },
    entry_points={
        'console_scripts': [
            'strip-sex-seduce=main:main',
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop", 
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Games/Entertainment :: Role-Playing",
        "Natural Language :: French",
    ],
    keywords="game, interactive fiction, adult, narrative, ecs",
    project_urls={
        "Bug Reports": "https://github.com/toutounnisgame-netizen/ara-ara/issues",
        "Source": "https://github.com/toutounnisgame-netizen/ara-ara/tree/main/strip_sex_seduce",
    },
)
