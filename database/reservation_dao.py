# database/reservation_dao.py
# BLOC 4 — DAO pour les Réservations

class ReservationDAO:
    """Gère les opérations base de données pour les réservations."""

    def __init__(self, db_manager):
        self.conn = db_manager.get_connexion()

    # ─── CREATE ───────────────────────────────────────────────────────────────
    def inserer(self, reservation) -> int:
        curseur = self.conn.cursor()
        curseur.execute("""
            INSERT INTO reservations
                (salle_id, responsable, date_res, heure_debut, heure_fin, motif)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            reservation.get_salle().get_id(),
            reservation.get_responsable(),
            reservation.get_date().isoformat(),
            reservation.get_heure_debut().strftime("%H:%M"),
            reservation.get_heure_fin().strftime("%H:%M"),
            reservation.get_motif()
        ))
        self.conn.commit()
        print(f"[DB] Réservation insérée (ID={curseur.lastrowid})")
        return curseur.lastrowid

    # ─── READ ─────────────────────────────────────────────────────────────────
    def get_toutes(self) -> list:
        curseur = self.conn.cursor()
        curseur.execute("""
            SELECT r.*, s.nom as salle_nom, s.numero as salle_numero
            FROM reservations r
            JOIN salles s ON r.salle_id = s.id
            ORDER BY r.date_res, r.heure_debut
        """)
        return curseur.fetchall()

    def get_par_date(self, date_str: str) -> list:
        curseur = self.conn.cursor()
        curseur.execute("""
            SELECT r.*, s.nom as salle_nom
            FROM reservations r
            JOIN salles s ON r.salle_id = s.id
            WHERE r.date_res = ?
            ORDER BY r.heure_debut
        """, (date_str,))
        return curseur.fetchall()

    def get_par_salle(self, salle_id: int) -> list:
        curseur = self.conn.cursor()
        curseur.execute("""
            SELECT * FROM reservations
            WHERE salle_id = ?
            ORDER BY date_res, heure_debut
        """, (salle_id,))
        return curseur.fetchall()

    def get_par_id(self, res_id: int):
        curseur = self.conn.cursor()
        curseur.execute("SELECT * FROM reservations WHERE id = ?", (res_id,))
        return curseur.fetchone()

    # ─── UPDATE ───────────────────────────────────────────────────────────────
    def modifier(self, res_id: int, date_res: str, heure_debut: str,
                 heure_fin: str, motif: str):
        curseur = self.conn.cursor()
        curseur.execute("""
            UPDATE reservations
            SET date_res = ?, heure_debut = ?, heure_fin = ?, motif = ?
            WHERE id = ?
        """, (date_res, heure_debut, heure_fin, motif, res_id))
        self.conn.commit()
        print(f"[DB] Réservation {res_id} modifiée.")

    # ─── DELETE ───────────────────────────────────────────────────────────────
    def supprimer(self, res_id: int) -> bool:
        curseur = self.conn.cursor()
        curseur.execute("DELETE FROM reservations WHERE id = ?", (res_id,))
        self.conn.commit()
        return curseur.rowcount > 0

    # ─── STATISTIQUES ─────────────────────────────────────────────────────────
    def get_statistiques(self) -> dict:
        curseur = self.conn.cursor()
        curseur.execute("SELECT COUNT(*) as total FROM reservations")
        total = curseur.fetchone()["total"]

        curseur.execute("""
            SELECT s.nom, COUNT(*) as nb
            FROM reservations r
            JOIN salles s ON r.salle_id = s.id
            GROUP BY r.salle_id
            ORDER BY nb DESC
            LIMIT 1
        """)
        top = curseur.fetchone()

        return {
            "total": total,
            "salle_top": top["nom"] if top else "—",
            "salle_top_nb": top["nb"] if top else 0
        }
