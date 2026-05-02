# database/salle_dao.py
# BLOC 4 — CRUD Salles dans SQLite

class SalleDAO:

    def __init__(self, db_manager):
        self.conn = db_manager.get_connexion()

    # ── CREATE ────────────────────────────────────────────────────────────────
    def inserer(self, salle) -> int:
        c = self.conn.cursor()
        c.execute("""
            INSERT INTO salles (numero, nom, localisation, capacite, type_salle, disponible)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            salle.get_numero(),
            salle.get_nom(),
            salle.get_localisation(),
            salle.get_capacite(),
            salle.get_type(),
            1 if salle.est_disponible() else 0
        ))
        self.conn.commit()
        return c.lastrowid

    # ── READ ──────────────────────────────────────────────────────────────────
    def get_toutes(self) -> list:
        c = self.conn.cursor()
        c.execute("SELECT * FROM salles ORDER BY numero")
        return c.fetchall()

    def get_par_id(self, salle_id: int):
        c = self.conn.cursor()
        c.execute("SELECT * FROM salles WHERE id = ?", (salle_id,))
        return c.fetchone()

    def get_disponibles(self) -> list:
        c = self.conn.cursor()
        c.execute("SELECT * FROM salles WHERE disponible = 1")
        return c.fetchall()

    # ── UPDATE ────────────────────────────────────────────────────────────────
    def modifier(self, salle_id: int, capacite: int, type_salle: str, disponible: bool):
        c = self.conn.cursor()
        c.execute("""
            UPDATE salles SET capacite=?, type_salle=?, disponible=?
            WHERE id=?
        """, (capacite, type_salle, 1 if disponible else 0, salle_id))
        self.conn.commit()

    # ── DELETE ────────────────────────────────────────────────────────────────
    def supprimer(self, salle_id: int) -> bool:
        c = self.conn.cursor()
        c.execute("DELETE FROM salles WHERE id=?", (salle_id,))
        self.conn.commit()
        return c.rowcount > 0

    def compter(self) -> int:
        c = self.conn.cursor()
        c.execute("SELECT COUNT(*) FROM salles")
        return c.fetchone()[0]