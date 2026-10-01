"""Base SQLite (bibliothèque standard, pas d'ORM)."""

import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS inscription (
    id INTEGER PRIMARY KEY,
    nom TEXT NOT NULL,
    telephone TEXT NOT NULL,
    port TEXT NOT NULL CHECK (port IN ('Anvela', 'Corvala')),
    immatriculation TEXT NOT NULL UNIQUE,
    statut TEXT NOT NULL DEFAULT 'proposee' CHECK (statut IN ('proposee', 'validee')),
    propose_par TEXT NOT NULL
);
"""


def connecter(chemin: str) -> sqlite3.Connection:
    connexion = sqlite3.connect(chemin, check_same_thread=False)
    connexion.row_factory = sqlite3.Row
    connexion.executescript(SCHEMA)
    return connexion
