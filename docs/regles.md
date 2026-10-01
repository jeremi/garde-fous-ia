# Règles du registre et leurs tests de refus

Chaque règle métier ou d'accès a une ligne ici. Une règle sans test de refus n'est pas une règle.
`scripts/verifier_regles.py` échoue si un test cité n'existe pas parmi les tests collectés par pytest.

| Règle | Où elle est bloquée | Test de refus |
|---|---|---|
| Le public ne voit jamais le téléphone | `app/public.py` (nom et port seulement) + règle Semgrep | `test_refus_telephone_dans_la_liste_publique` |
| Le public ne voit que les inscriptions validées | `app/public.py` (requête SQL) | `test_refus_inscription_non_validee_dans_la_liste_publique` |
| Un bateau n'est inscrit qu'une fois | `app/db.py` (`UNIQUE` sur `immatriculation`), réponse 409 | `test_refus_double_inscription_du_meme_bateau` |
| Personne ne valide sa propre proposition | `app/regles.py` `peut_valider`, réponse 403 | `test_refus_auto_validation_par_le_siege` |
| Seul le siège valide | `app/regles.py` `peut_valider`, réponse 403 | `test_refus_validation_par_un_agent_de_port` |
| Un agent ne lit que son port (404, comme une inscription inexistante) | `app/regles.py` `peut_voir` | `test_refus_lecture_d_un_autre_port_comme_inexistante` |
| Un agent n'inscrit que dans son port | `app/regles.py` `peut_voir`, réponse 403 | `test_refus_inscription_dans_un_autre_port` |
| Utilisateur inconnu refusé | `app/regles.py` `utilisateur_courant`, réponse 401 | `test_refus_utilisateur_inconnu` |
