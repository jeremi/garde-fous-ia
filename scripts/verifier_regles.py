"""Échoue si un test cité dans docs/regles.md n'existe pas parmi les tests collectés par pytest."""

import re
import subprocess
import sys
from pathlib import Path


def tests_cites() -> set[str]:
    texte = Path("docs/regles.md").read_text(encoding="utf-8")
    return set(re.findall(r"`(test_\w+)`", texte))


def tests_collectes() -> set[str]:
    sortie = subprocess.run(
        [sys.executable, "-m", "pytest", "--collect-only", "-q"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    return {ligne.split("::")[-1].split("[")[0] for ligne in sortie.splitlines() if "::" in ligne}


cites = tests_cites()
if not cites:
    sys.exit("ERREUR : aucun test cité dans docs/regles.md")
manquants = sorted(cites - tests_collectes())
if manquants:
    sys.exit("ERREUR : tests cités mais introuvables :\n  " + "\n  ".join(manquants))
print(f"OK : les {len(cites)} tests cités dans docs/regles.md existent.")
