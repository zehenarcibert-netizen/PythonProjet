# tests/test_reservation.py
#commande pour lancer : pytest tests/-v

import sys , os

from bloc2 import equipements_salle_A
from exceptions.bloc5_exceptions_demo import reservations

sys.path.insert(0, os.path.join(os.path. dirname(__file__), ".."))

import  pytest
from datetime import date, time
from  models.reservation import Reservation
from models.salle import Salle
from models.utilisateur import Utilisateur
from service.planning import Planning
from service.auth import AuthService

#--------fixture(données de test réutilisable )----------
@pytest.fixture
def salle_test():
    return Salle("T01", "Salle Test", "Batiment Test", 30, "TD")

@pytest.fixture
def planning_avec_salle(salle_test, salle_amphi):
    p = Planning()
    p.ajouter_salle(salle_test)
    p.ajouter_salle(salle_amphi)
    return p
@pytest.fixture
def date_test():
    return date.today()

#----------TEST: Sallle---------------------------
class TestSalle:
    def test_creation_salle(self, salle_test):
        assert salle_test.get_nom()== "Salle Test"
        assert salle_test.get_capacite()== 50
        assert salle_test.get_type()== "TD"
        assert salle_test.est_disponible() is True
    def test_salle_a_un_id_unique(self):
        s1 = Salle("X01", "Salle X1", "Bat X", 20,"cours")
        s2= Salle("X02", "Salle X2", "Bat X", 20,"cours")
        assert s1.get_id() != s2.get_id()
    def test_ajouter_equipement(self, salle_test):
        from models.equipement import Equipement
        eq = Equipement("Proj-01", "salle Test", "Projecteur", "Epson")
        salle_test.ajouter_equipement(eq)
        assert  len(salle_test.get_equipement())== 1
        assert "Projecteur" in salle_test.get_equipement()
    def test_modifier_capacite(self, salle_test):
        salle_test.set_capacite(100)
        assert salle_test.get_capacite()== 100
    def test_get_info_contien_nom(self, salle_test):
        assert "salle Test" in salle_test.get_info()

#------TEST: réservation------------
class TestReservation:
    def test_creation_reservation(self, salle_test, date_test):
        r = Reservation(salle_test, "prof.A", date_test,time(8, 0), time(10, 0), "cours")
        assert r.get_responsable() == "Prof.A"
        assert r.get_heure_debut() === time(8, 0)
        assert r.get_heure_fin()== time(10,0)
        assert r.get_motif() =="cours"


    def test_pas_de_conflit_salle_different(self, salle_test, date_test):
        s1 = Salle("C1", "Salle C1", "Bat C", 25,"TD")
        s2 = Salle("C2", "Salle C2", "Bat C", 25,"TD")
        r1 = Reservation(s1, "prof.A", date_test, time(8, 0), time(10, 0), " ")
        r2 = Reservation(s2, "prof.B", date_test, time(8, 0), time(10, 0), " ")
        assert r1.est_en_conflit(r2) is False

    def test_pas_de_conflit_dates_differentes(self, salle_test, date_test):
        r1 = Reservation(salle_test,"Prof.A", date(2026, 4, 24), time(8, 0), time(10, 0), " ")
        r2 = Reservation(salle_test,"Prof.B", date(2026, 4, 25), time(8, 0), time(10, 0), " ")
        assert r1.est_en_conflit(r2) is False

    def test_conflit_chevauchement_partielle(self, salle_test, date_test):
        r1 = Reservation(salle_test, "Prof.A", date_test, time(8, 0), time(10, 0), " ")
        r2 = Reservation(salle_test, "Prof.B", date_test, time(9, 0), time(11, 0), " ")
        assert r1.est_en_conflit(r2) is True

    def test_conflit_reservation_incluse(self, salle_test, date_test):
        r1 = Reservation(salle_test, "Prof.A", date_test, time(8, 0), time(12, 0), " ")
        r2 = Reservation(salle_test, "Prof.B", date_test, time(9, 0), time(11, 0), " ")
        assert r1.est_en_conflit(r2) is True

    def test_pas_de_conflit_consecutif(self, salle_test, date_test):
        r1 = Reservation(salle_test, "Prof.A", date_test, time(8, 0), time(10, 0), " ")
        r2 = Reservation(salle_test, "Prof.B", date_test, time(10, 0), time(12, 0), " ")
        assert r1.est_en_conflit(r2) is False

    def test_id_reservation_unique(self, salle_test, date_test):
        r1 = Reservation(salle_test, "Prof.A", date_test, time(8, 0), time(10, 0), " ")
        r2 = Reservation(salle_test, "Prof.B", date_test, time(10, 0), time(12, 0), " ")
        assert r1.get_id() != r2.get_id()

