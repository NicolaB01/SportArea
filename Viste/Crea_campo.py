from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow

from Attività.Campo import Campo


class Crea_campo(QMainWindow):
    def __init__(self, pagina_precedente):
        super().__init__()
        uic.loadUi("/Users/nicola/PycharmProjects/ProgettoIDS/UI/SportArea-AggiungiCampo.ui", self)
        self.pagina_precedente = pagina_precedente

        self.pushButton_back.clicked.connect(self.torna_indietro)
        self.pushButton_conferma.clicked.connect(self.crea_campo)

    def crea_campo(self):
        nome = self.lineEdit_nomeCampo.text()
        numero_max_partecipanti = self.spinBox_partecipanti.value()
        prezzo =  self.doubleSpinBox_prezzo.value()
        attività = self.lineEdit_attivita.text()

        Campo.crea_campo(nome, numero_max_partecipanti, prezzo, attività)

        self.torna_indietro()

    def torna_indietro(self):
        self.pagina_precedente.show()
        self.close()