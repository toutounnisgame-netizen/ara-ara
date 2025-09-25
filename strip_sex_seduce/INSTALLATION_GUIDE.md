# Guide Installation Correctifs V2.0

## 📋 PRÉREQUIS
- Python 3.8+
- Projet Strip, Sex & Seduce V1.0 installé
- Backup recommandé

## 🔧 INSTALLATION RAPIDE

### Étape 1: Backup
```bash
cp -r strip_sex_seduce strip_sex_seduce_backup
```

### Étape 2: Extraction
```bash
unzip correctifs_v2.0.zip
cd correctifs_v2.0/
```

### Étape 3: Copie écrasement
```bash
# Copier tous fichiers vers projet principal
cp -r * ../strip_sex_seduce/
```

### Étape 4: Test installation
```bash
cd ../strip_sex_seduce/
python main.py
```

## ✅ VALIDATION INSTALLATION

### Tests Performance
- Tour de jeu < 50ms
- Pas de warning "Performance dégradée"
- Stats visibles changent immédiatement

### Tests Gameplay  
- NPC messages adaptation
- Transitions lieux automatiques
- Descriptions vêtements si modifiés
- Dialogues variés selon résistance

### Tests IA
- "Il devient plus patient..." (adaptation)
- Actions différentes selon personnalité
- Escalation progressive visible

## 🚨 DÉPANNAGE

### Problème: Stats ne changent pas
**Solution:** Vérifier `systems/stats_system.py` copié

### Problème: Performance toujours lente
**Solution:** Vérifier `systems/dialogue_system.py` copié

### Problème: Pas escalation automatique  
**Solution:** Vérifier `core/game_session_escalation_fixes.py` intégré

### Problème: Erreurs import
**Solution:** Restart interpreter Python

## 📞 SUPPORT TECHNIQUE

En cas problème persistant:
1. Vérifier tous fichiers listés copiés
2. Comparer tailles fichiers avec versions backup
3. Check logs Python pour erreurs spécifiques
