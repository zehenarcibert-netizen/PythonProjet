# models/reservation.py
from datetime import date, time


class Reservation:
    """Représentation d'une réservation de salle"""

    _compteur = 0

    def __init__(self, salle, responsable: str, date_res: date,
                 heure_debut: time, heure_fin: time, motif: str = ""):

        Reservation._compteur += 1
        self.__id = Reservation._compteur
        self.__salle = salle
        self.__responsable = responsable
        self.__date = date_res
        self.__heure_debut = heure_debut
        self.__heure_fin = heure_fin
        self.__motif = motif

    # ✅ Getters
    def get_id(self):
        return self.__id

    def get_salle(self):
        return self.__salle

    def get_responsable(self):
        return self.__responsable

    def get_date(self):
        return self.__date

    def get_heure_debut(self):
        return self.__heure_debut

    def get_heure_fin(self):
        return self.__heure_fin

    def get_motif(self):
        return self.__motif

    # ✅ Setters
    def set_date(self, v):
        self.__date = v

    def set_heure_debut(self, v):
        self.__heure_debut = v

    def set_heure_fin(self, v):
        self.__heure_fin = v

    def set_motif(self, v):
        self.__motif = v

    # ✅ Vérification de conflit
    def est_en_conflit(self, autre: "Reservation") -> bool:
        # Pas la même salle → pas de conflit
        if self.__salle.get_id() != autre.get_salle().get_id():
            return False

        # Pas la même date → pas de conflit
        if self.__date != autre.get_date():
            return False

        # Vérifier chevauchement des heures
        return not (
                self.__heure_fin <= autre.get_heure_debut() or
                self.__heure_debut >= autre.get_heure_fin()
        )

    def __str__(self):
        return (
            f"Réservation #{self.__id}\n"
            f"| Salle: {self.__salle.get_nom()} |\n"
            f"| Date: {self.__date.strftime('%d/%m/%Y')} |\n"
            f"| Heure: {self.__heure_debut.strftime('%H:%M')} -> {self.__heure_fin.strftime('%H:%M')} |\n"
            f"| Responsable: {self.__responsable} |\n"
            f"| Motif: {self.__motif} |"
        )