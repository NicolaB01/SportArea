from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QMessageBox

from Attività.Cliente import Cliente
from Gestore.Eccezioni import ExceptionEmailFormat, ExceptionAmicizia, ExceptionEmailSconosciuta
from Path.Path_viste import PATH_MENU_AMICIZIA
from Viste.Cliente.Amici.Amici_attivi import Amici_attivi
from Viste.Cliente.Amici.Richieste_amicizia import Richieste_amicizia


class Menu_amicizia(QMainWindow):
    def __init__(self, pagina_precedente):
        super().__init__()
        uic.loadUi(PATH_MENU_AMICIZIA, self)
        self.pagina_precedente = pagina_precedente

        self.pushButton_listaAmici.clicked.connect(self.lista_amici)
        self.pushButton_richieste.clicked.connect(self.richieste_amicizia)
        self.pushButton_conferma.clicked.connect(self.manda_amicizia)
        self.pushButton_back.clicked.connect(self.torna_indietro)

    def lista_amici(self):
        self.lista_amici = Amici_attivi(self)
        self.lista_amici.show()
        self.close()

    def richieste_amicizia(self):
        self.richieste_amicizia = Richieste_amicizia(self)
        self.richieste_amicizia.show()
        self.close()

    def manda_amicizia(self):
        try:
            email = self.lineEdit_email.text()
            Cliente.get_account_connesso().richiesta_amicizia(email)
        except ExceptionEmailSconosciuta as e:
            QMessageBox.warning(self, "Attenzione", e.__str__())
        except ExceptionEmailFormat as e:
            QMessageBox.warning(self, "Attenzione", e.__str__())
        except ExceptionAmicizia as e:
            QMessageBox.about(self, "Comunicazione", e.__str__())

    def torna_indietro(self):
        self.pagina_precedente.show()
        self.close()

