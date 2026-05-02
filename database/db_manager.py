# database/db_manager.py
# BLOC 4 — SQLite uniquement
# Le fichier .db sera créé dans le même dossier que le projet

import sqlite3
import os

# Le fichier sera créé ici :
# C:\Users\USER\PythonProject\PythonProject\reservation_up.db
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "reservation_up.db")

class DatabaseManager:

    def __init__(self):
        self.db_path = os.path.abspath(DB_PATH)
        self.connexion = None
        self._initialiser()
        print(f"[DB] Fichier base de donnees : {self.db_path}")

    def _initialiser(self):
        self.connexion = sqlite3.connect(self.db_path)
        self.connexion.row_factory = sqlite3.Row
        curseur = self.connexion.cursor()

        curseur.executescript("""
            CREATE TABLE IF NOT EXISTS salles (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                numero       TEXT    NOT NULL,
                nom          TEXT    NOT NULL,
                localisation TEXT    NOT NULL,
                capacite     INTEGER NOT NULL,
                type_salle   TEXT    NOT NULL,
                disponible   INTEGER DEFAULT 1
            );

            CREATE TABLE IF NOT EXISTS equipements (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                nom          TEXT    NOT NULL,
                localisation TEXT    NOT NULL,
                type_eq      TEXT    NOT NULL,
                marque       TEXT,
                salle_id     INTEGER,
                disponible   INTEGER DEFAULT 1,
                FOREIGN KEY (salle_id) REFERENCES salles(id)
            );

            CREATE TABLE IF NOT EXISTS utilisateurs (
                id                INTEGER PRIMARY KEY AUTOINCREMENT,
                nom               TEXT NOT NULL,
                prenom            TEXT NOT NULL,
                email             TEXT UNIQUE NOT NULL,
                mot_de_passe_hash TEXT NOT NULL,
                role              TEXT NOT NULL DEFAULT 'enseignant',
                actif             INTEGER DEFAULT 1
            );

            CREATE TABLE IF NOT EXISTS reservations (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                salle_id    INTEGER NOT NULL,
                responsable TEXT    NOT NULL,
                date_res    TEXT    NOT NULL,
                heure_debut TEXT    NOT NULL,
                heure_fin   TEXT    NOT NULL,
                motif       TEXT,
                cree_le     TEXT    DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (salle_id) REFERENCES salles(id)
            );
        """)
        self.connexion.commit()

    def get_connexion(self):
        return self.connexion

    def fermer(self):
        if self.connexion:
            self.connexion.close()