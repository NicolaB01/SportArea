from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow

from Attività.Cliente import Cliente
from Path.Path_viste import PATH_PORTAFOGLIO


class Portafoglio(QMainWindow):
    def __init__(self, pagina_precedente):
        super().__init__()
        uic.loadUi(PATH_PORTAFOGLIO, self)
        self.pagina_precedente = pagina_precedente
        self.cliente = Cliente.get_account_connesso()

        self.refresh()

        self.pushButton_ricarica.clicked.connect(self.ricarica)
        self.back.clicked.connect(self.torna_indietro)

    def refresh(self):
        self.label_saldo.setText(str(self.cliente.get_saldo()))

    def ricarica(self):
        self.cliente.deposito(self.doubleSpinBox_ricarica.value())
        self.doubleSpinBox_ricarica.setValue(0.0)
        self.refresh()

    def torna_indietro(self):
        self.pagina_precedente.show()
        self.close()

