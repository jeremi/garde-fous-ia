"""Route publique, sans authentification. Elle ne renvoie que le nom et le port."""

from fastapi import APIRouter, Request
from pydantic import BaseModel

router = APIRouter(prefix="/public")


class PecheurPublic(BaseModel):
    nom: str
    port: str


@router.get("/pecheurs")
def lister_pecheurs(request: Request) -> list[PecheurPublic]:
    lignes = request.app.state.db.execute(
        "SELECT nom, port FROM inscription WHERE statut = 'validee' ORDER BY nom"
    ).fetchall()
    return [PecheurPublic(nom=ligne["nom"], port=ligne["port"]) for ligne in lignes]
