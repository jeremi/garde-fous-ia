"""Registre fictif des pêcheurs artisans de Solmara (ports d'Anvela et de Corvala)."""

import os
import sqlite3
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Request
from pydantic import BaseModel

from app import db, public
from app.regles import Utilisateur, peut_valider, peut_voir, utilisateur_courant

router = APIRouter()


class NouvelleInscription(BaseModel):
    nom: str
    telephone: str
    port: Literal["Anvela", "Corvala"]
    immatriculation: str


def lire(request: Request, utilisateur: Utilisateur, id_: int) -> sqlite3.Row:
    ligne = request.app.state.db.execute(
        "SELECT * FROM inscription WHERE id = ?", (id_,)
    ).fetchone()
    # Hors de son port : même réponse qu'une inscription inexistante.
    if ligne is None or not peut_voir(utilisateur, ligne["port"]):
        raise HTTPException(status_code=404, detail="Inscription introuvable")
    return ligne


@router.post("/inscriptions", status_code=201)
def inscrire(
    request: Request,
    donnees: NouvelleInscription,
    utilisateur: Annotated[Utilisateur, Depends(utilisateur_courant)],
) -> dict:
    if not peut_voir(utilisateur, donnees.port):
        raise HTTPException(status_code=403, detail="Port hors de votre périmètre")
    try:
        with request.app.state.db as connexion:
            curseur = connexion.execute(
                "INSERT INTO inscription (nom, telephone, port, immatriculation, propose_par)"
                " VALUES (?, ?, ?, ?, ?)",
                (
                    donnees.nom,
                    donnees.telephone,
                    donnees.port,
                    donnees.immatriculation,
                    utilisateur.identifiant,
                ),
            )
    except sqlite3.IntegrityError as erreur:
        raise HTTPException(status_code=409, detail="Bateau déjà inscrit") from erreur
    return dict(lire(request, utilisateur, curseur.lastrowid))


@router.get("/inscriptions/{id_}")
def consulter(
    request: Request,
    id_: int,
    utilisateur: Annotated[Utilisateur, Depends(utilisateur_courant)],
) -> dict:
    return dict(lire(request, utilisateur, id_))


@router.post("/inscriptions/{id_}/validation")
def valider(
    request: Request,
    id_: int,
    utilisateur: Annotated[Utilisateur, Depends(utilisateur_courant)],
) -> dict:
    ligne = lire(request, utilisateur, id_)
    if not peut_valider(utilisateur, ligne["propose_par"]):
        raise HTTPException(status_code=403, detail="Validation refusée")
    with request.app.state.db as connexion:
        connexion.execute("UPDATE inscription SET statut = 'validee' WHERE id = ?", (id_,))
    return dict(lire(request, utilisateur, id_))


def creer_app(chemin_db: str = ":memory:") -> FastAPI:
    app = FastAPI(title="Registre des pêcheurs de Solmara (fictif)")
    app.state.db = db.connecter(chemin_db)
    app.include_router(public.router)
    app.include_router(router)
    return app


app = creer_app(os.environ.get("REGISTRE_DB", ":memory:"))
