# models/salle.py
from models.ressource import Ressource


class Salle(Ressource):
    """Représentation d'une salle avec ses équipements"""

    TYPES = ["Cours", "TD", "Amphi", "Réunion", "Informatique"]

    def __init__(self, nom: str, numero: str, localisation: str,
                 capacite: int, type_salle: str = "Cours"):

        super().__init__(nom, localisation)
        self.__numero = numero
        self.__capacite = capacite
        self.__type_salle = type_salle if type_salle in Salle.TYPES else "Cours"
        self.__equipements = []  # liste d'objets Equipement

    # --- Gestion des équipements ---
    def ajouter_equipement(self, equipement):
        self.__equipements.append(equipement)

    def get_equipements(self):
        return self.__equipements

    def nom_equipements(self) -> str:
        if not self.__equipements:
            return "aucun"
        return ", ".join(e.get_type() for e in self.__equipements)

    # --- Getters ---
    def get_numero(self):
        return self.__numero

    def get_type(self):
        return self.__type_salle

    def get_capacite(self):
        return self.__capacite

    # --- Setters ---
    def set_capacite(self, v):
        self.__capacite = v

    def set_type_salle(self, v):
        if v in Salle.TYPES:
            self.__type_salle = v

    # --- Info ---
    def get_info(self) -> str:
        statut = "✅" if self.est_disponible() else "❌"
        return (
            f"{statut} {self.__numero} - {self.get_nom()} | "
            f"{self.__type_salle} | {self.__capacite} places | "
            f"{self.nom_equipements()} | {self.get_localisation()}"
        )

    def __str__(self):
        return self.get_info()