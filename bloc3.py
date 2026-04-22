
print("=" * 60)
print("  BLOC 3 — Concepts POO du Projet 7")
print("=" * 60)

# ─── 1. CLASSE & ENCAPSULATION ────────────────────────────────────────────────
print("\n--- 1. CLASSE & ENCAPSULATION ---")

from models.ressource import Ressource
from models.salle import Salle
from models.equipement import Equipement
from models.utilisateur import Utilisateur

# Attributs privés (__ = encapsulé, accès via getters/setters)
u = Utilisateur("Adjonou", "Kofi", "kofi@up.bj", "mdp123", "enseignant")
print(f"Utilisateur : {u.get_nom_complet()}")
print(f"Rôle        : {u.get_role()}")
print(f"Peut gérer salles ? {u.peut_gerer_salles()}")
# u.__nom  ← INTERDIT (attribut privé) — encapsulation respectée

# ─── 2. HÉRITAGE ──────────────────────────────────────────────────────────────
print("\n--- 2. HÉRITAGE ---")

# Hiérarchie : Ressource ← Salle, Equipement, Projecteur
proj = Equipement("Projecteur-01", "Amphi A", "Projecteur", "Epson")
salle = Salle("B101", "Salle B101", "Bâtiment B", 40, "Cours")
salle.ajouter_equipement(proj)

print(f"Salle    : {salle.get_info()}")
print(f"Projecteur: {proj.get_info()}")

# Vérification d'héritage
print(f"Salle est une Ressource ? {isinstance(salle, Ressource)}")
print(f"Projecteur est une Ressource ? {isinstance(proj, Ressource)}")

# ─── 3. POLYMORPHISME ─────────────────────────────────────────────────────────
print("\n--- 3. POLYMORPHISME ---")

# get_info() est défini dans Ressource et REDÉFINi dans Salle et Equipement
ressources = [
    Salle("A001", "Amphi A", "Bat.Principal", 200, "Amphi"),
    Equipement("Micro-01", "Salle Conf", "Microphone", "Shure"),
    Equipement("PC-01", "Labo", "Ordinateur", "Dell"),
]

print("Affichage polymorphe (même appel, résultats différents) :")
for r in ressources:
    print(f"  {r.get_info()}")   # Appel identique, comportement différent !

# ─── 4. MODULARITÉ ────────────────────────────────────────────────────────────
print("\n--- 4. MODULARITÉ ---")
print("Structure modulaire du projet :")
modules = {
    "models/ressource.py":    "Classe mère — encapsulation, getters/setters",
    "models/salle.py":        "Hérite Ressource — +capacité, équipements",
    "models/equipement.py":   "Hérite Ressource — +type, marque",
    "models/reservation.py":  "Logique de conflits horaires",
    "models/utilisateur.py":  "Authentification, rôles",
    "services/planning.py":   "Orchestration — CRUD + algorithmes",
    "services/auth.py":       "Service d'authentification",
    "services/notification.py":"Système de notifications",
    "gui/login.py":           "Interface de connexion",
    "gui/app.py":             "Interface principale (6 onglets)",
    "main.py":                "Point d'entrée",
}
for fichier, role in modules.items():
    print(f"  {fichier:<30} → {role}")

# ─── 5. ALGORITHME DE DÉTECTION DE CONFLITS ───────────────────────────────────
print("\n--- 5. ALGORITHME CLEF : Détection de conflits ---")

from models.reservation import Reservation
from datetime import date, time

s = Salle("T01", "Salle Test", "Bat.A", 30, "TD")
d = date(2026, 4, 22)

r1 = Reservation(s, "Prof. A", d, time(8, 0), time(10, 0), "Cours")
r2 = Reservation(s, "Prof. B", d, time(9, 0), time(11, 0), "TD")   # conflit!
r3 = Reservation(s, "Prof. C", d, time(10, 0), time(12, 0), "TP")  # pas de conflit

print(f"R1 : 08:00→10:00")
print(f"R2 : 09:00→11:00  — conflit avec R1 ? {r1.est_en_conflit(r2)}")  # True
print(f"R3 : 10:00→12:00  — conflit avec R1 ? {r1.est_en_conflit(r3)}")  # False

print("\nFormule : conflit = meme_salle ET meme_date ET chevauchement_horaire")
print("Chevauchement = NOT (fin1 <= debut2 OR debut1 >= fin2)")

print("\n" + "=" * 60)
print("  RÉSUMÉ POO — Projet 7")
print("=" * 60)
concepts = [
    ("Classe",          "Ressource, Salle, Reservation, Utilisateur..."),
    ("Encapsulation",   "__id, __nom, __mot_de_passe + getters/setters"),
    ("Héritage",        "Salle(Ressource), Equipement(Ressource)"),
    ("Polymorphisme",   "get_info() redéfinie dans chaque sous-classe"),
    ("Modularité",      "1 classe = 1 fichier, organisés en packages"),
    ("Attribut classe", "Ressource._compteur_id, Reservation._compteur"),
]
for concept, exemple in concepts:
    print(f"  {concept:<20} : {exemple}")

