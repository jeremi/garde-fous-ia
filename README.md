# Garde-fous pour du code écrit avec un agent IA

Petit projet de départ qui accompagne l'exposé « Coder avec l'IA, livrer des services fiables.
L'IA écrit. Vous signez. » Il montre des garde-fous simples, à copier dans vos propres dépôts.

C'est un projet personnel. Il n'est approuvé ni soutenu par aucune institution.

Le domaine est fictif : un registre des pêcheurs artisans de Solmara, avec deux ports, Anvela et
Corvala. Toutes les données sont inventées.

## Lancer le projet

```bash
uv sync
uv run pytest -q
uv run ruff check .
uvx semgrep@1.178.0 scan --config .semgrep/regles.yml --error --metrics=off
uv run python scripts/verifier_regles.py
uv run mutmut run && uv run mutmut results
osv-scanner scan source --lockfile uv.lock
gitleaks git .
pre-commit install
pre-commit run --all-files
uv run uvicorn app.main:app --reload
```

- Semgrep est épinglé à la même version que la CI et pre-commit.
- `mutmut results` n'affiche rien quand aucun mutant ne survit.
- Si Git utilise un dossier de hooks global (`core.hooksPath`), `pre-commit install` refuse
  de s'installer ; `pre-commit run --all-files` lance quand même les contrôles.
- L'API est servie sur http://127.0.0.1:8000/docs.

**Authentification de démonstration uniquement.** L'utilisateur est choisi par l'en-tête
`X-Utilisateur` (`agent-anvela`, `agent-corvala`, `siege`). Ce n'est pas une authentification :
ne reprenez pas ce mécanisme en production.

## Erreurs de l'agent et garde-fous

| Erreur de l'agent | Fichier | Ce que ça bloque |
|---|---|---|
| 1. A inventé une règle métier que personne n'avait décidée | `AGENTS.md`, `.github/pull_request_template.md` | Rien d'automatique : la PR doit lister « Décisions prises » et « Questions ouvertes », et un humain les relit |
| 2. A rendu le téléphone public sous la pression | `app/public.py`, `.semgrep/regles.yml`, `.github/CODEOWNERS` | Semgrep échoue si `telephone` ou `SELECT *` apparaît dans le module public ; les fichiers d'accès demandent un code owner |
| 3. Tests de refus écrits mais jamais exécutés | `docs/regles.md`, `scripts/verifier_regles.py`, `[tool.mutmut]` dans `pyproject.toml` | La CI échoue si un test cité n'existe pas ; mutmut casse les règles et vérifie qu'un test échoue |
| 4. Le même doublon corrigé deux fois | `app/db.py` (`UNIQUE`), `tests/test_refus.py` | La base refuse un second bateau avec la même immatriculation (409) |
| 5. Le siège pouvait valider sa propre inscription | `app/regles.py` (`peut_valider`, `peut_voir`) | 403 si le validateur a proposé l'inscription ; 404 pour un agent qui lit un autre port |
| Sécurité de base | `pyproject.toml` (ruff `S`, `B`, `T20`), `.pre-commit-config.yaml`, `.github/workflows/ci.yml`, `.github/dependabot.yml` | Code dangereux, `print()` oubliés, secrets commités, dépendances vulnérables |

Les règles et leurs tests de refus sont listés dans [`docs/regles.md`](docs/regles.md).

## Permissions de l'agent

`.claude/settings.json` interdit à Claude Code de lire les fichiers `.env`, de lancer `git push`,
`curl` ou `wget`. C'est une ceinture de sécurité, pas un bac à sable. Les autres agents (Codex,
Cursor, Copilot, etc.) ont des réglages équivalents.

## Réglages GitHub à activer

Ces réglages ne sont pas dans git, il faut les faire à la main.
Settings > Rules > Rulesets > New branch ruleset, cible : la branche par défaut.

- Require a pull request before merging, avec au moins 1 approbation.
- Require review from Code Owners.
- Require approval of the most recent reviewable push.
- Require status checks to pass : `ruff`, `semgrep`, `tests`, `gitleaks`, `dependances`.
- Block force pushes.

Activez aussi Dependabot alerts et, si votre offre le permet, Secret scanning avec push protection.

## Sur GitLab

- `.gitlab-ci.yml` remplace `.github/workflows/` : mêmes commandes (`uv run pytest`, `uvx semgrep`,
  `gitleaks`, `osv-scanner`), un job chacune.
- `CODEOWNERS` fonctionne aussi (à la racine, dans `docs/` ou dans `.gitlab/`).
- Modèles de merge request : `.gitlab/merge_request_templates/Default.md`.
- Approbations : branche protégée, approbation des code owners, « Prevent approval by author »,
  retrait des approbations quand un commit est ajouté. Les règles d'approbation obligatoires et
  l'approbation par les code owners dépendent de l'édition de GitLab (Premium ou Ultimate) :
  vérifiez sur votre instance.

## Équivalents dans d'autres langages

| Rôle | Python (ici) | PHP | Java | JS/TS |
|---|---|---|---|---|
| Analyse statique et sécurité | ruff (`S`, `B`) | PHPStan, Psalm | SpotBugs, Error Prone | ESLint |
| Tests de mutation | mutmut | Infection | PIT | Stryker |
| Échouer s'il n'y a aucun test | `verifier_regles.py` | PHPUnit `failOnEmptyTestSuite` | Surefire `failIfNoTests` | Jest et Vitest échouent par défaut |
| Règles maison | Semgrep | Semgrep | Semgrep | Semgrep |

## Licence

Apache-2.0, voir [`LICENSE`](LICENSE).
