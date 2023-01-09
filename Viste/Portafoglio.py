from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow

from Attività.Cliente import Cliente
from Viste.Modifica_account import Modifica_account


class Portafoglio(QMainWindow):
    def __init__(self, pagina_precedente):
        super().__init__()
        uic.loadUi("/Users/nicola/PycharmProjects/ProgettoIDS/UI/SportArea-Portafoglio.ui", self)
        self.pagina_precedente = pagina_precedente
        self.cliente = Cliente.get_account_connesso()
        self.refresh()

        self.pushButton_ricarica.clicked.connect(self.ricarica)
        self.back.clicked.connect(self.torna_indietro)

    def ricarica(self):
        self.cliente.deposito(self.doubleSpinBox_ricarica.value())
        self.refresh()


    def torna_indietro(self):
        self.pagina_precedente.show()
        self.close()

    def refresh(self):
        self.label_saldo.setText(str(self.cliente.saldo))