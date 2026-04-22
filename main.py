# main.py — Point d'entree du Projet 7
from models.salle import Salle
from models.equipement import Equipement
from services.planning import Planning
from services.auth import AuthService
from services.notification import NotificationService
from gui.login import LoginWindow
from gui.app import App


def initialiser_donnees(planning: Planning):
    """Salles et equipements de demonstration."""
    # Equipements
    proj1 = Equipement("Projecteur-A01", "Amphi A", "Projecteur", "Epson")
    proj2 = Equipement("Projecteur-B01", "Bat.B", "Projecteur", "BenQ")
    pc1   = Equipement("PC-Info-01", "Labo Info", "Ordinateur", "Dell")
    micro = Equipement("Micro-Conf", "Salle Conf", "Microphone", "Shure")
    tab   = Equipement("TBI-C01", "Bat.C", "Tableau interactif", "Promethean")

    for eq in [proj1, proj2, pc1, micro, tab]:
        planning.ajouter_equipement(eq)

    # Salles
    salles_data = [
        ("A001", "Amphi A",    "Batiment Principal", 200, "Amphi",       [proj1]),
        ("B101", "Salle B101", "Batiment B",         40,  "Cours",       [proj2]),
        ("B102", "Salle B102", "Batiment B",         40,  "Cours",       []),
        ("C01",  "TD C01",     "Batiment C",         25,  "TD",          [tab]),
        ("C02",  "TD C02",     "Batiment C",         25,  "TD",          []),
        ("INF1", "Labo Info",  "Labo Informatique",  30,  "Informatique",[pc1]),
        ("ADM1", "Salle Conf", "Administration",     20,  "Reunion",     [micro]),
    ]
    for numero, nom, loc, cap, type_s, equips in salles_data:
        s = Salle(numero, nom, loc, cap, type_s)
        for eq in equips:
            s.ajouter_equipement(eq)
        planning.ajouter_salle(s)


def main():
    planning = Planning()
    auth     = AuthService()
    notif    = NotificationService()

    initialiser_donnees(planning)

    # Fenetre de connexion
    login = LoginWindow(auth)
    login.mainloop()

    # Si connexion reussie, ouvrir l'appli principale
    if auth.est_connecte():
        app = App(planning, auth, notif)
        app.mainloop()


if __name__ == "__main__":
    main()

