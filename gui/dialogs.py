# gui/dialogs.py
# BLOC 6 — Boîtes de dialogue réutilisables

import tkinter as tk
from tkinter import ttk, messagebox

BLEU_FONCE = "#1a3a5c"
BLEU_MOYEN = "#2563a8"
VERT       = "#16a34a"
ROUGE      = "#dc2626"
BLANC      = "#ffffff"
GRIS_CLAIR = "#f1f5f9"
POLICE     = ("Segoe UI", 15)


class DialogueAjoutSalle(tk.Toplevel):
    """Dialogue pour ajouter une nouvelle salle."""

    def __init__(self, parent, planning, callback):
        super().__init__(parent)
        self.planning  = planning
        self.callback  = callback   # Fonction appelée après ajout
        self.title("Ajouter une salle")
        self.geometry("380x700")
        self.resizable(False, False)
        self.configure(bg=GRIS_CLAIR)
        self.grab_set()             # Fenêtre modale
        self._construire()
        self._centrer()

    def _centrer(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth()  - 380) // 2
        y = (self.winfo_screenheight() - 400) // 2
        self.geometry(f"380x400+{x}+{y}")

    def _construire(self):
        tk.Label(self, text="Nouvelle Salle", font=("Segoe UI", 13, "bold"),
                 bg=GRIS_CLAIR, fg=BLEU_FONCE).pack(pady=15)

        cadre = tk.Frame(self, bg=GRIS_CLAIR)
        cadre.pack(padx=30, fill="x")

        self.champs = {}
        for label, defaut in [
            ("Numéro", "B101"),
            ("Nom", "Salle B101"),
            ("Localisation", "Bâtiment B"),
            ("Capacité", "40"),
        ]:
            tk.Label(cadre, text=label, font=("Segoe UI", 9, "bold"),
                     bg=GRIS_CLAIR, fg="#374151", anchor="w").pack(fill="x", pady=(8, 1))
            e = tk.Entry(cadre, font=POLICE, bd=1, relief="solid")
            e.insert(0, defaut)
            e.pack(fill="x", ipady=5)
            self.champs[label] = e

        tk.Label(cadre, text="Type", font=("Segoe UI", 9, "bold"),
                 bg=GRIS_CLAIR, fg="#374151", anchor="w").pack(fill="x", pady=(8, 1))
        self.var_type = tk.StringVar(value="Cours")
        ttk.Combobox(cadre, textvariable=self.var_type,
                     values=["Cours", "TD", "Amphi", "Réunion", "Informatique"],
                     state="readonly").pack(fill="x")

        tk.Button(self, text="✅ Ajouter la salle",
                  font=("Segoe UI", 10, "bold"),
                  bg=VERT, fg=BLANC, relief="flat", cursor="hand2",
                  pady=8, command=self._valider).pack(fill="x", padx=30, pady=20)

    def _valider(self):
        try:
            from models.salle import Salle
            numero  = self.champs["Numéro"].get().strip()
            nom     = self.champs["Nom"].get().strip()
            loc     = self.champs["Localisation"].get().strip()
            cap     = int(self.champs["Capacité"].get())
            type_s  = self.var_type.get()

            if not all([numero, nom, loc]):
                messagebox.showwarning("Champs manquants",
                                       "Remplissez tous les champs.", parent=self)
                return
            if cap <= 0:
                messagebox.showwarning("Capacité invalide",
                                       "La capacité doit être > 0.", parent=self)
                return

            salle = Salle(numero, nom, loc, cap, type_s)
            self.planning.ajouter_salle(salle)
            messagebox.showinfo("Succès", f"Salle '{nom}' ajoutée !", parent=self)
            self.callback()
            self.destroy()

        except ValueError:
            messagebox.showerror("Erreur", "La capacité doit être un nombre entier.",
                                 parent=self)


class DialogueModifierReservation(tk.Toplevel):
    """Dialogue pour modifier une réservation existante."""

    def __init__(self, parent, reservation, planning, callback):
        super().__init__(parent)
        self.reservation = reservation
        self.planning    = planning
        self.callback    = callback
        self.title(f"Modifier Réservation #{reservation.get_id()}")
        self.geometry("380x320")
        self.resizable(False, False)
        self.configure(bg=GRIS_CLAIR)
        self.grab_set()
        self._construire()

    def _construire(self):
        r = self.reservation
        tk.Label(self, text=f"Modifier #{r.get_id()} — {r.get_salle().get_nom()}",
                 font=("Segoe UI", 11, "bold"),
                 bg=GRIS_CLAIR, fg=BLEU_FONCE).pack(pady=12)

        cadre = tk.Frame(self, bg=GRIS_CLAIR)
        cadre.pack(padx=30, fill="x")

        self.champs = {}
        for label, defaut in [
            ("Date (JJ/MM/AAAA)", r.get_date().strftime("%d/%m/%Y")),
            ("Heure début",       r.get_heure_debut().strftime("%H:%M")),
            ("Heure fin",         r.get_heure_fin().strftime("%H:%M")),
            ("Motif",             r.get_motif()),
        ]:
            tk.Label(cadre, text=label, font=("Segoe UI", 9, "bold"),
                     bg=GRIS_CLAIR, fg="#374151", anchor="w").pack(fill="x", pady=(6, 1))
            e = tk.Entry(cadre, font=POLICE, bd=1, relief="solid")
            e.insert(0, defaut)
            e.pack(fill="x", ipady=5)
            self.champs[label] = e

        tk.Button(self, text="💾 Enregistrer",
                  font=("Segoe UI", 10, "bold"),
                  bg=BLEU_MOYEN, fg=BLANC, relief="flat", cursor="hand2",
                  pady=8, command=self._valider).pack(fill="x", padx=30, pady=15)

    def _valider(self):
        from datetime import datetime
        try:
            d  = datetime.strptime(self.champs["Date (JJ/MM/AAAA)"].get(), "%d/%m/%Y").date()
            h1 = datetime.strptime(self.champs["Heure début"].get(), "%H:%M").time()
            h2 = datetime.strptime(self.champs["Heure fin"].get(), "%H:%M").time()
            motif = self.champs["Motif"].get().strip()

            if h2 <= h1:
                messagebox.showwarning("Horaire invalide",
                                       "Heure fin doit être après heure début.", parent=self)
                return

            self.reservation.set_date(d)
            self.reservation.set_heure_debut(h1)
            self.reservation.set_heure_fin(h2)
            self.reservation.set_motif(motif)

            messagebox.showinfo("Succès", "Réservation modifiée !", parent=self)
            self.callback()
            self.destroy()

        except ValueError as e:
            messagebox.showerror("Erreur", f"Format incorrect :\n{e}", parent=self)

