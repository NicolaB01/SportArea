from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow

from Viste.Crea_campo import Crea_campo


class Menu_campi(QMainWindow):
    def __init__(self, pagina_precedente):
        super().__init__()
        uic.loadUi("/Users/nicola/PycharmProjects/ProgettoIDS/UI/SportArea-V_Campi.ui", self)
        self.pagina_precedente = pagina_precedente

        self.pushButton_nuovo.clicked.connect(self.menu_nuovo_campo)
        self.pushButton_back.clicked.connect(self.torna_indietro)

    def menu_nuovo_campo(self):
        self.menu_crea_campo = Crea_campo(self)
        self.menu_crea_campo.show()
        self.close()

    def torna_indietro(self):
        self.pagina_precedente.show()
        self.close()