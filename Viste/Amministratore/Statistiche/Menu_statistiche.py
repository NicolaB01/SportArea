from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow

from Path.Path_viste import PATH_MENU_STATISTICHE
from Viste.Amministratore.Statistiche.Statistiche_attivita import Statistiche_attivita
from Viste.Amministratore.Statistiche.Statistiche_eta import Statistiche_eta
from Viste.Amministratore.Statistiche.Statistiche_fatturato import Statistiche_fatturato
from Viste.Amministratore.Statistiche.Statistiche_iscrizioni import Statistiche_iscrizioni


class Menu_statistiche(QMainWindow):
    def __init__(self, pagina_precedente):
        super().__init__()
        uic.loadUi(PATH_MENU_STATISTICHE, self)
        self.pagina_precedente = pagina_precedente


        self.numero_iscrizioni.clicked.connect(self.stat1)
        self.età_media.clicked.connect(self.stat2)
        self.btn_attività.clicked.connect(self.stat3)
        self.fatturato.clicked.connect(self.stat4)
        self.back.clicked.connect(self.torna_indietro)

    def stat1(self):
        self.stat1 = Statistiche_iscrizioni(self)
        self.stat1.show()
        self.close()

    def stat2(self):
        self.stat2 = Statistiche_eta(self)
        self.stat2.show()
        self.close()

    def stat3(self):
        self.stat3 = Statistiche_attivita(self)
        self.stat3.show()
        self.close()

    def stat4(self):
        self.stat4 = Statistiche_fatturato(self)
        self.stat4.show()
        self.close()

    def torna_indietro(self):
        self.pagina_precedente.show()
        self.close()