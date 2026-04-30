# bloc4_demo.py
# BLOC 4 — Démonstration complète : SQLite + JSON + CSV
# A placer à la racine du projet et exécuter directement

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.db_manager    import DatabaseManager
from database.salle_dao     import SalleDAO
from database.reservation_dao import ReservationDAO
from database.export_service  import ExportService

# Import des modèles existants
from models.salle       import Salle
from models.reservation import Reservation
from datetime import date, time

print("=" * 55)
print("  BLOC 4 — Persistance SQLite + JSON + CSV")
print("=" * 55)

# ─── 1. CONNEXION BASE DE DONNÉES ─────────────────────────────────────────────
print("\n--- 1. Connexion SQLite ---")
db = DatabaseManager()
salle_dao = SalleDAO(db)
res_dao   = ReservationDAO(db)
export    = ExportService(res_dao, salle_dao)

# ─── 2. INSÉRER DES SALLES ────────────────────────────────────────────────────
print("\n--- 2. Insertion des salles ---")
salles_obj = [
    Salle("A001", "Amphi A",    "Batiment Principal", 200, "Amphi"),
    Salle("B101", "Salle B101", "Batiment B",         40,  "Cours"),
    Salle("C01",  "TD C01",     "Batiment C",         25,  "TD"),
    Salle("INF1", "Labo Info",  "Labo Informatique",  30,  "Informatique"),
]
ids_salles = []
for s in salles_obj:
    sid = salle_dao.inserer(s)
    ids_salles.append(sid)

# ─── 3. LIRE LES SALLES ───────────────────────────────────────────────────────
print("\n--- 3. Lecture des salles ---")
salles_db = salle_dao.get_toutes()
for s in salles_db:
    print(f"  [{s['id']}] {s['numero']} — {s['nom']} | {s['type_salle']} | {s['capacite']} places")

# ─── 4. INSÉRER DES RÉSERVATIONS ──────────────────────────────────────────────
print("\n--- 4. Insertion des réservations ---")

# On simule des objets salle avec un id
class SalleSimple:
    def __init__(self, sid, nom): self._id = sid; self._nom = nom
    def get_id(self): return self._id
    def get_nom(self): return self._nom

s1 = SalleSimple(ids_salles[0], "Amphi A")
s2 = SalleSimple(ids_salles[1], "Salle B101")

r1 = Reservation(s1, "Prof. Adjonou", date(2026, 4, 24), time(8,0),  time(10,0), "Cours Algo")
r2 = Reservation(s1, "Prof. Bello",   date(2026, 4, 24), time(14,0), time(16,0), "Cours Réseau")
r3 = Reservation(s2, "Prof. Dossou",  date(2026, 4, 25), time(10,0), time(12,0), "TD Python")

for r in [r1, r2, r3]:
    res_dao.inserer(r)

# ─── 5. LIRE LES RÉSERVATIONS ─────────────────────────────────────────────────
print("\n--- 5. Lecture des réservations ---")
for r in res_dao.get_toutes():
    print(f"  [{r['id']}] {r['salle_nom']} | {r['date_res']} | {r['heure_debut']}→{r['heure_fin']} | {r['responsable']}")

# ─── 6. MODIFIER UNE RÉSERVATION ──────────────────────────────────────────────
print("\n--- 6. Modification ---")
res_dao.modifier(1, "2026-04-24", "09:00", "11:00", "Cours Algo (modifié)")
print("  Réservation 1 modifiée : 09:00→11:00")

# ─── 7. STATISTIQUES ──────────────────────────────────────────────────────────
print("\n--- 7. Statistiques ---")
stats = res_dao.get_statistiques()
print(f"  Total réservations : {stats['total']}")
print(f"  Salle la plus utilisée : {stats['salle_top']} ({stats['salle_top_nb']} fois)")

# ─── 8. EXPORT JSON ───────────────────────────────────────────────────────────
print("\n--- 8. Export JSON ---")
export.exporter_json("export_reservations.json")

# ─── 9. EXPORT CSV ────────────────────────────────────────────────────────────
print("\n--- 9. Export CSV ---")
export.exporter_csv("rapport_reservations.csv")
export.exporter_rapport_stats("rapport_stats.csv")

# ─── 10. SUPPRIMER ────────────────────────────────────────────────────────────
print("\n--- 10. Suppression ---")
res_dao.supprimer(3)
print("  Réservation 3 supprimée.")

print("\n" + "=" * 55)
print("  Bloc 4 terminé ! Fichiers créés :")
print("  - reservation_up.db  (base SQLite)")
print("  - export_reservations.json")
print("  - rapport_reservations.csv")
print("  - rapport_stats.csv")
print("=" * 55)

db.fermer()
