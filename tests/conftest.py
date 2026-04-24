# tests/conftest.py
# configuration globale de Pytest
# ce fichier es automatiquement lu par  pytest
import sys
import os

#ajouter le dossier racine au chemin python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..."))