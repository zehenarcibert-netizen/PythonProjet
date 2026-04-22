# models/ressource.py
# Classe mère pour toutes les ressources de l'université

class Ressource:
    """Classe abstraite représentant une ressource universitaire."""

    _compteur_id = 0  # Attribut de classe (partagé par toutes les instances)

    def __init__(self, nom: str, localisation: str):
        Ressource._compteur_id += 1
        self.__id = Ressource._compteur_id   # Attribut privé (encapsulation)
        self.__nom = nom
        self.__localisation = localisation
        self._disponible = True              # Attribut protégé

    # --- Getters ---
    def get_id(self):
        return self.__id

    def get_nom(self):
        return self.__nom

    def get_localisation(self):
        return self.__localisation

    def est_disponible(self):
        return self._disponible

    # --- Setters ---
    def set_nom(self, nom: str):
        if nom.strip():
            self.__nom = nom

    def set_disponible(self, etat: bool):
        self._disponible = etat

    # --- Méthode polymorphe ---
    def get_info(self) -> str:
        statut = "Disponible" if self._disponible else "Indisponible"
        return f"[{self.__id}] {self.__nom} | {self.__localisation} | {statut}"

    def __str__(self):
        return self.get_info()
        return self.get_info()
        return self.get_info()
        return self.get_info()
        return self.get_info()