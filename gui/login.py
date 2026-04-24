# gui/login.py
import tkinter as tk
from tkinter import messagebox

from gui.splash import BLEU_CLAIR

BLEU_FONCE = "#1a3a5c"
BLEU_MOYEN = "#2563a8"
BLANC      = "#ffffff"
GRIS_CLAIR = "#f1f5f9"
TEXTE      = "#0f172a"
POLICE     = ("Segoe UI", 10)

class LoginWindow(tk.Tk):
    """Fenêtre de connexion au système."""

    def __init__(self, auth_service):
        super().__init__()
        self.auth = auth_service
        self.utilisateur_connecte = None

        self.title("Authentification ")
        self.geometry("800x700")
        self.resizable(False, False)
        self.configure(bg=GRIS_CLAIR)

        self._construire_ui()
        self.eval('tk::PlaceWindow . center')

    def _construire_ui(self):
        # En-tête
        header = tk.Frame(self, bg=BLEU_CLAIR)
        header.pack(fill="x")
        tk.Label(header, text="🏫", font=("Segoe UI", 36),
                 bg=BLEU_FONCE, fg=BLANC, pady=20).pack()

        tk.Label(header, text="Système de Réservation de Salles",
                 font=("Segoe UI", 9), bg=BLEU_FONCE, fg="#93c5fd", pady=8).pack()

        # Formulaire
        cadre = tk.Frame(self, bg=GRIS_CLAIR, pady=20)
        cadre.pack(fill="both", expand=True, padx=40)

        tk.Label(cadre, text="Email", font=("Segoe UI", 9, "bold"),
                 bg=GRIS_CLAIR, fg=TEXTE, anchor="w").pack(fill="x", pady=(18, 5))
        self.entry_email = tk.Entry(cadre, font=POLICE, bd=1, relief="solid",
                                    fg=TEXTE, bg=BLANC)
        self.entry_email.pack(fill="x", ipady=6)
        self.entry_email.insert(0, "admin@up.bj")

        tk.Label(cadre, text="Mot de passe", font=("Segoe UI", 9, "bold"),
                 bg=GRIS_CLAIR, fg=TEXTE, anchor="w").pack(fill="x", pady=(12, 2))
        self.entry_mdp = tk.Entry(cadre, font=POLICE, bd=1, relief="solid",
                                  show="*", fg=TEXTE, bg=BLANC)
        self.entry_mdp.pack(fill="x", ipady=6)
        self.entry_mdp.insert(0, "admin123")

        self.lbl_erreur = tk.Label(cadre, text="", fg="#dc2626",
                                   bg=GRIS_CLAIR, font=("Segoe UI", 9))
        self.lbl_erreur.pack(pady=5)

        tk.Button(cadre, text="Se connecter", font=("Segoe UI", 10, "bold"),
                  bg=BLEU_MOYEN, fg=BLANC, relief="flat", cursor="hand2",
                  pady=8, command=self._connecter).pack(fill="x", pady=5)

        # Comptes de démo
        tk.Label(cadre, text="Comptes de démonstration :",
                 font=("Segoe UI", 8, "bold"), bg=GRIS_CLAIR, fg="#64748b").pack(pady=(15, 2))
        demos = [
            ("Admin",     "admin@up.bj",    ""),
            ("Enseignant","k.adjonou@up.bj",""),
            ("Agent",     "m.bello@up.bj",  "agent123"),
            ("Agent", " ", "")

        ]
        for role, email, mdp in demos:
            tk.Label(cadre, text=f"{role}: {email} / {mdp}",
                     font=("Segoe UI", 8), bg=GRIS_CLAIR, fg="#94a3b8").pack()

        # Bind Enter
        self.bind("<Return>", lambda e: self._connecter())

    def _connecter(self):
        email = self.entry_email.get().strip()
        mdp   = self.entry_mdp.get().strip()

        if not email or not mdp:
            self.lbl_erreur.config(text="Veuillez remplir tous les champs.")
            return

        succes, message = self.auth.connecter(email, mdp)
        if succes:
            self.utilisateur_connecte = self.auth.get_utilisateur_connecte()
            self.destroy()
        else:
            self.lbl_erreur.config(text=message)

