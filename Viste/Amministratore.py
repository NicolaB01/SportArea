from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow

from Viste.Menu_campi import Menu_campi


class Amministratore(QMainWindow):
    def __init__(self, pagina_precedente):
        super().__init__()
        uic.loadUi("/Users/nicola/PycharmProjects/ProgettoIDS/UI/SportArea-Amministrazione.ui", self)
        self.pagina_precedente = pagina_precedente

        self.struttura.clicked.connect(self.menu_campi)
        self.logout.clicked.connect(self.torna_indietro)

    def menu_campi(self):
        self.campi = Menu_campi(self)
        self.campi.show()
        self.close()

    def torna_indietro(self):
        self.pagina_precedente.email.clear()
        self.pagina_precedente.pwd.clear()

        self.pagina_precedente.show()
        self.close()