# Guide Développement

## Setup environnement

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows
pip install -e .[dev]
```

## Lancement
```bash
python main.py
# ou
python scripts/run.py
```

## Tests
```bash
python scripts/test.py
# ou
python -m pytest tests/
```

## Architecture TDD
1. Écrire test qui échoue (RED)
2. Code minimal qui passe (GREEN)
3. Refactoring (BLUE)

## Standards code
- PEP 8 avec Black
- Type hints
- Docstrings complètes
- Tests 80%+ coverage
