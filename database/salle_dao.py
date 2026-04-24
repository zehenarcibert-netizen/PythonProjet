# database/salle_dao.py
#BLOC 4 --DAO (Data Access Object) pour les salles
# Toutes les opérations CRUD sur la table salles

class SalleDAO:
    """Gere les opérations base de données pour les salles."""

    def __init__(self, db__manager):
        self.conn = db_manager.get_connexion()

    #___CREATE_______________________________________________
    def inserer(self, salle)  -> int:
        """Insere une salle et retourne son ID."""
        curseur = self.conn.cursor()
        curseur.execute("""
            INSERT INTO salles (numero,nom,localisation,capacite,type_salle,disponible)
            VALUES (?, ?, ?, ?, ?, ?)
        """,(
           salle.get_numero(),
           salle.get_nom(),
           salle.get_localisation(),
           salle.get_capacite(),
           salle.get_type(),
           1 if salle.est_disponible() else 0
        ))
        self.conn.commit()
        print(f"[DB]  Salle inseré : {salle.get_nom()} (ID={curseur.lastrowid})")
        return curseur.lastrowid
    # ________READ_______________________________
    def get_toutes(self) -> list:
        """Retourne toutes les salles."""
        curseur = self.conn.cursor()
        curseur.execute("SELECT * FROM salles ORDER BY numero ")

    def get_par_id(self, salle_id: int) :

        curseur =self.conn.cursor()
        curseur.execute("SELECT * FROM salles WHERE id = ?", (salle_id,))
        return curseur.fetchall()
    
    def disponibles(self) -> list:
        curseur = self.conn.cursor()
        curseur.execute("SELECT * FROM salles WHERE disponible =1 ORDER BY nom")
        return curseur.fetchall()
    
    #______________UPDATE___________________________
    def modifier(self, salle_id: int, capacite:int, type_salle: str, disponible: bool):
      curseur = self.conn.cursor()
      curseur.execute ("""
         UPDATE salles
         SET capacite = ?, type_salle = ?, disponible = ?
         WHERE id =?
       """,  (capacite, type_salle, 1 if disponible else 0,salle_id))
       self.conn.commit()
       print(f"[DB] Salle {salle_id} modifiée.")
      
      #_________DELETE__________________________________________
      def supprimer(self, salle_id: int ) -> bool:
         curseur =self.conn.cursor()
         curseur.execute("DELETE FROM salles WHERE id = ?",(salle_id,))
         self.conn.commit()
         print(f"[DB] Salle {salle_id} supprimée.")
         return curseur.rowcount > 0
                      
      
    