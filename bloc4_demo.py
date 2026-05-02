# bloc4_demo.py
# BLOC 4 — Démonstration SQLite uniquement
# Lance avec : python bloc4_demo.py

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.db_manager      import DatabaseManager
from database.salle_dao       import SalleDAO
from database.reservation_dao import ReservationDAO
from models.salle             import Salle
from models.reservation       import Reservation
from datetime import date, time

print("=" * 60)
print("  BLOC 4 — Persistance SQLite")
print("  Universite de Parakou — Projet 7")
print("=" * 60)

# ─── 1. CONNEXION ─────────────────────────────────────────────────────────────
print("\n--- 1. Connexion SQLite ---")
db        = DatabaseManager()
salle_dao = SalleDAO(db)
res_dao   = ReservationDAO(db)

# ─── AFFICHER OÙ EST SAUVEGARDÉ LE FICHIER ────────────────────────────────────
print(f"\n>>> Le fichier SQLite est sauvegarde ici :")
print(f"    {db.db_path}")

# ─── 2. INSERTION SALLES ──────────────────────────────────────────────────────
print("\n--- 2. Insertion des salles ---")
salles = [
    Salle("A001", "Amphi A",    "Batiment Principal", 200, "Amphi"),
    Salle("B101", "Salle B101", "Batiment B",          40, "Cours"),
    Salle("C01",  "TD C01",     "Batiment C",          25, "TD"),
    Salle("INF1", "Labo Info",  "Labo Informatique",   30, "Informatique"),
]
ids = [salle_dao.inserer(s) for s in salles]
print(f"  {len(ids)} salles inserees.")

# ─── 3. LECTURE SALLES ────────────────────────────────────────────────────────
print("\n--- 3. Lecture des salles ---")
for s in salle_dao.get_toutes():
    print(f"  ID={s['id']} | {s['numero']} | {s['nom']} | {s['capacite']} places")

# ─── 4. INSERTION RÉSERVATIONS ────────────────────────────────────────────────
print("\n--- 4. Insertion des reservations ---")

class SalleRef:
    def __init__(self, sid, nom):
        self._id = sid; self._nom = nom
    def get_id(self): return self._id
    def get_nom(self): return self._nom

s1 = SalleRef(ids[0], "Amphi A")
s2 = SalleRef(ids[1], "Salle B101")

reservations = [
    Reservation(s1, "Prof. Adjonou", date(2026, 4, 24), time(8,0),  time(10,0), "Cours Algo"),
    Reservation(s1, "Prof. Bello",   date(2026, 4, 24), time(14,0), time(16,0), "Cours Reseau"),
    Reservation(s2, "Prof. Dossou",  date(2026, 4, 25), time(10,0), time(12,0), "TD Python"),
]
for r in reservations:
    res_dao.inserer(r)
print(f"  {len(reservations)} reservations inserees.")

# ─── 5. LECTURE RÉSERVATIONS ──────────────────────────────────────────────────
print("\n--- 5. Lecture des reservations ---")
for r in res_dao.get_toutes():
    print(f"  ID={r['id']} | {r['salle_nom']:<15} | {r['date_res']} | "
          f"{r['heure_debut']}→{r['heure_fin']} | {r['responsable']}")

# ─── 6. MODIFICATION ──────────────────────────────────────────────────────────
print("\n--- 6. Modification reservation ID=1 ---")
res_dao.modifier(1, "2026-04-24", "09:00", "11:00", "Cours Algo modifie")
r = res_dao.get_par_id(1)
print(f"  Nouveau creneau : {r['heure_debut']}→{r['heure_fin']} | {r['motif']}")

# ─── 7. STATISTIQUES ──────────────────────────────────────────────────────────
print("\n--- 7. Statistiques ---")
stats = res_dao.get_statistiques()
print(f"  Total reservations : {stats['total']}")
print(f"  Salle la plus utilisee : {stats['salle_top']}")
for salle, nb in stats["par_salle"].items():
    print(f"    {salle:<20} : {nb} reservation(s)")

# ─── 8. SUPPRESSION ───────────────────────────────────────────────────────────
print("\n--- 8. Suppression reservation ID=3 ---")
res_dao.supprimer(3)
print(f"  Total apres suppression : {res_dao.compter()} reservations")

print("\n" + "=" * 60)
print("  BLOC 4 TERMINE !")
print(f"  Ouvre ce fichier pour voir les donnees :")
print(f"  {db.db_path}")
print("  Utilise DB Browser for SQLite (gratuit)")
print("  ou le plugin Database de PyCharm")
print("=" * 60)

db.fermer()