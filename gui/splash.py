import tkinter as tk
import time
import threading
from zipfile import sizeCentralDir

BLEU_FONCE = "#1a3a5c"
BLANC      = "#ffffff"
ROUGE      = "#dc7626"
BLEU_CLAIR = "#93c5fd"
noire = "#000000"

class SplashScreen(tk.Toplevel):
    """Écran de démarrage affiché au lancement."""

    def __init__(self, parent):
        super().__init__(parent)
        self.overrideredirect(True)   # Pas de barre de titre
        self.configure(bg=BLEU_FONCE)

        # Centrer sur l'écran
        largeur, hauteur = 900, 820
        x = (self.winfo_screenwidth()  - largeur) // 2
        y = (self.winfo_screenheight() - hauteur) // 2
        self.geometry(f"{largeur}x{hauteur}+{x}+{y}")

        # Contenu
        tk.Label(self, text="", font=("Segoe UI", 52),
                 bg=BLEU_FONCE, fg=BLANC).pack(pady=(30, 5))

        tk.Label(self, text="***BIENVENUE  ***",
                 font=("Segoe UI",16, "bold"),
                 bg=BLEU_FONCE, fg=BLANC).pack()
        tk.Label(self, text="***UNIVERSITER DE PARAKOU ***",
                 font=("Segoe UI", 4, "bold"),
                 bg=BLEU_FONCE, fg=BLANC).pack()

        tk.Label(self, text="Système de Réservation de Salles",
                 font=("Segoe UI", 25),
                 bg=BLEU_FONCE, fg=BLEU_CLAIR).pack(pady=10)

        tk.Label(self, text="Bienvenus sur notre portail  \n"
                            "Nous vou prinons de prendre le soint de lire les condition de confidentialiter ",
                 font=("Segoe UI", 18),
                 bg=BLEU_FONCE, fg="#64748b").pack()

        # Barre de progression
        self.canvas = tk.Canvas(self, width=800, height=5,
                                bg="#0f2940", highlightthickness=0)
        self.canvas.pack(pady= 200)
        self.barre = self.canvas.create_rectangle(0, 0, 0, 12,
                                                   fill=noire, outline="")

        self.lbl_status = tk.Label(self, text="Chargement...",
                                   font=("Segoe UI", 5),
                                   bg=BLEU_FONCE, fg=BLEU_CLAIR)
        self.lbl_status.pack()

        self.lift()
        self.update()

    def progresser(self, valeur: int, message: str = ""):
        """Met à jour la barre de progression (0-100)."""
        largeur = int(400 * valeur / 100)
        self.canvas.coords(self.barre, 0, 0, largeur, 12)
        if message:
            self.lbl_status.config(text=message)
        self.update()

