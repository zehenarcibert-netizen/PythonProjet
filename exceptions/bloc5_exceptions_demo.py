# bloc5 exception_demo.py
# Montre comment utiliser try/except avec les exceptions personnalisées
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from  exceptions.exceptions_projet import (
ConflitReservationError, HoraireInvalideError,
SalleIntrouvableError,AuthentificationError, PermissionRefuseeError,
CapaciteIndisponibleError)

print("=" * 55)
print("Gestion des Exceptions")
print("=" * 55)

#----------Exception simple------------
print("\n___1. try / except simple ------")
try:
    heure_debut = "08:00"
    heure_fin = "07:00" # excption car fin avant début
    if heure_fin <= heure_debut:
        raise HoraireInvalideError()
except HoraireInvalideError as e:
    print(f" [Error Horaire] {e}")

#------exception sallle introuvable-------
print("\n--2. Salle introuvable ---")
def chercher_salle(nom: str, salles: list):
    for s in salles:
        if s == nom:
            return s
        raise SalleIntrouvableError(nom)
try:
    salles_dispo = ["Amphi A", "salle B101", "TD C01"]
    salle=chercher_salle("Salle XYZ", salles_dispo)
except SalleIntrouvableError as e:
    print(f" [Error Horaire] {e}")

#------Excption conflit-------------
print("\n--3. Conflit de reservations ------ ")
def resever(salle, debut, fin, reservations_existantes):
    for r in reservations_existantes:
        if r[salle] == salle:
            if not (fin <= r["debut"] or debut >= r["fin"]):
                raise ConflitReservationError(
                    f"conflit avec la réservation de {r['responsable']}"
                    f"({r['debut']}->{r['fin']})"
                )
    return True
try:
    reservations= [
        {
            "salle": "Amphi A",
            "debut": "08:00",
            "fin": "10:00",
            "responsable": "prof A",
        }
    ]
    resever("Amphi A", "09:00", "11:00", reservations)
except ConflitReservationError as e:
    print(f" [Conflit] {e}")

#---------excption d'authentification----------
print("\n--4. Authentification ------ ")
def connecter(email, mbp):
    comptes = {"admin@up.bj", "admin123"}
    if email not in comptes or comptes[email] != mbp:
        raise AuthentificationError()
    return True
try:
    connecter("admin@up.bj", "mauvais_mbp")
except AuthentificationError as e:
    print(f" [Authentification échouer ] {e}")

#-------exception permission-------
print("\n--5. Permission ------ ")
def supprime_utilisateur(role_actuel):
    if role_actuel != "administrateur":
        raise PermissionRefuseeError(role_actuel, "supprime utilisateur")
    return True
try:
    supprime_utilisateur("enseignant")
except PermissionRefuseeError as e:
    print(f" [Permission Refusee] {e}")

#------capaciter insuffisant----------
print("\n--6. Capacite ------ ")
try:
    capacite_salle = 150
    nb_personnes = 2000
    if nb_personnes > capacite_salle:
        raise CapaciteIndisponibleError(capacite_salle,nb_personnes)
except CapaciteIndisponibleError as e:
    print(f" [Capacite Indisponible] {e}")

#--------finale-------------
print("\n--7. try / except .else /finally ------ ")
def lire_fichier(chemin):
    try:
        with open(chemin, "r") as f:
            contenu = f.read()
    except FileNotFoundError:
        print(f"[Fichier] Fichier '{chemin}' n'existe pas.")
        contenu = None
    except PermissionError:
        print(f"[Fichier] Permission refusée pour '{chemin}'.")
        contenu = None
    else:
        print(f"[Fichier] lu avec succès {len(contenu)} caratters.")
    finally:
        print(" [finally] Opération termeiée(succès ou échec).")
    return contenu
lire_fichier("fichier_inexistant.txt")

print("\n " +"=" * 55)
print("Résumé des excption utiliser dans ceux projet")
print("=" * 55)
exceptions = [
    ("ConflitReservationError",  "Chevauchement horaire"),
    ("HoraireInvalideError",  "Fin <= Début"),
    ("SalleIntrouvableError",  "Salle inexistante"),
    ("SallaIndisponibleError", "Salle non disponible"),
    ("CapaciteIndisponibleError", "Trop de participant"),
    ("EmailDejaUtiliseError", "email dupliqué"),
    ("AuthentificationError", "Mauvais identifiant"),
    ("PermissionRefuseeError", "Action non autorisée"),
    ("BaseDonnesError", "Errure SQLite"),
    ("EportError", "Echec JSON/csv"),

]
for nom,desc in exceptions:
    print(f" {nom:<30} -> {desc}")