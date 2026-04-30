# database/db_manager.py
# BLOC 4 — Persistance SQLite
# Gère la connexion et la création des tables

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "reservation_up.db")

class DatabaseManager:
    """Gestionnaire de la base de données SQLite."""

    def __init__(self):
        self.db_path = DB_PATH
        self.connexion = None
        self._initialiser()

    def _initialiser(self):
        """Crée les tables si elles n'existent pas encore."""
        self.connexion = sqlite3.connect(self.db_path)
        self.connexion.row_factory = sqlite3.Row  # accès par nom de colonne
        curseur = self.connexion.cursor()

        curseur.executescript("""
            CREATE TABLE IF NOT EXISTS salles (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                numero      TEXT    NOT NULL,
                nom         TEXT    NOT NULL,
                localisation TEXT   NOT NULL,
                capacite    INTEGER NOT NULL,
                type_salle  TEXT    NOT NULL,
                disponible  INTEGER DEFAULT 1
            );

            CREATE TABLE IF NOT EXISTS equipements (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                nom         TEXT    NOT NULL,
                localisation TEXT   NOT NULL,
                type_eq     TEXT    NOT NULL,
                marque      TEXT,
                salle_id    INTEGER,
                disponible  INTEGER DEFAULT 1,
                FOREIGN KEY (salle_id) REFERENCES salles(id)
            );

            CREATE TABLE IF NOT EXISTS utilisateurs (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                nom         TEXT    NOT NULL,
                prenom      TEXT    NOT NULL,
                email       TEXT    UNIQUE NOT NULL,
                mot_de_passe_hash TEXT NOT NULL,
                role        TEXT    NOT NULL DEFAULT 'enseignant',
                actif       INTEGER DEFAULT 1
            );

            CREATE TABLE IF NOT EXISTS reservations (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                salle_id     INTEGER NOT NULL,
                responsable  TEXT    NOT NULL,
                date_res     TEXT    NOT NULL,
                heure_debut  TEXT    NOT NULL,
                heure_fin    TEXT    NOT NULL,
                motif        TEXT,
                cree_le      TEXT    DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (salle_id) REFERENCES salles(id)
            );
        """)
        self.connexion.commit()
        print(f"[DB] Base de données initialisée : {self.db_path}")

    def get_connexion(self):
        return self.connexion

    def fermer(self):
        if self.connexion:
            self.connexion.close()
            print("[DB] Connexion fermée.")
