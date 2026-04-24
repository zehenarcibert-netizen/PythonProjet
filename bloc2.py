
# ─── 1. LISTES ────────────────────────────────────────────────────────────────
print("=" * 55)
print("1. LISTES")
print("=" * 55)

salles = ["Amphi A", "Salle B101", "TD C01", "Labo Info", "Salle Conf"]
print("Salles disponibles :", salles)

# Ajout / suppression
salles.append("Salle B102")
salles.remove("Salle Conf")
print("Après modification :", salles)

# Compréhension de liste (list comprehension)
salles_td = [s for s in salles if "TD" in s or "Labo" in s]
print("Salles TD/Labo :", salles_td)

# Tri
salles.sort()
print("Triées :", salles)

# ─── 2. TUPLES ────────────────────────────────────────────────────────────────
print("\n" + "=" * 55)
print("2. TUPLES (immuables)")
print("=" * 55)

# Un créneau horaire = tuple (immuable car un horaire fixé ne change pas)
creneau1 = ("08:00", "10:00")
creneau2 = ("10:00", "12:00")
creneau3 = ("14:00", "16:00")

creneaux = [creneau1, creneau2, creneau3]
print("Créneaux disponibles :")
for i, (debut, fin) in enumerate(creneaux, 1):
    print(f"  Créneau {i} : {debut} → {fin}")

# Déballage (unpacking)
debut_matin, fin_matin = creneau1
print(f"Matin : début={debut_matin}, fin={fin_matin}")

# ─── 3. DICTIONNAIRES ─────────────────────────────────────────────────────────
print("\n" + "=" * 55)
print("3. DICTIONNAIRES")
print("=" * 55)

# Dictionnaire simple
salle_info = {
    "numero": "B101",
    "nom": "Salle B101",
    "capacite": 40,
    "localisation": "Bâtiment B",
    "disponible": True,
    "equipements": ["Projecteur", "Tableau blanc"]
}
print("Info salle :", salle_info)
print("Capacité :", salle_info["capacite"])
print("Équipements :", salle_info.get("equipements", []))

# Dictionnaire imbriqué
planning = {
    "22/04/2026": {
        "Amphi A": [("08:00", "10:00", "Prof. Adjonou", "Cours Algo"),
                    ("14:00", "16:00", "Prof. Bello",   "Cours Réseau")],
        "Salle B101": [("10:00", "12:00", "Prof. Dossou", "TD Python")],
    },
    "23/04/2026": {
        "Amphi A": [("08:00", "10:00", "Prof. Adjonou", "Cours BD")],
    }
}

print("\nPlanning complet :")
for jour, salles_dict in planning.items():
    print(f"\n  📅 {jour}")
    for salle, reservations in salles_dict.items():
        print(f"    🏫 {salle}")
        for debut, fin, resp, motif in reservations:
            print(f"       {debut}→{fin} | {resp} | {motif}")

# Méthodes utiles
print("\nJours planifiés :", list(planning.keys()))
print("Nombre de jours :", len(planning))

# ─── 4. SETS (ensembles) ──────────────────────────────────────────────────────
print("\n" + "=" * 55)
print("4. SETS (ensembles — pas de doublons)")
print("=" * 55)

equipements_salle_A = {"Projecteur", "Tableau blanc", "Micro"}
equipements_salle_B = {"Projecteur", "Ordinateur", "Tableau interactif"}

# Opérations ensemblistes
communs = equipements_salle_A & equipements_salle_B
uniquesA = equipements_salle_A - equipements_salle_B
tous = equipements_salle_A | equipements_salle_B

print("Équipements communs   :", communs)
print("Uniquement en salle A :", uniquesA)
print("Tous les équipements  :", tous)

# Vérification rapide
print("Salle A a un micro ?", "Micro" in equipements_salle_A)

# ─── 5. COMPRÉHENSIONS AVANCÉES ───────────────────────────────────────────────
print("\n" + "=" * 55)
print("5. COMPRÉHENSIONS AVANCÉES")
print("=" * 55)

# Dictionnaire des taux d'occupation
reservations_par_salle = {
    "Amphi A":    15,
    "Salle B101": 8,
    "TD C01":     12,
    "Labo Info":  5,
}
total = sum(reservations_par_salle.values())

taux_occupation = {
    salle: round(nb / total * 100, 1)
    for salle, nb in reservations_par_salle.items()
}
print("Taux d'occupation :", taux_occupation)

# Filtrage : salles avec plus de 10 réservations
tres_utilisees = {s: nb for s, nb in reservations_par_salle.items() if nb > 10}
print("Salles très utilisées :", tres_utilisees)

# Salle la plus utilisée
salle_top = max(reservations_par_salle, key=reservations_par_salle.get)
print("Top salle :", salle_top, "—", reservations_par_salle[salle_top], "réservations")

# ─── 6. RÉSUMÉ POUR LE BLOC 2 ─────────────────────────────────────────────────
print("\n" + "=" * 55)
print("RÉSUMÉ : Structures utilisées dans le Projet 7")
print("=" * 55)
print("  liste  → salles, réservations, équipements")
print("  tuple  → créneaux horaires (immuables)")
print("  dict   → planning, infos salle, stats")
print("  set    → équipements (pas de doublons)")
print("  compréhension → filtres, taux d'occupation")

