# gui/app.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, time, datetime

BLEU_FONCE  = "#1a3a5c"
BLEU_MOYEN  = "#2563a8"
BLEU_CLAIR  = "#dbeafe"
VERT        = "#16a34a"
ROUGE       = "#dc2626"
ORANGE      = "#d97706"
GRIS_CLAIR  = "#f1f5f9"
BLANC       = "#ffffff"
TEXTE       = "#0f172a"
POLICE      = ("Segoe UI", 10)
POLICE_TITRE= ("Segoe UI", 12, "bold")


class App(tk.Tk):
    def __init__(self, planning, auth_service, notif_service):
        super().__init__()
        self.planning = planning
        self.auth = auth_service
        self.notif = notif_service
        self.user = auth_service.get_utilisateur_connecte()

        self.title(f"Reservation de Salles — {self.user.get_nom_complet()} [{self.user.get_role()}]")
        self.geometry("1100x680")
        self.configure(bg=GRIS_CLAIR)

        self._construire_ui()
        self._actualiser_tout()

    def _construire_ui(self):
        # Header
        header = tk.Frame(self, bg=BLEU_FONCE, height=55)
        header.pack(fill="x")
        tk.Label(header, text="Systeme de Reservation de Salles — Universite de Parakou",
                 font=("Segoe UI", 13, "bold"), bg=BLEU_FONCE, fg=BLANC, pady=15).pack(side="left", padx=20)
        tk.Button(header, text=f"Deconnexion ({self.user.get_prenom()})",
                  font=("Segoe UI", 9), bg="#334155", fg=BLANC, relief="flat",
                  cursor="hand2", command=self._deconnecter).pack(side="right", padx=15, pady=12)

        # Onglets
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=8)

        self.tab_reservation  = tk.Frame(self.notebook, bg=GRIS_CLAIR)
        self.tab_planning     = tk.Frame(self.notebook, bg=GRIS_CLAIR)
        self.tab_salles       = tk.Frame(self.notebook, bg=GRIS_CLAIR)
        self.tab_utilisateurs = tk.Frame(self.notebook, bg=GRIS_CLAIR)
        self.tab_rapports     = tk.Frame(self.notebook, bg=GRIS_CLAIR)
        self.tab_notifications= tk.Frame(self.notebook, bg=GRIS_CLAIR)

        self.notebook.add(self.tab_reservation,  text="  Reservations  ")
        self.notebook.add(self.tab_planning,     text="  Planning  ")
        self.notebook.add(self.tab_salles,       text="  Salles  ")
        self.notebook.add(self.tab_notifications,text="  Notifications  ")
        self.notebook.add(self.tab_rapports,     text="  Rapports  ")
        if self.user.peut_gerer_utilisateurs():
            self.notebook.add(self.tab_utilisateurs, text="  Utilisateurs  ")

        self._build_tab_reservation()
        self._build_tab_planning()
        self._build_tab_salles()
        self._build_tab_notifications()
        self._build_tab_rapports()
        if self.user.peut_gerer_utilisateurs():
            self._build_tab_utilisateurs()

        # Barre de statut
        self.barre_stat = tk.Label(self, text="", font=("Segoe UI", 9),
                                   bg=BLEU_FONCE, fg=BLANC, anchor="w", pady=4)
        self.barre_stat.pack(fill="x", side="bottom")

    # ─── TAB RESERVATIONS ─────────────────────────────────────────────────────
    def _build_tab_reservation(self):
        tab = self.tab_reservation
        corps = tk.Frame(tab, bg=GRIS_CLAIR)
        corps.pack(fill="both", expand=True, padx=10, pady=8)

        # Formulaire
        form = tk.LabelFrame(corps, text=" Nouvelle Reservation ",
                             font=POLICE_TITRE, bg=BLANC, fg=BLEU_FONCE, bd=2)
        form.pack(side="left", fill="y", padx=(0, 8))

        def lbl(texte, row):
            tk.Label(form, text=texte, font=POLICE, bg=BLANC,
                     fg=TEXTE, anchor="w").grid(row=row, column=0,
                     sticky="w", padx=12, pady=5)

        lbl("Salle :", 0)
        noms = [s.get_nom() for s in self.planning.get_salles()]
        self.var_salle = tk.StringVar(value=noms[0] if noms else "")
        self.combo_salle = ttk.Combobox(form, textvariable=self.var_salle,
                                        values=noms, state="readonly", width=22)
        self.combo_salle.grid(row=0, column=1, padx=12, pady=5)

        lbl("Responsable :", 1)
        self.entry_resp = tk.Entry(form, font=POLICE, width=25, bd=1, relief="solid")
        self.entry_resp.insert(0, self.user.get_nom_complet())
        self.entry_resp.grid(row=1, column=1, padx=12, pady=5)

        lbl("Date (JJ/MM/AAAA) :", 2)
        self.entry_date = tk.Entry(form, font=POLICE, width=25, bd=1, relief="solid")
        self.entry_date.insert(0, date.today().strftime("%d/%m/%Y"))
        self.entry_date.grid(row=2, column=1, padx=12, pady=5)

        lbl("Debut (HH:MM) :", 3)
        self.entry_debut = tk.Entry(form, font=POLICE, width=25, bd=1, relief="solid")
        self.entry_debut.insert(0, "08:00")
        self.entry_debut.grid(row=3, column=1, padx=12, pady=5)

        lbl("Fin (HH:MM) :", 4)
        self.entry_fin = tk.Entry(form, font=POLICE, width=25, bd=1, relief="solid")
        self.entry_fin.insert(0, "10:00")
        self.entry_fin.grid(row=4, column=1, padx=12, pady=5)

        lbl("Motif :", 5)
        self.entry_motif = tk.Entry(form, font=POLICE, width=25, bd=1, relief="solid")
        self.entry_motif.grid(row=5, column=1, padx=12, pady=5)

        def btn(texte, color, cmd, row):
            tk.Button(form, text=texte, font=("Segoe UI", 9, "bold"),
                      bg=color, fg=BLANC, relief="flat", cursor="hand2",
                      pady=6, command=cmd).grid(
                      row=row, column=0, columnspan=2, sticky="ew", padx=12, pady=4)

        btn("Reserver", BLEU_MOYEN, self._reserver, 6)
        btn("Salles disponibles", VERT, self._voir_disponibles, 7)
        btn("Supprimer selection", ROUGE, self._supprimer, 8)

        # Tableau
        liste = tk.LabelFrame(corps, text=" Planning des Reservations ",
                              font=POLICE_TITRE, bg=BLANC, fg=BLEU_FONCE, bd=2)
        liste.pack(side="right", fill="both", expand=True)

        cols = ("ID", "Salle", "Date", "Debut", "Fin", "Responsable", "Motif")
        self.tableau_res = ttk.Treeview(liste, columns=cols, show="headings", height=22)
        largeurs = [40, 120, 90, 60, 60, 150, 180]
        for col, larg in zip(cols, largeurs):
            self.tableau_res.heading(col, text=col)
            self.tableau_res.column(col, width=larg, anchor="center")

        sc = ttk.Scrollbar(liste, orient="vertical", command=self.tableau_res.yview)
        self.tableau_res.configure(yscroll=sc.set)
        sc.pack(side="right", fill="y")
        self.tableau_res.pack(fill="both", expand=True, padx=8, pady=8)
        self.tableau_res.tag_configure("pair", background=BLEU_CLAIR)
        self.tableau_res.tag_configure("impair", background=BLANC)

    # ─── TAB PLANNING ─────────────────────────────────────────────────────────
    def _build_tab_planning(self):
        tab = self.tab_planning
        ctrl = tk.Frame(tab, bg=GRIS_CLAIR)
        ctrl.pack(fill="x", padx=10, pady=6)

        tk.Label(ctrl, text="Vue :", font=POLICE, bg=GRIS_CLAIR).pack(side="left")
        self.var_vue = tk.StringVar(value="Journalier")
        for v in ["Journalier", "Hebdomadaire", "Mensuel"]:
            tk.Radiobutton(ctrl, text=v, variable=self.var_vue, value=v,
                           font=POLICE, bg=GRIS_CLAIR,
                           command=self._actualiser_planning).pack(side="left", padx=8)

        tk.Label(ctrl, text="  Date :", font=POLICE, bg=GRIS_CLAIR).pack(side="left")
        self.entry_date_planning = tk.Entry(ctrl, font=POLICE, width=14, bd=1, relief="solid")
        self.entry_date_planning.insert(0, date.today().strftime("%d/%m/%Y"))
        self.entry_date_planning.pack(side="left", padx=5)

        tk.Button(ctrl, text="Afficher", font=POLICE, bg=BLEU_MOYEN, fg=BLANC,
                  relief="flat", cursor="hand2",
                  command=self._actualiser_planning).pack(side="left", padx=8)

        self.text_planning = tk.Text(tab, font=("Courier New", 10),
                                     bg=BLANC, fg=TEXTE, bd=1, relief="solid",
                                     wrap="none")
        sc_p = ttk.Scrollbar(tab, orient="vertical", command=self.text_planning.yview)
        self.text_planning.configure(yscroll=sc_p.set)
        sc_p.pack(side="right", fill="y", padx=(0,10))
        self.text_planning.pack(fill="both", expand=True, padx=10, pady=(0,10))

    # ─── TAB SALLES ───────────────────────────────────────────────────────────
    def _build_tab_salles(self):
        tab = self.tab_salles
        cols = ("ID", "Numero", "Nom", "Type", "Capacite", "Equipements", "Localisation", "Statut")
        self.tableau_salles = ttk.Treeview(tab, columns=cols, show="headings", height=25)
        largeurs = [40, 70, 130, 90, 70, 200, 150, 80]
        for col, larg in zip(cols, largeurs):
            self.tableau_salles.heading(col, text=col)
            self.tableau_salles.column(col, width=larg, anchor="center")

        sc = ttk.Scrollbar(tab, orient="vertical", command=self.tableau_salles.yview)
        self.tableau_salles.configure(yscroll=sc.set)
        sc.pack(side="right", fill="y", pady=10, padx=(0,10))
        self.tableau_salles.pack(fill="both", expand=True, padx=10, pady=10)

        if self.user.peut_gerer_salles():
            barre = tk.Frame(tab, bg=GRIS_CLAIR)
            barre.pack(fill="x", padx=10, pady=(0, 8))
            tk.Button(barre, text="Supprimer salle", font=POLICE,
                      bg=ROUGE, fg=BLANC, relief="flat", cursor="hand2",
                      command=self._supprimer_salle).pack(side="left", padx=5)

    # ─── TAB NOTIFICATIONS ────────────────────────────────────────────────────
    def _build_tab_notifications(self):
        tab = self.tab_notifications
        self.text_notif = tk.Text(tab, font=POLICE, bg=BLANC, fg=TEXTE,
                                  bd=1, relief="solid", state="disabled")
        sc = ttk.Scrollbar(tab, orient="vertical", command=self.text_notif.yview)
        self.text_notif.configure(yscroll=sc.set)
        sc.pack(side="right", fill="y", pady=10, padx=(0,10))
        self.text_notif.pack(fill="both", expand=True, padx=10, pady=10)

    # ─── TAB RAPPORTS ─────────────────────────────────────────────────────────
    def _build_tab_rapports(self):
        tab = self.tab_rapports
        self.text_rapport = tk.Text(tab, font=("Courier New", 10),
                                    bg=BLANC, fg=TEXTE, bd=1, relief="solid",
                                    state="disabled")
        sc = ttk.Scrollbar(tab, orient="vertical", command=self.text_rapport.yview)
        self.text_rapport.configure(yscroll=sc.set)
        sc.pack(side="right", fill="y", pady=10, padx=(0,10))
        self.text_rapport.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Button(tab, text="Actualiser rapport", font=POLICE,
                  bg=BLEU_MOYEN, fg=BLANC, relief="flat", cursor="hand2",
                  command=self._actualiser_rapport).pack(pady=4)

    # ─── TAB UTILISATEURS ─────────────────────────────────────────────────────
    def _build_tab_utilisateurs(self):
        tab = self.tab_utilisateurs
        cols = ("ID", "Nom", "Prenom", "Email", "Role", "Actif")
        self.tableau_users = ttk.Treeview(tab, columns=cols, show="headings", height=20)
        for col in cols:
            self.tableau_users.heading(col, text=col)
            self.tableau_users.column(col, width=150, anchor="center")

        sc = ttk.Scrollbar(tab, orient="vertical", command=self.tableau_users.yview)
        self.tableau_users.configure(yscroll=sc.set)
        sc.pack(side="right", fill="y", pady=10, padx=(0,10))
        self.tableau_users.pack(fill="both", expand=True, padx=10, pady=10)

        barre = tk.Frame(tab, bg=GRIS_CLAIR)
        barre.pack(fill="x", padx=10, pady=(0,8))
        tk.Button(barre, text="Supprimer utilisateur", font=POLICE,
                  bg=ROUGE, fg=BLANC, relief="flat", cursor="hand2",
                  command=self._supprimer_utilisateur).pack(side="left", padx=5)
        tk.Button(barre, text="Ajouter utilisateur", font=POLICE,
                  bg=VERT, fg=BLANC, relief="flat", cursor="hand2",
                  command=self._ajouter_utilisateur).pack(side="left", padx=5)

    # ─── ACTIONS ──────────────────────────────────────────────────────────────
    def _reserver(self):
        try:
            from models.reservation import Reservation
            salle = self.planning.get_salle_par_nom(self.var_salle.get())
            resp  = self.entry_resp.get().strip()
            d     = datetime.strptime(self.entry_date.get(), "%d/%m/%Y").date()
            h1    = datetime.strptime(self.entry_debut.get(), "%H:%M").time()
            h2    = datetime.strptime(self.entry_fin.get(),   "%H:%M").time()
            motif = self.entry_motif.get().strip()

            if not resp:
                messagebox.showwarning("Champ manquant", "Saisissez le responsable.")
                return
            if h2 <= h1:
                messagebox.showwarning("Horaire invalide", "Heure fin > Heure debut.")
                return

            res = Reservation(salle, resp, d, h1, h2, motif)
            succes, msg = self.planning.ajouter_reservation(res)

            if succes:
                self.notif.confirmation_reservation(res, self.user.get_nom_complet())
                messagebox.showinfo("Succes", msg)
                self._actualiser_tout()
            else:
                # Proposer des creneaux alternatifs
                creneaux = self.planning.proposer_creneaux(salle, d)
                suggestion = ""
                if creneaux:
                    suggestion = "\n\nCreneaux disponibles pour cette salle :\n"
                    for c in creneaux[:3]:
                        suggestion += f"   {c[0].strftime('%H:%M')} -> {c[1].strftime('%H:%M')}\n"
                messagebox.showerror("Conflit detecte", msg + suggestion)

        except ValueError as e:
            messagebox.showerror("Erreur", f"Format incorrect :\n{e}\nEx: 22/04/2026  |  08:00")

    def _supprimer(self):
        sel = self.tableau_res.selection()
        if not sel:
            messagebox.showwarning("Aucune selection", "Selectionnez une reservation.")
            return
        rid = int(self.tableau_res.item(sel[0])["values"][0])
        r = self.planning.get_reservation_par_id(rid)
        if messagebox.askyesno("Confirmer", f"Annuler la reservation #{rid} ?"):
            self.notif.annulation_reservation(r, self.user.get_nom_complet())
            self.planning.supprimer_reservation(rid)
            self._actualiser_tout()

    def _voir_disponibles(self):
        try:
            d  = datetime.strptime(self.entry_date.get(), "%d/%m/%Y").date()
            h1 = datetime.strptime(self.entry_debut.get(), "%H:%M").time()
            h2 = datetime.strptime(self.entry_fin.get(),   "%H:%M").time()
            dispo = self.planning.get_salles_disponibles(d, h1, h2)
            if dispo:
                liste = "\n".join(f"  {s.get_info()}" for s in dispo)
                messagebox.showinfo("Salles disponibles",
                                    f"Creneaux libres le {d.strftime('%d/%m/%Y')} "
                                    f"{h1.strftime('%H:%M')} -> {h2.strftime('%H:%M')} :\n\n{liste}")
            else:
                messagebox.showwarning("Aucune salle libre",
                                       "Toutes les salles sont occupees sur ce creneau.")
        except ValueError:
            messagebox.showerror("Erreur", "Verifiez la date et les heures.")

    def _supprimer_salle(self):
        sel = self.tableau_salles.selection()
        if not sel:
            messagebox.showwarning("Aucune selection", "Selectionnez une salle.")
            return
        sid = int(self.tableau_salles.item(sel[0])["values"][0])
        if messagebox.askyesno("Confirmer", "Supprimer cette salle ?"):
            self.planning.supprimer_salle(sid)
            self._actualiser_tout()

    def _supprimer_utilisateur(self):
        sel = self.tableau_users.selection()
        if not sel:
            messagebox.showwarning("Aucune selection", "Selectionnez un utilisateur.")
            return
        uid = int(self.tableau_users.item(sel[0])["values"][0])
        if messagebox.askyesno("Confirmer", "Supprimer cet utilisateur ?"):
            self.auth.supprimer_utilisateur(uid)
            self._actualiser_utilisateurs()

    def _ajouter_utilisateur(self):
        fenetre = tk.Toplevel(self)
        fenetre.title("Ajouter un utilisateur")
        fenetre.geometry("350x350")
        fenetre.configure(bg=GRIS_CLAIR)
        fenetre.resizable(False, False)

        champs = {}
        for i, (label, defaut) in enumerate([
            ("Nom", ""), ("Prenom", ""), ("Email", "@up.bj"),
            ("Mot de passe", ""), ("Role (administrateur/enseignant/agent)", "enseignant")
        ]):
            tk.Label(fenetre, text=label, font=POLICE, bg=GRIS_CLAIR).pack(pady=(8, 0))
            e = tk.Entry(fenetre, font=POLICE, width=30, bd=1, relief="solid")
            e.insert(0, defaut)
            if "passe" in label.lower():
                e.config(show="*")
            e.pack()
            champs[label] = e

        def valider():
            vals = [e.get().strip() for e in champs.values()]
            succes, msg = self.auth.creer_compte(*vals)
            if succes:
                messagebox.showinfo("Succes", msg)
                self._actualiser_utilisateurs()
                fenetre.destroy()
            else:
                messagebox.showerror("Erreur", msg)

        tk.Button(fenetre, text="Creer le compte", font=("Segoe UI", 10, "bold"),
                  bg=BLEU_MOYEN, fg=BLANC, relief="flat", cursor="hand2",
                  command=valider).pack(pady=15, ipadx=10, ipady=5)

    def _deconnecter(self):
        if messagebox.askyesno("Deconnexion", "Voulez-vous vous deconnecter ?"):
            self.auth.deconnecter()
            self.destroy()

    # ─── ACTUALISATION ────────────────────────────────────────────────────────
    def _actualiser_tout(self):
        self._actualiser_liste_reservations()
        self._actualiser_salles()
        self._actualiser_planning()
        self._actualiser_notifications()
        self._actualiser_rapport()
        if self.user.peut_gerer_utilisateurs():
            self._actualiser_utilisateurs()
        self._maj_barre()

    def _actualiser_liste_reservations(self):
        for row in self.tableau_res.get_children():
            self.tableau_res.delete(row)
        for i, r in enumerate(self.planning.get_reservations()):
            tag = "pair" if i % 2 == 0 else "impair"
            self.tableau_res.insert("", "end", tags=(tag,), values=(
                r.get_id(), r.get_salle().get_nom(),
                r.get_date().strftime("%d/%m/%Y"),
                r.get_heure_debut().strftime("%H:%M"),
                r.get_heure_fin().strftime("%H:%M"),
                r.get_responsable(), r.get_motif()
            ))

    def _actualiser_salles(self):
        for row in self.tableau_salles.get_children():
            self.tableau_salles.delete(row)

        for s in self.planning.get_salles():
            self.tableau_salles.insert("", "end", values=(
                s.get_id(),
                s.get_numero(),
                s.get_nom(),
                s.get_type(),
                s.get_capacite(),
                s.nom_equipements(),  # ✅ CORRECTION ICI
                s.get_localisation(),
                "Disponible" if s.est_disponible() else "Indisponible"
            ))

    def _actualiser_planning(self):
        self.text_planning.config(state="normal")
        self.text_planning.delete("1.0", "end")
        try:
            d = datetime.strptime(self.entry_date_planning.get(), "%d/%m/%Y").date()
        except:
            d = date.today()

        vue = self.var_vue.get()
        if vue == "Journalier":
            res = self.planning.get_reservations_par_date(d)
            titre = f"Planning du {d.strftime('%d/%m/%Y')}"
        elif vue == "Hebdomadaire":
            res = self.planning.get_reservations_semaine(d)
            titre = f"Planning de la semaine du {d.strftime('%d/%m/%Y')}"
        else:
            res = self.planning.get_reservations_mois(d.year, d.month)
            titre = f"Planning du mois {d.strftime('%m/%Y')}"

        self.text_planning.insert("end", f"{'='*70}\n{titre}\n{'='*70}\n\n")
        if not res:
            self.text_planning.insert("end", "  Aucune reservation sur cette periode.\n")
        else:
            for r in sorted(res, key=lambda x: (x.get_date(), x.get_heure_debut())):
                self.text_planning.insert("end",
                    f"  [{r.get_date().strftime('%d/%m')}] "
                    f"{r.get_heure_debut().strftime('%H:%M')} - {r.get_heure_fin().strftime('%H:%M')}"
                    f"  |  {r.get_salle().get_nom():<20}"
                    f"  |  {r.get_responsable():<20}"
                    f"  |  {r.get_motif()}\n"
                )
        self.text_planning.config(state="disabled")

    def _actualiser_notifications(self):
        self.text_notif.config(state="normal")
        self.text_notif.delete("1.0", "end")
        notifs = self.notif.get_notifications(self.user.get_nom_complet())
        if not notifs:
            self.text_notif.insert("end", "  Aucune notification.\n")
        else:
            for n in reversed(notifs):
                self.text_notif.insert("end", f"  {n}\n")
        self.text_notif.config(state="disabled")

    def _actualiser_rapport(self):
        self.text_rapport.config(state="normal")
        self.text_rapport.delete("1.0", "end")
        stats = self.planning.get_statistiques()
        lignes = [
            "=" * 60,
            "  RAPPORT STATISTIQUE — SYSTEME DE RESERVATION",
            "  Universite de Parakou",
            "=" * 60,
            f"\n  Total reservations     : {stats['total_reservations']}",
            f"  Total salles           : {stats['total_salles']}",
            f"  Salle plus utilisee    : {stats['salle_plus_utilisee']}",
            "\n  TAUX D'OCCUPATION PAR SALLE :",
            "-" * 40,
        ]
        for nom, taux in stats["taux_occupation"].items():
            nb = stats["compteur_par_salle"].get(nom, 0)
            barre = "#" * int(taux / 5)
            lignes.append(f"  {nom:<20} {barre:<20} {taux}% ({nb} res.)")
        self.text_rapport.insert("end", "\n".join(lignes))
        self.text_rapport.config(state="disabled")

    def _actualiser_utilisateurs(self):
        for row in self.tableau_users.get_children():
            self.tableau_users.delete(row)
        for u in self.auth.get_tous_utilisateurs():
            self.tableau_users.insert("", "end", values=(
                u.get_id(), u.get_nom(), u.get_prenom(),
                u.get_email(), u.get_role(),
                "Oui" if u.est_actif() else "Non"
            ))

    def _maj_barre(self):
        stats = self.planning.get_statistiques()
        non_lues = len(self.notif.get_non_lues(self.user.get_nom_complet()))
        self.barre_stat.config(
            text=f"  Reservations: {stats['total_reservations']}  |  "
                 f"Salles: {stats['total_salles']}  |  "
                 f"Notifications non lues: {non_lues}  |  "
                 f"Connecte: {self.user.get_nom_complet()} [{self.user.get_role()}]"
        )

