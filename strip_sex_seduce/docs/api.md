# Documentation API

## Core ECS

### Entity
```python
entity = Entity("my_id")
entity.add_component(component)
comp = entity.get_component_of_type(ComponentClass)
```

### Component
```python
class MyComponent(Component):
    def __init__(self):
        super().__init__()
        self.data = "value"
```

### System
```python
class MySystem(System):
    def update(self, entities, delta_time=0.0, **kwargs):
        # Logique système
        pass
```

## Components principaux

### StatsComponent
- `volonte`: Résistance (0-100)
- `excitation`: Arousal (0-100)  
- `apply_modifier(stat, value)`: Modifie stat

### ClothingComponent
- `pieces`: Dict détaillé vêtements
- `get_exposure_level()`: Niveau exposition
- `modify_piece()`: Modifie vêtement
