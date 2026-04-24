# database/export_service.py
# BLOC 4 — Export JSON et CSV des données

import json
import csv
import os
from datetime import datetime

class ExportService:
    """Gère l'export des données en JSON et CSV."""

    def __init__(self, reservation_dao, salle_dao):
        self.res_dao  = reservation_dao
        self.salle_dao = salle_dao

    # ─── EXPORT JSON ──────────────────────────────────────────────────────────
    def exporter_json(self, fichier: str = "export_reservations.json") -> bool:
        """Exporte toutes les réservations en JSON."""
        try:
            reservations = self.res_dao.get_toutes()
            data = []
            for r in reservations:
                data.append({
                    "id":          r["id"],
                    "salle":       r["salle_nom"],
                    "responsable": r["responsable"],
                    "date":        r["date_res"],
                    "debut":       r["heure_debut"],
                    "fin":         r["heure_fin"],
                    "motif":       r["motif"],
                    "cree_le":     r["cree_le"]
                })

            with open(fichier, "w", encoding="utf-8") as f:
                json.dump({
                    "exported_at": datetime.now().isoformat(),
                    "total":       len(data),
                    "reservations": data
                }, f, ensure_ascii=False, indent=2)

            print(f"[EXPORT] JSON créé : {fichier} ({len(data)} réservations)")
            return True

        except Exception as e:
            print(f"[ERREUR] Export JSON : {e}")
            return False

    # ─── IMPORT JSON ──────────────────────────────────────────────────────────
    def importer_json(self, fichier: str = "export_reservations.json") -> int:
        """Importe des réservations depuis un fichier JSON."""
        if not os.path.exists(fichier):
            print(f"[ERREUR] Fichier introuvable : {fichier}")
            return 0
        try:
            with open(fichier, "r", encoding="utf-8") as f:
                data = json.load(f)

            print(f"[IMPORT] {data['total']} réservations trouvées dans {fichier}")
            return data["total"]

        except Exception as e:
            print(f"[ERREUR] Import JSON : {e}")
            return 0

    # ─── EXPORT CSV ───────────────────────────────────────────────────────────
    def exporter_csv(self, fichier: str = "rapport_reservations.csv") -> bool:
        """Exporte toutes les réservations en CSV."""
        try:
            reservations = self.res_dao.get_toutes()

            with open(fichier, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f, delimiter=";")

                # En-tête
                writer.writerow([
                    "ID", "Salle", "Numéro", "Date",
                    "Début", "Fin", "Responsable", "Motif", "Créé le"
                ])

                # Données
                for r in reservations:
                    writer.writerow([
                        r["id"],
                        r["salle_nom"],
                        r["salle_numero"],
                        r["date_res"],
                        r["heure_debut"],
                        r["heure_fin"],
                        r["responsable"],
                        r["motif"] or "",
                        r["cree_le"]
                    ])

            print(f"[EXPORT] CSV créé : {fichier} ({len(reservations)} lignes)")
            return True

        except Exception as e:
            print(f"[ERREUR] Export CSV : {e}")
            return False

    # ─── RAPPORT STATISTIQUES CSV ─────────────────────────────────────────────
    def exporter_rapport_stats(self, fichier: str = "rapport_stats.csv") -> bool:
        """Exporte un rapport de statistiques par salle."""
        try:
            salles = self.salle_dao.get_toutes()

            with open(fichier, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f, delimiter=";")
                writer.writerow(["Salle", "Type", "Capacité", "Nb Réservations", "Taux %"])

                stats = self.res_dao.get_statistiques()
                total = stats["total"]

                for s in salles:
                    res_salle = self.res_dao.get_par_salle(s["id"])
                    nb = len(res_salle)
                    taux = round(nb / total * 100, 1) if total > 0 else 0
                    writer.writerow([
                        s["nom"], s["type_salle"],
                        s["capacite"], nb, f"{taux}%"
                    ])

            print(f"[EXPORT] Rapport stats créé : {fichier}")
            return True

        except Exception as e:
            print(f"[ERREUR] Rapport stats : {e}")
            return False
