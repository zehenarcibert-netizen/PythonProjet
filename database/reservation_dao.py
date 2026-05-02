# database/reservation_dao.py
# BLOC 4 — CRUD Réservations dans SQLite

class ReservationDAO:

    def __init__(self, db_manager):
        self.conn = db_manager.get_connexion()

    # ── CREATE ────────────────────────────────────────────────────────────────
    def inserer(self, reservation) -> int:
        c = self.conn.cursor()

        # ══ Chercher l'ID de la salle dans SQLite par son NOM ══
        c.execute(
            "SELECT id FROM salles WHERE nom = ?",
            (reservation.get_salle().get_nom(),)
        )
        salle_row = c.fetchone()

        if not salle_row:
            print(f"[ERREUR] Salle '{reservation.get_salle().get_nom()}' introuvable en base !")
            return -1

        salle_id_sqlite = salle_row["id"]  # ← ID réel dans SQLite

        c.execute("""
            INSERT INTO reservations
                (salle_id, responsable, date_res, heure_debut, heure_fin, motif)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            salle_id_sqlite,  # ← ID SQLite correct
            reservation.get_responsable(),
            reservation.get_date().isoformat(),
            reservation.get_heure_debut().strftime("%H:%M"),
            reservation.get_heure_fin().strftime("%H:%M"),
            reservation.get_motif()
        ))
        self.conn.commit()
        print(f"[SQLite] Reservation inseree (ID={c.lastrowid})")
        return c.lastrowid

    # ── READ ──────────────────────────────────────────────────────────────────
    def get_toutes(self) -> list:
        c = self.conn.cursor()
        c.execute("""
            SELECT r.*, s.nom as salle_nom, s.numero as salle_numero
            FROM reservations r
            JOIN salles s ON r.salle_id = s.id
            ORDER BY r.date_res, r.heure_debut
        """)
        return c.fetchall()

    def get_par_date(self, date_str: str) -> list:
        c = self.conn.cursor()
        c.execute("""
            SELECT r.*, s.nom as salle_nom
            FROM reservations r
            JOIN salles s ON r.salle_id = s.id
            WHERE r.date_res = ?
            ORDER BY r.heure_debut
        """, (date_str,))
        return c.fetchall()

    def get_par_salle(self, salle_id: int) -> list:
        c = self.conn.cursor()
        c.execute("""
            SELECT * FROM reservations
            WHERE salle_id = ?
            ORDER BY date_res, heure_debut
        """, (salle_id,))
        return c.fetchall()

    def get_par_id(self, res_id: int):
        c = self.conn.cursor()
        c.execute("""
            SELECT r.*, s.nom as salle_nom
            FROM reservations r
            JOIN salles s ON r.salle_id = s.id
            WHERE r.id = ?
        """, (res_id,))
        return c.fetchone()

    # ── UPDATE ────────────────────────────────────────────────────────────────
    def modifier(self, res_id: int, date_res: str,
                 heure_debut: str, heure_fin: str, motif: str):
        c = self.conn.cursor()
        c.execute("""
            UPDATE reservations
            SET date_res=?, heure_debut=?, heure_fin=?, motif=?
            WHERE id=?
        """, (date_res, heure_debut, heure_fin, motif, res_id))
        self.conn.commit()

    # ── DELETE ────────────────────────────────────────────────────────────────
    def supprimer(self, res_id: int) -> bool:
        c = self.conn.cursor()
        c.execute("DELETE FROM reservations WHERE id=?", (res_id,))
        self.conn.commit()
        return c.rowcount > 0

    # ── STATISTIQUES ──────────────────────────────────────────────────────────
    def get_statistiques(self) -> dict:
        c = self.conn.cursor()
        c.execute("SELECT COUNT(*) as total FROM reservations")
        total = c.fetchone()["total"]

        c.execute("""
            SELECT s.nom, COUNT(*) as nb
            FROM reservations r
            JOIN salles s ON r.salle_id = s.id
            GROUP BY r.salle_id
            ORDER BY nb DESC
        """)
        par_salle = {row["nom"]: row["nb"] for row in c.fetchall()}

        return {
            "total":     total,
            "par_salle": par_salle,
            "salle_top": max(par_salle, key=par_salle.get) if par_salle else "—"
        }

    def compter(self) -> int:
        c = self.conn.cursor()
        c.execute("SELECT COUNT(*) FROM reservations")
        return c.fetchone()[0]