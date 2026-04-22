# models/equipement.py
from models.ressource import Ressource


class Equipement(Ressource):
    """Représente un équipement réservable (projecteur, pc, micro, tableau)."""

    TYPES = ["Projecteur", "Ordinateur", "Microphone", "Tableau interactif"]

    def __init__(self, nom: str, localisation: str, type_eq: str, marque: str = ""):
        super().__init__(nom, localisation)

        # Vérification du type
        if type_eq in Equipement.TYPES:
            self.__type = type_eq
        else:
            self.__type = "Projecteur"  # valeur par défaut

        self.__marque = marque

    def get_type(self):
        return self.__type

    def get_marque(self):
        return self.__marque

    def get_info(self) -> str:
        statut = "✅" if self.est_disponible() else "❌"
        return f"{statut} {self.get_nom()} | {self.__type} | {self.__marque} | {self.get_localisation()}"

    def __str__(self):
        return self.get_info()