#----------- Test : planning------------
class TestPlanning:
    def test_ajouter_salle(self,planning_avec_salle):
        assert len(planning_avec_salle.get_equipement())== 2
    def test_reservation_sans_conflit(self, planning_avec_salle, salle_test,date_test):
        r = Reservation(salle_test, "Prof.A", date_test, time(8, 0), time(10, 0), " ")
        succes, _ = planning_avec_salle.ajouter_salle(r)
        assert succes is True
    def test_reservation_avec_conflit(self, planning_avec_salle, salle_test,date_test):
        r1  = Reservation(salle_test, "Prof.A", date_test, time(8, 0), time(10, 0), " ")
        r2 = Reservation(salle_test, "Prof.B", date_test, time(9, 0),time(11, 0), " ")
        planning_avec_salle.ajouter_reservation(r1)
        succes, msg = planning_avec_salle.ajouter_reservation(r2)
        assert succes is False
        assert " Conflit" in msg or "Conflict" in msg.lower()
    def test_suprimer_reservation(self, planning_avec_salle, salle_test,date_test):
        r = Reservation(salle_test, "Prof.A", date_test, time(8, 0), time(10, 0), " ")
        planning_avec_salle.ajouter_reservation(r)
        rid = r.get_id()
        result = planning_avec_salle.suprimer_reservation(rid)
        assert result is True
    def test_get_salles_disponible(self, planning_avec_salle, salle_test,date_test):
        r = Reservation(salle_test, "Prof.A", date_test, time(8, 0), time(10, 0), " ")
        planning_avec_salle.ajouter_reservation(r)
        dispo = planning_avec_salle.get_salles_disponible(date_test, time(8, 0),time(10,0))
        noms = [s.get_nom() for s in dispo]
        assert "salle Test "not in noms
        assert "Amphi Test" in noms
    def test_get_statistique(self, planning_avec_salle, salle_test,date_test):
        r = Reservation(salle_test, "Prof.A", date_test, time(8, 0), time(10, 0), " ")
        planning_avec_salle.ajouter_reservation(r)
        stats = planning_avec_salle.get_statistique()
        assert stats ["total_reservations"] >= 1
        assert "total_salles" in stats

# ─── TESTS : UTILISATEUR & AUTH ─-----────
    class TestAuth:
    def test_connexion_correcte(self):
        auth = AuthService()
        succes, msg = auth.connecter("admin@up.bj", "admin123")
        assert succes is True
        assert auth.est_connecte() is True

    def test_connexion_mauvais_mdp(self):
        auth = AuthService()
        succes, _ = auth.connecter("admin@up.bj", "mauvais")
        assert succes is False

    def test_connexion_email_inconnu(self):
        auth = AuthService()
        succes, _ = auth.connecter("inconnu@up.bj", "admin123")
        assert succes is False

    def test_creer_compte(self):
        auth = AuthService()
        succes, _ = auth.creer_compte("Test", "User", "test@up.bj", "mdp123", "enseignant")
        assert succes is True

    def test_email_duplique(self):
        auth = AuthService()
        auth.creer_compte("Test", "User", "double@up.bj", "mdp", "enseignant")
        succes, _ = auth.creer_compte("Test2", "User2", "double@up.bj", "mdp", "enseignant")
        assert succes is False

    def test_role_administrateur(self):
        u = Utilisateur("Admin", "Super", "a@up.bj", "mdp", "administrateur")
        assert u.peut_gerer_utilisateurs() is True
        assert u.peut_gerer_salles() is True

    def test_role_enseignant(self):
        u = Utilisateur("Prof", "Kofi", "p@up.bj", "mdp", "enseignant")
        assert u.peut_gerer_utilisateurs() is False
        assert u.peut_gerer_salles() is False

