# models/utilisateur.py
import hashlib

class Utilisateur:
    """Représente un utilisateur du système avec son rôle"""

    ROLES = ["administrateur", "enseignant", "agent"]
    _compteur = 0

    def __init__(self, nom: str, prenom: str, email: str,
                 mot_de_passe: str, role: str = "enseignant"):

        Utilisateur._compteur += 1
        self.__id = Utilisateur._compteur

        self.__nom = nom
        self.__prenom = prenom
        self.__email = email
        self.__mot_de_passe_hash = self._hasher(mot_de_passe)

        self.__role = role if role in Utilisateur.ROLES else "enseignant"
        self.__actif = True

    # --- Sécurité ---
    def _hasher(self, mot_de_passe: str) -> str:
        return hashlib.sha256(mot_de_passe.encode()).hexdigest()

    def verifier_mot_de_passe(self, mot_de_passe: str) -> bool:
        return self.__mot_de_passe_hash == self._hasher(mot_de_passe)

    def changer_mot_de_passe(self, ancien: str, nouveau: str) -> bool:
        if self.verifier_mot_de_passe(ancien):
            self.__mot_de_passe_hash = self._hasher(nouveau)
            return True
        return False

    # --- Getters ---
    def get_id(self): return self.__id
    def get_nom(self): return self.__nom
    def get_prenom(self): return self.__prenom
    def get_nom_complet(self): return f"{self.__prenom} {self.__nom}"
    def get_email(self): return self.__email
    def get_role(self): return self.__role
    def est_actif(self): return self.__actif

    # --- Setters ---
    def set_nom(self, v): self.__nom = v
    def set_prenom(self, v): self.__prenom = v
    def set_email(self, v): self.__email = v

    def set_role(self, v):
        if v in Utilisateur.ROLES:
            self.__role = v

    def set_actif(self, v): self.__actif = v

    # --- Permissions ---
    def peut_gerer_salles(self) -> bool:
        return self.__role in ["administrateur", "agent"]

    def peut_gerer_utilisateurs(self) -> bool:
        return self.__role == "administrateur"

    def __str__(self):
        return f"[{self.__id}] {self.get_nom_complet()} | {self.__email} | {self.__role}"