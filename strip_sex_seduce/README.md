# 🔥 Strip, Sex & Seduce

**Jeu narratif interactif adulte** avec architecture Entity-Component-System (ECS).

⚠️ **CONTENU ADULTE 18+** - Réservé exclusivement aux personnes majeures.

## 📋 Description

Strip, Sex & Seduce est un jeu narratif textuel explorant les dynamiques de séduction et résistance à travers un système de gameplay sophistiqué. Le joueur navigue dans différents lieux (bar, voiture, salon, chambre) face à un NPC doté d'une IA adaptative qui ajuste son comportement selon la résistance manifestée.

### 🎯 Caractéristiques Principales

- **Système de stats** : Volonté/Excitation en temps réel
- **IA adaptative** : NPC qui s'adapte au style de jeu
- **Gestion vêtements détaillée** : Système complexe avec historique
- **Rejouabilité** : Variabilité des personnalités et scénarios
- **Architecture ECS** : Code modulaire et extensible

### 🔧 Spécifications Techniques

- **Langage** : Python 3.8+ pur (sans dépendances)
- **Performance** : <5MB RAM, <50ms temps de réponse
- **Plateforme** : Console multiplateforme (Windows/Linux/macOS)
- **Architecture** : Entity-Component-System stricte

## 🚀 Installation

### Prérequis
- Python 3.8 ou supérieur
- Système d'exploitation : Windows, Linux ou macOS

### Installation rapide
```bash
git clone https://github.com/toutounnisgame-netizen/ara-ara.git
cd ara-ara/strip_sex_seduce
python main.py
```

### Installation développeur
```bash
pip install -e .[dev]  # Installation avec outils développement
```

## 🎮 Utilisation

### Lancement
```bash
python main.py
```

### Commandes de base
- `r` ou `résister` : Résister à l'action NPC
- `a` ou `permettre` : Laisser faire l'action
- `f` ou `fuir` : Tenter de quitter la situation
- `l` ou `regarder` : Observer l'environnement
- `aide` : Afficher l'aide complète

### Interface
L'interface affiche en permanence :
- **Lieu actuel** : Bar, Voiture, Salon ou Chambre
- **Volonté** : Niveau de résistance (0-100)
- **Excitation** : Niveau d'arousal (0-100)
- **État vêtements** : Modifications en cours

## 🏗️ Architecture

### Structure ECS
```
Entities (Objets du jeu)
├── PlayerCharacter (Joueur)
├── NPCMale (Personnage non-joueur)
├── Environment (Environnements/lieux)
└── GameState (État global)

Components (Données)
├── StatsComponent (Volonté/Excitation)
├── ClothingComponent (Gestion vêtements)
├── PersonalityComponent (Traits NPC)
└── DialogueComponent (Dialogues contextuels)

Systems (Logique)
├── StatsSystem (Équilibrage)
├── AISystem (IA adaptative)
├── ClothingSystem (Vêtements)
└── DialogueSystem (Génération texte)
```

### Flux de données
```
Input Console → InputSystem → GameSession
                ↓
         Update Systems → Update Entities → Update Components
                ↓
            Output Console
```

## 🧪 Tests

### Lancement des tests
```bash
python -m pytest tests/
```

### Coverage
```bash
python -m pytest --cov=. tests/
```

### Tests spécifiques
```bash
# Tests core ECS
python -m pytest tests/test_core/

# Tests gameplay
python -m pytest tests/test_gameplay/
```

## 📁 Structure Projet

```
strip_sex_seduce/
├── main.py              # Entry point
├── core/                # Framework ECS
├── components/          # Components spécialisés  
├── systems/             # Systems de jeu
├── entities/            # Entities principales
├── assets/              # Configuration JSON
├── tests/               # Tests TDD
├── utils/               # Utilitaires
├── docs/                # Documentation
└── scripts/             # Scripts utiles
```

## ⚙️ Configuration

### Fichiers de configuration
- `assets/config/settings.json` : Paramètres généraux
- `assets/config/balance.json` : Équilibrage gameplay
- `assets/dialogues/*.json` : Textes par lieu
- `assets/personalities/*.json` : Configurations NPC

### Personnalisation
Le jeu est entièrement configurable via les fichiers JSON pour :
- Modifier l'équilibrage des stats
- Ajouter de nouveaux dialogues
- Créer de nouvelles personnalités NPC
- Ajuster les paramètres de performance

## 🤝 Développement

### Architecture TDD
Le projet suit une approche Test-Driven Development avec :
- Tests unitaires (logique pure)
- Tests d'intégration (systems interconnectés)
- Tests gameplay (scénarios complets)

### Standards de code
- **Style** : PEP 8 avec Black formatter
- **Type hints** : Mypy pour vérification types
- **Documentation** : Docstrings complètes
- **Performance** : Monitoring mémoire intégré

### Contribution
1. Fork le repository
2. Créer une branche feature (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Tests et développement TDD
4. Commit avec messages descriptifs
5. Push et créer Pull Request

## 📄 Licence

MIT License - Voir fichier `LICENSE` pour détails.

## ⚠️ Avertissements

### Contenu Adulte
Ce jeu est strictement réservé aux personnes majeures et contient du contenu sexuellement explicite. Il s'agit d'une œuvre de fiction interactive destinée au divertissement adulte.

### Responsabilité
Les développeurs ne sont pas responsables de l'utilisation inappropriée de ce logiciel. L'utilisateur est seul responsable du respect des lois locales concernant le contenu adulte.

### Support
Pour questions techniques ou bugs : [GitHub Issues](https://github.com/toutounnisgame-netizen/ara-ara/issues)

---

**🎮 Bon jeu ! (Réservé aux adultes)**
