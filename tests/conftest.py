import pytest
from fastapi.testclient import TestClient

from app.main import creer_app


@pytest.fixture
def client():
    with TestClient(creer_app(":memory:")) as client:
        yield client


@pytest.fixture
def inscrire(client):
    """Inscrit un pêcheur fictif au nom de l'utilisateur donné."""

    def _inscrire(utilisateur, port="Anvela", immatriculation="PIR-ANV-0123"):
        return client.post(
            "/inscriptions",
            headers={"X-Utilisateur": utilisateur},
            json={
                "nom": "Pêcheur Fictif",
                "telephone": "+000 00 00 00",
                "port": port,
                "immatriculation": immatriculation,
            },
        )

    return _inscrire
