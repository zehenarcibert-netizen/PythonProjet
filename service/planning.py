# services/planning.py
from models.reservation import Reservation
from models.salle import Salle
from models.equipement import Equipement
from datetime import date, time, timedelta

class Planning:
    """Service central : réservations, salles, équipements, rapports."""

    def __init__(self):
        self.__reservations: list = []
        self.__salles: list = []
        self.__equipements: list = []

    # ─── Salles ───────────────────────────────────────────────────────────────
    def ajouter_salle(self, salle):
        self.__salles.append(salle)

    def supprimer_salle(self, salle_id: int) -> bool:
        for i, s in enumerate(self.__salles):
            if s.get_id() == salle_id:
                self.__salles.pop(i)
                return True
        return False

    def get_salles(self):
        return self.__salles

    def get_salle_par_nom(self, nom: str):
        for s in self.__salles:
            if s.get_nom() == nom:
                return s
        return None

    def get_salle_par_id(self, sid: int):
        for s in self.__salles:
            if s.get_id() == sid:
                return s
        return None

    # ─── Équipements ──────────────────────────────────────────────────────────
    def ajouter_equipement(self, eq):
        self.__equipements.append(eq)

    def get_equipements(self):
        return self.__equipements

    # ─── Réservations ─────────────────────────────────────────────────────────
    def ajouter_reservation(self, reservation) -> tuple:
        conflits = self.detecter_conflits(reservation)
        if conflits:
            c = conflits[0]
            msg = (f"Conflit avec reservation #{c.get_id()} "
                   f"({c.get_responsable()}) : "
                   f"{c.get_heure_debut().strftime('%H:%M')} -> "
                   f"{c.get_heure_fin().strftime('%H:%M')}")
            return False, msg
        self.__reservations.append(reservation)
        return True, "Reservation confirmee !"

    def supprimer_reservation(self, res_id: int) -> bool:
        for i, r in enumerate(self.__reservations):
            if r.get_id() == res_id:
                self.__reservations.pop(i)
                return True
        return False

    def get_reservation_par_id(self, rid: int):
        for r in self.__reservations:
            if r.get_id() == rid:
                return r
        return None

    def detecter_conflits(self, nouvelle):
        return [r for r in self.__reservations if nouvelle.est_en_conflit(r)]

    # ─── Filtres ──────────────────────────────────────────────────────────────
    def get_reservations(self):
        return sorted(self.__reservations,
                      key=lambda r: (r.get_date(), r.get_heure_debut()))

    def get_reservations_par_date(self, d):
        return [r for r in self.__reservations if r.get_date() == d]

    def get_reservations_semaine(self, d):
        lundi = d - timedelta(days=d.weekday())
        dimanche = lundi + timedelta(days=6)
        return [r for r in self.__reservations if lundi <= r.get_date() <= dimanche]

    def get_reservations_mois(self, annee: int, mois: int):
        return [r for r in self.__reservations
                if r.get_date().year == annee and r.get_date().month == mois]

    def get_reservations_par_salle(self, salle_id: int):
        return [r for r in self.__reservations if r.get_salle().get_id() == salle_id]

    def get_salles_disponibles(self, date_f, h_debut, h_fin):
        occupees = set()
        for r in self.__reservations:
            if r.get_date() == date_f:
                if not (h_fin <= r.get_heure_debut() or h_debut >= r.get_heure_fin()):
                    occupees.add(r.get_salle().get_id())
        return [s for s in self.__salles if s.get_id() not in occupees]

    def proposer_creneaux(self, salle, date_f):
        """Propose des creneaux libres pour une salle un jour donne."""
        res_jour = [r for r in self.get_reservations_par_salle(salle.get_id())
                    if r.get_date() == date_f]
        res_jour.sort(key=lambda r: r.get_heure_debut())

        creneaux_libres = []
        debut_journee = time(7, 0)
        fin_journee   = time(20, 0)
        curseur = debut_journee

        for r in res_jour:
            if curseur < r.get_heure_debut():
                creneaux_libres.append((curseur, r.get_heure_debut()))
            curseur = r.get_heure_fin()

        if curseur < fin_journee:
            creneaux_libres.append((curseur, fin_journee))

        return creneaux_libres

    # ─── Statistiques ─────────────────────────────────────────────────────────
    def get_statistiques(self) -> dict:
        total = len(self.__reservations)
        compteur = {}
        for r in self.__reservations:
            nom = r.get_salle().get_nom()
            compteur[nom] = compteur.get(nom, 0) + 1

        taux = {}
        for s in self.__salles:
            nb = compteur.get(s.get_nom(), 0)
            taux[s.get_nom()] = round((nb / total * 100) if total > 0 else 0, 1)

        return {
            "total_reservations": total,
            "total_salles": len(self.__salles),
            "salle_plus_utilisee": max(compteur, key=compteur.get) if compteur else "—",
            "taux_occupation": taux,
            "compteur_par_salle": compteur,
        }

