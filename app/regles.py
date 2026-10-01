"""Règles d'accès. Toute modification de ce fichier demande la revue d'un code owner."""

from dataclasses import dataclass

from fastapi import Header, HTTPException


@dataclass(frozen=True)
class Utilisateur:
    identifiant: str
    port: str | None  # None : siège, voit tous les ports
    peut_valider: bool


# DÉMO UNIQUEMENT : utilisateurs fictifs et fixes, choisis par l'en-tête X-Utilisateur.
# Ce n'est pas une authentification. Ne jamais utiliser ce mécanisme en production.
UTILISATEURS_DEMO = {
    "agent-anvela": Utilisateur("agent-anvela", "Anvela", peut_valider=False),
    "agent-corvala": Utilisateur("agent-corvala", "Corvala", peut_valider=False),
    "siege": Utilisateur("siege", None, peut_valider=True),
}


def utilisateur_courant(x_utilisateur: str = Header()) -> Utilisateur:
    utilisateur = UTILISATEURS_DEMO.get(x_utilisateur)
    if utilisateur is None:
        raise HTTPException(status_code=401, detail="Utilisateur inconnu")
    return utilisateur


def peut_voir(utilisateur: Utilisateur, port: str) -> bool:
    return utilisateur.port is None or utilisateur.port == port


def peut_valider(utilisateur: Utilisateur, propose_par: str) -> bool:
    if not utilisateur.peut_valider:
        return False
    if propose_par == utilisateur.identifiant:
        return False  # personne ne valide sa propre proposition
    return True
