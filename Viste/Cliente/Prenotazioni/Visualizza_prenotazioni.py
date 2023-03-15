from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow

from Path.Path_viste import PATH_VISUALIZZA_PRENOTAZIONI
from Viste.Cliente.Prenotazioni.Prenotazioni_attive import Prenotazioni_attive
from Viste.Cliente.Prenotazioni.Prenotazioni_passate import Prenotazioni_passate


class Visualizza_prenotazioni(QMainWindow):
    def __init__(self, pagina_precedente):
        super().__init__()
        uic.loadUi(PATH_VISUALIZZA_PRENOTAZIONI, self)
        self.pagina_precedente = pagina_precedente

        self.pushButton_prenotzioniAttive.clicked.connect(self.mostra_prenotazioni_attive)
        self.pushButton_prenotazioniPassate.clicked.connect(self.mostra_prenotazioni_passate)
        self.back.clicked.connect(self.torna_indietro)

    def mostra_prenotazioni_attive(self):
        self.prenotazioni_attive = Prenotazioni_attive(self)
        self.prenotazioni_attive.show()
        self.close()

    def mostra_prenotazioni_passate(self):
        self.prenotazioni_passate = Prenotazioni_passate(self)
        self.prenotazioni_passate.show()
        self.close()

    def torna_indietro(self):
        self.pagina_precedente.show()
        self.close()
