# Architecture Technique

## Vue d'ensemble ECS

Strip, Sex & Seduce utilise une architecture Entity-Component-System stricte:

- **Entities**: Conteneurs d'ID (Player, NPC, Environment, GameState)
- **Components**: Données pures (Stats, Clothing, Dialogue, Personality)  
- **Systems**: Logique métier (StatsSystem, AISystem, ClothingSystem, etc.)

## Flux de données

```
Input → Systems → Components → Entities → Output
```

## Performance

- <5MB RAM total
- <50ms temps de réponse
- Memory-safe avec nettoyage automatique
- Cache intelligent pour dialogues
