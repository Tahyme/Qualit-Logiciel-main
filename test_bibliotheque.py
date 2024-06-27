import bibliotheque
from unittest.mock import Mock

def test_ajouter_livre():
    biblio = bibliotheque.Bibliotheque()
    biblio.ajouter_livre("123", "Le Petit Prince")
    assert biblio.livres["123"] == {'auteur': None, 'titre': "Le Petit Prince"}

def test_inscrire_utilisateur():
    biblio = bibliotheque.Bibliotheque()
    biblio.inscrire_utilisateur("user1")
    assert "user1" in biblio.utilisateurs

def test_emprunter_livre():
    biblio = bibliotheque.Bibliotheque()
    biblio.ajouter_livre("123", "Le Petit Prince")
    biblio.inscrire_utilisateur("user1")
    biblio.emprunter_livre("user1", "123")
    assert biblio.emprunts["123"] == "user1"

def test_emprunter_livre_deja_emprunte():
    biblio = bibliotheque.Bibliotheque()
    biblio.ajouter_livre("123", "Le Petit Prince")
    biblio.inscrire_utilisateur("user1")
    biblio.inscrire_utilisateur("user2")
    biblio.emprunter_livre("user1", "123")
    try:
        biblio.emprunter_livre("user2", "123")
    except ValueError as e:
        assert str(e) == "Livre déjà emprunté"

def test_retourner_livre():
    biblio = bibliotheque.Bibliotheque()
    biblio.ajouter_livre("123", "Le Petit Prince")
    biblio.inscrire_utilisateur("user1")
    biblio.emprunter_livre("user1", "123")
    biblio.retourner_livre("user1", "123")
    assert "123" not in biblio.emprunts

def test_retourner_livre_non_emprunte():
    biblio = bibliotheque.Bibliotheque()
    biblio.ajouter_livre("123", "Le Petit Prince")
    biblio.inscrire_utilisateur("user1")
    try:
        biblio.retourner_livre("user1", "123")
    except ValueError as e:
        assert str(e) == "Livre non emprunté"

def test_emprunter_livre_utilisateur_non_inscrit():
    biblio = bibliotheque.Bibliotheque()
    biblio.ajouter_livre("123", "Le Petit Prince")
    try:
        biblio.emprunter_livre("user1", "123")
    except ValueError as e:
        assert str(e) == "Utilisateur non inscrit"

def test_emprunter_livre_non_disponible():
    biblio = bibliotheque.Bibliotheque()
    biblio.inscrire_utilisateur("user1")
    try:
        biblio.emprunter_livre("user1", "123")
    except ValueError as e:
        assert str(e) == "Livre non trouvé"

def test_notification_emprunt():
    notification_service = Mock()
    biblio = bibliotheque.Bibliotheque(notification_service)
    biblio.ajouter_livre("123", "Le Petit Prince")
    biblio.inscrire_utilisateur("user1")
    biblio.emprunter_livre("user1", "123")
    notification_service.notifier.assert_called_with("user1", "Vous avez emprunté Le Petit Prince")

def test_notification_retour():
    notification_service = Mock()
    biblio = bibliotheque.Bibliotheque(notification_service)
    biblio.ajouter_livre("123", "Le Petit Prince")
    biblio.inscrire_utilisateur("user1")
    biblio.emprunter_livre("user1", "123")
    biblio.retourner_livre("user1", "123")
    notification_service.notifier.assert_called_with("user1", "Vous avez retourné Le Petit Prince")

def test_recherche_par_titre():
    biblio = bibliotheque.Bibliotheque()
    biblio.ajouter_livre("123", "Le Petit Prince")
    biblio.ajouter_livre("124", "Prince Caspian")
    resultats = biblio.recherche(titre="Prince")
    assert len(resultats) == 2
    assert resultats[0]["isbn"] == "123"
    assert resultats[1]["isbn"] == "124"

def test_recherche_par_auteur():
    biblio = bibliotheque.Bibliotheque()
    biblio.ajouter_livre("123", "Le Petit Prince", "Antoine de Saint-Exupéry")
    biblio.ajouter_livre("124", "Night Flight", "Antoine de Saint-Exupéry")
    resultats = biblio.recherche(auteur="Antoine de Saint-Exupéry")
    assert len(resultats) == 2
    assert resultats[0]["isbn"] == "123"
    assert resultats[1]["isbn"] == "124"

def test_recherche_disponible():
    biblio = bibliotheque.Bibliotheque()
    biblio.ajouter_livre("123", "Le Petit Prince")
    biblio.ajouter_livre("124", "Prince Caspian")
    biblio.inscrire_utilisateur("user1")
    biblio.emprunter_livre("user1", "123")
    resultats = biblio.recherche(disponible=True)
    assert len(resultats) == 1
    assert resultats[0]["isbn"] == "124"

def test_tri_par_titre():
    biblio = bibliotheque.Bibliotheque()
    biblio.ajouter_livre("123", "Le Petit Prince")
    biblio.ajouter_livre("124", "Prince Caspian")
    biblio.ajouter_livre("125", "A Tale of Two Cities")
    resultats = biblio.recherche(tri="titre")
    assert len(resultats) == 3
    assert resultats[0]["isbn"] == "125"
    assert resultats[1]["isbn"] == "123"
    assert resultats[2]["isbn"] == "124"

def test_tri_par_auteur():
    biblio = bibliotheque.Bibliotheque()
    biblio.ajouter_livre("123", "Le Petit Prince", "Antoine de Saint-Exupéry")
    biblio.ajouter_livre("124", "Night Flight", "Rntoine de Saint-Exupéry")
    biblio.ajouter_livre("125", "A Tale of Two Cities", "Charles Dickens")
    resultats = biblio.recherche(tri="auteur")
    assert len(resultats) == 3
    assert resultats[0]["isbn"] == "123"
    assert resultats[1]["isbn"] == "125"
    assert resultats[2]["isbn"] == "124"

def test_filtrage_et_tri():
    biblio = bibliotheque.Bibliotheque()
    biblio.ajouter_livre("123", "Le Petit Prince", "Antoine de Saint-Exupéry")
    biblio.ajouter_livre("124", "Night Flight", "Antoine de Saint-Exupéry")
    biblio.ajouter_livre("125", "A Tale of Two Cities", "Charles Dickens")
    biblio.inscrire_utilisateur("user1")
    biblio.emprunter_livre("user1", "124")
    resultats = biblio.recherche(auteur="Antoine", disponible=True, tri="titre")
    assert len(resultats) == 1
    assert resultats[0]["isbn"] == "123"
