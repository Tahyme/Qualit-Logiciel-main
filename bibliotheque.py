class Bibliotheque:
    def __init__(self, notification_service=None):
        self.livres = {}
        self.utilisateurs = set()
        self.emprunts = {}
        self.notification_service = notification_service

    def ajouter_livre(self, isbn, titre, auteur=None):
        self.livres[isbn] = {"titre": titre, "auteur": auteur}

    def inscrire_utilisateur(self, utilisateur_id):
        self.utilisateurs.add(utilisateur_id)

    def emprunter_livre(self, utilisateur_id, isbn):
        if isbn not in self.livres:
            raise ValueError("Livre non trouvé")
        if isbn in self.emprunts:
            raise ValueError("Livre déjà emprunté")
        if utilisateur_id not in self.utilisateurs:
            raise ValueError("Utilisateur non inscrit")
        self.emprunts[isbn] = utilisateur_id
        if self.notification_service:
            self.notification_service.notifier(utilisateur_id, f"Vous avez emprunté {self.livres[isbn]['titre']}")

    def retourner_livre(self, utilisateur_id, isbn):
        if isbn not in self.emprunts:
            raise ValueError("Livre non emprunté")
        if self.emprunts[isbn] != utilisateur_id:
            raise ValueError("Ce livre n'a pas été emprunté par cet utilisateur")
        del self.emprunts[isbn]
        if self.notification_service:
            self.notification_service.notifier(utilisateur_id, f"Vous avez retourné {self.livres[isbn]['titre']}")

    def recherche(self, titre=None, auteur=None, disponible=None):
        resultats = []
        for isbn, details in self.livres.items():
            if titre and titre.lower() not in details["titre"].lower():
                continue
            if auteur and auteur.lower() not in details.get("auteur", "").lower():
                continue
            if disponible is not None:
                if disponible and isbn in self.emprunts:
                    continue
                if not disponible and isbn not in self.emprunts:
                    continue
            resultats.append({"isbn": isbn, "titre": details["titre"], "auteur": details.get("auteur")})
        return resultats

    def recherche(self, titre=None, auteur=None, disponible=None, tri=None):
        resultats = []
        for isbn, details in self.livres.items():
            if titre and titre.lower() not in details["titre"].lower():
                continue
            if auteur and auteur.lower() not in details.get("auteur", "").lower():
                continue
            if disponible is not None:
                if disponible and isbn in self.emprunts:
                    continue
                if not disponible and isbn not in self.emprunts:
                    continue
            resultats.append({"isbn": isbn, "titre": details["titre"], "auteur": details.get("auteur")})

        if tri:
            resultats = sorted(resultats, key=lambda x: x[tri])

        return resultats