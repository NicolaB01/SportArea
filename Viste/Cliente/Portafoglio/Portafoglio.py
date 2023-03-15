import threading

from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow

from Gestore.Gestore_cliente import Gestore_cliente
from Gestore.Gestore_email import Gestore_email
from Path.Path_viste import PATH_PORTAFOGLIO


class Portafoglio(QMainWindow):
    def __init__(self, pagina_precedente):
        super().__init__()
        uic.loadUi(PATH_PORTAFOGLIO, self)
        self.pagina_precedente = pagina_precedente
        self.cliente = Gestore_cliente.get_account_connesso()

        self.refresh()

        self.pushButton_ricarica.clicked.connect(self.ricarica)
        self.pushButton_back.clicked.connect(self.torna_indietro)

    def refresh(self):
        self.label_saldo.setText(str(self.cliente.get_saldo()))

    #Quando un cliente ricarica il proprio account il sistema invia una email con l'importo versato.
    def ricarica(self):
        importo = self.doubleSpinBox_ricarica.value()
        self.cliente.deposito(importo)
        threading.Thread(target=Gestore_email.invia_email_ricarica_portafoglio, args=(self.cliente, importo)).start()
        self.doubleSpinBox_ricarica.setValue(0.0)
        self.refresh()

    def torna_indietro(self):
        self.pagina_precedente.show()
        self.close()

