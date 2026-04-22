# services/notification.py
from datetime import datetime

class Notification:
    """Représente une notification système."""
    _compteur = 0

    def __init__(self, type_notif: str, destinataire: str, message: str):
        Notification._compteur += 1
        self.id = Notification._compteur
        self.type = type_notif   # "confirmation", "annulation", "modification", "rappel"
        self.destinataire = destinataire
        self.message = message
        self.date = datetime.now()
        self.lue = False

    def __str__(self):
        statut = "✅" if self.lue else "🔔"
        return f"{statut} [{self.type.upper()}] {self.message} — {self.date.strftime('%d/%m %H:%M')}"


class NotificationService:
    """Gère l'envoi et le stockage des notifications."""

    def __init__(self):
        self.__notifications: list[Notification] = []

    def envoyer(self, type_notif: str, destinataire: str, message: str):
        n = Notification(type_notif, destinataire, message)
        self.__notifications.append(n)
        return n

    def confirmation_reservation(self, reservation, utilisateur: str):
        msg = (f"Réservation confirmée : {reservation.get_salle().get_nom()} | "
               f"{reservation.get_date().strftime('%d/%m/%Y')} | "
               f"{reservation.get_heure_debut().strftime('%H:%M')} → "
               f"{reservation.get_heure_fin().strftime('%H:%M')}")
        self.envoyer("confirmation", utilisateur, msg)
        self.envoyer("confirmation", "administration", f"[{utilisateur}] {msg}")

    def annulation_reservation(self, reservation, utilisateur: str):
        msg = (f"Réservation annulée : {reservation.get_salle().get_nom()} | "
               f"{reservation.get_date().strftime('%d/%m/%Y')}")
        self.envoyer("annulation", utilisateur, msg)
        self.envoyer("annulation", "administration", f"[{utilisateur}] {msg}")

    def modification_reservation(self, reservation, utilisateur: str):
        msg = f"Réservation modifiée : #{reservation.get_id()} — {reservation.get_salle().get_nom()}"
        self.envoyer("modification", utilisateur, msg)

    def get_notifications(self, destinataire: str = None) -> list[Notification]:
        if destinataire:
            return [n for n in self.__notifications if n.destinataire == destinataire]
        return self.__notifications

    def get_non_lues(self, destinataire: str) -> list[Notification]:
        return [n for n in self.get_notifications(destinataire) if not n.lue]

    def marquer_lue(self, notif_id: int):
        for n in self.__notifications:
            if n.id == notif_id:
                n.lue = True

