#exceptions/exception_projet/py
#Bloc 5 - exception persoonaliser
#----------Exception Réservation -------------------
from pyexpat.errors import messages


class ConflitReservationError(Exception):
    """Leveé quand deux réservation se chevauchent"""
    def __init__(self, message ="conflit d'horaire détecter avec une réservation existante."):
        super().__init__(message)
class HoraireInvalideError(Exception):
    """Leveé quand les heure de fin est avant ou égale à l'heure de début """
    def __init__(self):
        super().__init__("L'heure de fin doit être stricyement après l'heure de début.")
class ReservationIntrouvableError(Exception):
    """Leveé quand une reservation es inexistant ou introuvable"""
    def __init__(self, res_id:int):
        super().__init__(f"Le reservation {res_id} est introuvable.")

#---------Exception salle--------------
class SalleIntrouvableError(Exception):
    """leveé quand une salle est introuvable ou n'exite pas """
    def __init__(self,nom:str =""):
        super().__init__(f"Le salle est introuvable:'{nom}'.")

class SalleIndisponibleError(Exception):
    """leveé quand une sallle est marquéeindisponible."""
    def __init__(self,nom:str =""):
        super().__init__(f"Le salle '{nom}'est  actuellement indisponible.")

class CapaciteIndisponibleError(ValueError):
    """leveé quand le nombre de participant dépasse la capacité """
    def __init__(self, capacite: int,demande: int):
        super().__init__(f"capaciter insuffisante : salle={capacite} place , demande={demande} personne.")



#----------Exception utilisateur----------
class EmailDejaUtiliseError(Exception):
    """levée lors de la créatioon d'un compte avec un email existant"""
    def __init__(self, email: str):
        super().__init__(f"L'email  '{email}'est déjà utiliser.")

class AuthentificationError(Exception):
    """levée quand les identifiants sont incorrectes"""
    def __init__(self):
        super().__init__("Email ou le mots de passe es incorrecte veillez revoir. ")

class PermissionRefuseeError(Exception):
    """levée quand un utilisateur tente une action nom autoriser """
    def __init__(self, role: str, action: str):
        super().__init__(f"Rôle '{role}' non autorisé à effectuer : {action}.")

#----------Exceotion base de donner --------------
class BaseDonneesError(Exception):
    """levée pour toute erreur de base de donner """
    def __init__(self, message: str):
        super().__init__(f"Erreur base de donner : {message}")

class ExportError(Exception):
    """levée lors d'un échec d'export JSON/CSV."""
    def __init__(self, format_fichier: str):
        super().__init__(f"Echec d'export {format_fichier} : {messages}")