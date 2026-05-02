import sys
import os
sys.path.insert(0, r"C:\Users\USER\PythonProject\PythonProject")

from models.salle       import Salle
from models.equipement  import Equipement
from service.planning     import Planning
from service.auth         import AuthService
from service.notification import NotificationService
from gui.login import LoginWindow
from gui.app   import App

# ── BLOC 4 — SQLite ───────────────────────────────────────────
from database.db_manager      import DatabaseManager
from database.salle_dao       import SalleDAO
from database.reservation_dao import ReservationDAO


def initialiser_donnees(planning, salle_dao):
    proj1 = Equipement("Projecteur-A01", "Amphi A",    "Projecteur",        "Epson")
    proj2 = Equipement("Projecteur-B01", "Bat.B",      "Projecteur",        "BenQ")
    pc1   = Equipement("PC-Info-01",     "Labo Info",  "Ordinateur",        "Dell")
    micro = Equipement("Micro-Conf",     "Salle Conf", "Microphone",        "Shure")
    tab   = Equipement("TBI-C01",        "Bat.C",      "Tableau interactif","Promethean")

    for eq in [proj1, proj2, pc1, micro, tab]:
        planning.ajouter_equipement(eq)

    salles_data = [
        ("A001", "Amphi A",    "Batiment Principal", 200, "Amphi",        [proj1]),
        ("B101", "Salle B101", "Batiment B",          40, "Cours",        [proj2]),
        ("B102", "Salle B102", "Batiment B",          40, "Cours",        []),
        ("C01",  "TD C01",     "Batiment C",          25, "TD",           [tab]),
        ("C02",  "TD C02",     "Batiment C",          25, "TD",           []),
        ("INF1", "Labo Info",  "Labo Informatique",   30, "Informatique", [pc1]),
        ("ADM1", "Salle Conf", "Administration",      20, "Reunion",      [micro]),
    ]
    for numero, nom, loc, cap, type_s, equips in salles_data:
        s = Salle(numero, nom, loc, cap, type_s)
        for eq in equips:
            s.ajouter_equipement(eq)
        planning.ajouter_salle(s)

    # Sauvegarde SQLite si table vide
    if salle_dao.compter() == 0:
        for s in planning.get_salles():
            salle_dao.inserer(s)
        print(f"[SQLite] {len(planning.get_salles())} salles sauvegardees.")
    else:
        print("[SQLite] Salles deja en base.")


def charger_reservations(planning, res_dao):
    from datetime import date, time as dtime
    nb = 0
    for r in res_dao.get_toutes():
        salle = planning.get_salle_par_nom(r["salle_nom"])
        if salle:
            try:
                d  = date.fromisoformat(r["date_res"])
                h1 = dtime(*map(int, r["heure_debut"].split(":")))
                h2 = dtime(*map(int, r["heure_fin"].split(":")))
                from models.reservation import Reservation
                res = Reservation(salle, r["responsable"], d, h1, h2, r["motif"] or "")
                planning.ajouter_reservation(res)
                nb += 1
            except Exception as e:
                print(f"[WARN] {e}")
    print(f"[SQLite] {nb} reservation(s) restauree(s).")


def sauvegarder_et_quitter(app, planning, res_dao, db):
    try:
        conn = db.get_connexion()
        conn.execute("DELETE FROM reservations")
        conn.commit()
        for r in planning.get_reservations():
            res_dao.inserer(r)
        print(f"[SQLite] {len(planning.get_reservations())} reservation(s) sauvegardees.")
    except Exception as e:
        print(f"[ERREUR] {e}")
    finally:
        db.fermer()
        app.destroy()


def main():
    planning = Planning()
    auth     = AuthService()
    notif    = NotificationService()

    # SQLite
    db        = DatabaseManager()
    salle_dao = SalleDAO(db)
    res_dao   = ReservationDAO(db)

    initialiser_donnees(planning, salle_dao)
    charger_reservations(planning, res_dao)

    # ── LOGIN (comme l'ancien qui marchait) ───────────────────
    login = LoginWindow(auth)
    login.mainloop()

    # ── INTERFACE PRINCIPALE ──────────────────────────────────
    if auth.est_connecte():
        app = App(planning, auth, notif, res_dao=res_dao)
        app.protocol(
            "WM_DELETE_WINDOW",
            lambda: sauvegarder_et_quitter(app, planning, res_dao, db)
        )
        app.mainloop()


if __name__ == "__main__":
    main()