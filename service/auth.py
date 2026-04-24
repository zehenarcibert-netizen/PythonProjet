# services/auth.py
from models.utilisateur import Utilisateur

class AuthService:
    """Gère l'authentification et les comptes utilisateurs."""

    def __init__(self):
        self.__utilisateurs: list[Utilisateur] = []
        self.__connecte: Utilisateur | None = None
        self._creer_comptes_defaut()

    def _creer_comptes_defaut(self):
        """Comptes de démonstration."""
        self.__utilisateurs = [
            Utilisateur("Admin",    "Super",   "admin@up.bj",    "admin123",    "administrateur"),
            Utilisateur("Adjonou",  "Kofi",    "k.adjonou@up.bj","enseign123",  "enseignant"),
            Utilisateur("Bello",    "Maryam",  "m.bello@up.bj",  "agent123",    "agent"),
            Utilisateur("ZEHE", "Narcibert", "zehenarcibert@gmail.com", "Zeheepiph@nie976090", "administrateur"),
            Utilisateur("YAOITCHA", "Rosette", "yaoitcharosette@gmail.com", "12345678", "agent"),
        ]

    # --- Authentification ---
    def connecter(self, email: str, mot_de_passe: str) -> tuple[bool, str]:
        for u in self.__utilisateurs:
            if u.get_email() == email and u.est_actif():
                if u.verifier_mot_de_passe(mot_de_passe):
                    self.__connecte = u
                    return True, f"Bienvenue, {u.get_nom_complet()} !"
                else:
                    return False, "Mot de passe incorrect."
        return False, "Aucun compte trouvé avec cet email."

    def deconnecter(self):
        self.__connecte = None

    def get_utilisateur_connecte(self) -> Utilisateur | None:
        return self.__connecte

    def est_connecte(self) -> bool:
        return self.__connecte is not None

    # --- Gestion des comptes ---
    def creer_compte(self, nom, prenom, email, mdp, role) -> tuple[bool, str]:
        if any(u.get_email() == email for u in self.__utilisateurs):
            return False, "Cet email est déjà utilisé."
        self.__utilisateurs.append(Utilisateur(nom, prenom, email, mdp, role))
        return True, "Compte créé avec succès."

    def get_tous_utilisateurs(self) -> list[Utilisateur]:
        return self.__utilisateurs

    def supprimer_utilisateur(self, uid: int) -> bool:
        for i, u in enumerate(self.__utilisateurs):
            if u.get_id() == uid:
                self.__utilisateurs.pop(i)
                return True
        return False

    def modifier_role(self, uid: int, nouveau_role: str) -> bool:
        for u in self.__utilisateurs:
            if u.get_id() == uid:
                u.set_role(nouveau_role)
                return True
        return False

