from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow

from Path.Path_viste import PATH_HOME_AMMINISTRATORE
from Viste.Amministratore.Statistiche.Menu_statistiche import Menu_statistiche
from Viste.Amministratore.Struttura.Menu_campi import Menu_campi
from Viste.Amministratore.Visualizza_clienti import Visualizza_clienti
from Viste.Amministratore.Visualizza_ricevute import Visualizza_ricevute


class Amministratore(QMainWindow):
    def __init__(self, pagina_precedente):
        super().__init__()
        uic.loadUi(PATH_HOME_AMMINISTRATORE, self)
        self.pagina_precedente = pagina_precedente

        self.clienti.clicked.connect(self.mostra_clienti)
        self.statistiche.clicked.connect(self.menu_statistiche)
        self.ricevute.clicked.connect(self.mostra_ricevute)
        self.struttura.clicked.connect(self.menu_campi)
        self.logout.clicked.connect(self.torna_indietro)

    def menu_statistiche(self):
        self.menu_statistiche = Menu_statistiche(self)
        self.menu_statistiche.show()
        self.close()

    def mostra_clienti(self):
        self.visualizza_clienti = Visualizza_clienti(self)
        self.visualizza_clienti.show()
        self.close()

    def mostra_ricevute(self):
        self.visualizza_ricevute = Visualizza_ricevute(self)
        self.visualizza_ricevute.show()
        self.close()

    def menu_campi(self):
        self.campi = Menu_campi(self)
        self.campi.show()
        self.close()

    def torna_indietro(self):
        self.pagina_precedente.show()
        self.close()