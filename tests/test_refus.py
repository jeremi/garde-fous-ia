"""Tests de refus : chaque règle de docs/regles.md doit être prouvée ici."""


def test_refus_telephone_dans_la_liste_publique(client, inscrire):
    id_ = inscrire("agent-anvela").json()["id"]
    client.post(f"/inscriptions/{id_}/validation", headers={"X-Utilisateur": "siege"})
    pecheurs = client.get("/public/pecheurs").json()
    assert pecheurs, "la liste publique ne doit pas être vide pour ce test"
    assert all(set(pecheur) == {"nom", "port"} for pecheur in pecheurs)


def test_refus_inscription_non_validee_dans_la_liste_publique(client, inscrire):
    inscrire("agent-anvela")
    assert client.get("/public/pecheurs").json() == []


def test_refus_double_inscription_du_meme_bateau(inscrire):
    assert inscrire("agent-anvela").status_code == 201
    reponse = inscrire("siege", port="Anvela")
    assert reponse.status_code == 409


def test_refus_auto_validation_par_le_siege(client, inscrire):
    id_ = inscrire("siege").json()["id"]
    reponse = client.post(f"/inscriptions/{id_}/validation", headers={"X-Utilisateur": "siege"})
    assert reponse.status_code == 403
    consultee = client.get(f"/inscriptions/{id_}", headers={"X-Utilisateur": "siege"})
    assert consultee.json()["statut"] == "proposee"


def test_refus_validation_par_un_agent_de_port(client, inscrire):
    id_ = inscrire("agent-anvela").json()["id"]
    reponse = client.post(
        f"/inscriptions/{id_}/validation", headers={"X-Utilisateur": "agent-anvela"}
    )
    assert reponse.status_code == 403


def test_refus_lecture_d_un_autre_port_comme_inexistante(client, inscrire):
    id_ = inscrire("agent-corvala", port="Corvala").json()["id"]
    autre_port = client.get(f"/inscriptions/{id_}", headers={"X-Utilisateur": "agent-anvela"})
    inexistante = client.get("/inscriptions/9999", headers={"X-Utilisateur": "agent-anvela"})
    assert autre_port.status_code == 404
    assert autre_port.json() == inexistante.json()


def test_refus_inscription_dans_un_autre_port(inscrire):
    reponse = inscrire("agent-anvela", port="Corvala", immatriculation="PIR-COR-0007")
    assert reponse.status_code == 403


def test_refus_utilisateur_inconnu(client):
    reponse = client.get("/inscriptions/1", headers={"X-Utilisateur": "inconnu"})
    assert reponse.status_code == 401
    assert reponse.json() == {"detail": "Utilisateur inconnu"}
