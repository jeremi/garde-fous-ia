# Consignes pour les agents de code

Registre fictif des pêcheurs artisans de Solmara. Python, FastAPI, SQLite, `uv`.

## Avant d'écrire du code
- Écris d'abord les critères d'acceptation de la tâche et fais-les valider.
- N'invente aucune règle métier : liste les questions ouvertes dans la description de la PR.

## Règles et tests
- Chaque règle métier ou d'accès a une ligne dans `docs/regles.md` et un test de refus `test_refus_...`.
- Signale en tête de PR toute modification de `app/regles.py`, `app/public.py`, `app/db.py` ou `.semgrep/`.
- `/public/pecheurs` ne renvoie que le nom et le port. Jamais le téléphone.

## Avant de dire « terminé »
- Lance `uv run pytest -q`, `uv run ruff check .`, `uv run python scripts/verifier_regles.py`
  et `uvx semgrep scan --config .semgrep/regles.yml --error`.
- Ne déclare jamais « terminé » sans la commande et son résultat, collés tels quels.

## Données et secrets
- Jamais de données réelles : noms, téléphones et immatriculations sont fictifs.
- Aucun secret dans le code, les tests, les journaux ou les messages. Ne lis pas les fichiers `.env`.
