"""Tests d'acceptation : ce qui doit marcher."""


def test_agent_inscrit_un_pecheur_de_son_port(inscrire):
    reponse = inscrire("agent-anvela")
    assert reponse.status_code == 201
    assert reponse.json()["statut"] == "proposee"
    assert reponse.json()["propose_par"] == "agent-anvela"


def test_agent_consulte_une_inscription_de_son_port(client, inscrire):
    id_ = inscrire("agent-anvela").json()["id"]
    reponse = client.get(f"/inscriptions/{id_}", headers={"X-Utilisateur": "agent-anvela"})
    assert reponse.status_code == 200
    assert reponse.json()["telephone"] == "+000 00 00 00"


def test_siege_valide_une_proposition_d_un_agent(client, inscrire):
    id_ = inscrire("agent-corvala", port="Corvala").json()["id"]
    reponse = client.post(f"/inscriptions/{id_}/validation", headers={"X-Utilisateur": "siege"})
    assert reponse.status_code == 200
    assert reponse.json()["statut"] == "validee"


def test_public_voit_nom_et_port_des_inscriptions_validees(client, inscrire):
    id_ = inscrire("agent-anvela").json()["id"]
    client.post(f"/inscriptions/{id_}/validation", headers={"X-Utilisateur": "siege"})
    reponse = client.get("/public/pecheurs")
    assert reponse.status_code == 200
    assert reponse.json() == [{"nom": "Pêcheur Fictif", "port": "Anvela"}]
