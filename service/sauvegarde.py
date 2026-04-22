# services/sauvegarde.py
# Fonctionnalité 9 : Sécurité — Sauvegarde automatique des données
import json
import os
from datetime import date, time, datetime

FICHIER_SAUVEGARDE = "donnees_sauvegarde.json"

class SauvegardeService:
    """Gère la sauvegarde et la restauration des réservations (JSON)."""

    @staticmethod
    def sauvegarder(planning) -> bool:
        """Sauvegarde toutes les réservations dans un fichier JSON."""
        try:
            data = []
            for r in planning.get_reservations():
                data.append({
                    "salle_id":    r.get_salle().get_id(),
                    "salle_nom":   r.get_salle().get_nom(),
                    "responsable": r.get_responsable(),
                    "date":        r.get_date().isoformat(),
                    "heure_debut": r.get_heure_debut().strftime("%H:%M"),
                    "heure_fin":   r.get_heure_fin().strftime("%H:%M"),
                    "motif":       r.get_motif(),
                    "sauvegarde_le": datetime.now().isoformat()
                })

            with open(FICHIER_SAUVEGARDE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            return True
        except Exception as e:
            print(f"Erreur sauvegarde : {e}")
            return False

    @staticmethod
    def charger(planning) -> int:
        """Recharge les réservations depuis le fichier JSON."""
        if not os.path.exists(FICHIER_SAUVEGARDE):
            return 0

        try:
            with open(FICHIER_SAUVEGARDE, "r", encoding="utf-8") as f:
                data = json.load(f)

            from models.reservation import Reservation
            nb = 0
            for item in data:
                salle = planning.get_salle_par_id(item["salle_id"])
                if salle:
                    d = date.fromisoformat(item["date"])
                    h1 = datetime.strptime(item["heure_debut"], "%H:%M").time()
                    h2 = datetime.strptime(item["heure_fin"],   "%H:%M").time()
                    r = Reservation(salle, item["responsable"], d, h1, h2, item["motif"])
                    planning.ajouter_reservation(r)
                    nb += 1
            return nb
        except Exception as e:
            print(f"Erreur chargement : {e}")
            return 0

    @staticmethod
    def exporter_csv(planning, fichier: str = "rapport_reservations.csv") -> bool:
        """Exporte les réservations en CSV (Fonctionnalité 8 : rapports)."""
        try:
            lignes = ["ID,Salle,Date,Debut,Fin,Responsable,Motif\n"]
            for r in planning.get_reservations():
                lignes.append(
                    f"{r.get_id()},"
                    f"{r.get_salle().get_nom()},"
                    f"{r.get_date().strftime('%d/%m/%Y')},"
                    f"{r.get_heure_debut().strftime('%H:%M')},"
                    f"{r.get_heure_fin().strftime('%H:%M')},"
                    f"{r.get_responsable()},"
                    f"{r.get_motif()}\n"
                )
            with open(fichier, "w", encoding="utf-8") as f:
                f.writelines(lignes)
            return True
        except Exception as e:
            print(f"Erreur export CSV : {e}")
            return False

