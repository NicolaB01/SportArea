import threading

from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QMessageBox

from Gestore.Gestore_cliente import Gestore_cliente
from Gestore.Gestore_email import Gestore_email
from Utils.Eccezioni import ExceptionAmicizia, ExceptionEmailSconosciuta
from Gestore.Gestore_amicizia import Gestore_amicizia
from Path.Path_viste import PATH_MENU_AMICIZIA
from Viste.Cliente.Amici.Gestione_amici_attesa import Gestione_amici_attesa
from Viste.Cliente.Amici.Gestione_amici_attivi import Gestione_amici_attivi


class Menu_amicizia(QMainWindow):
    def __init__(self, pagina_precedente):
        super().__init__()
        uic.loadUi(PATH_MENU_AMICIZIA, self)
        self.pagina_precedente = pagina_precedente

        self.pushButton_listaAmici.clicked.connect(self.visualizza_lista_amici)
        self.pushButton_richieste.clicked.connect(self.visualizza_richieste_amicizia)
        self.pushButton_conferma.clicked.connect(self.manda_richiesta_amicizia)
        self.pushButton_back.clicked.connect(self.torna_indietro)

    def visualizza_lista_amici(self):
        self.lista_amici = Gestione_amici_attivi(self)
        self.lista_amici.show()
        self.close()

    def visualizza_richieste_amicizia(self):
        self.richieste_amicizia = Gestione_amici_attesa(self)
        self.richieste_amicizia.show()
        self.close()

    #Qaundo il cliente vuole mandare una richiesta di amicizia a un altro account. Il cliente inserisce la email
    #dell'account a cui vuole mandare l'amicizia(se è corretta o non è presente già nella sua lista degli amici) la
    #richiesta va a buon fine e il sistema manda una email al account che riceve la richiesta di amicizia.
    def manda_richiesta_amicizia(self):
        try:
            email = self.lineEdit_email.text()
            Gestore_amicizia(email).invia_richiesta_amicizia()
            threading.Thread(target=Gestore_email.invia_email_richiesta_amicizia, args=(Gestore_cliente.cerca_account(email), Gestore_cliente.get_account_connesso())).start()
        except ExceptionEmailSconosciuta as e:
            QMessageBox.warning(self, "Attenzione", e.__str__())
        except ExceptionAmicizia as e:
            QMessageBox.about(self, "Comunicazione", e.__str__())

    def torna_indietro(self):
        self.pagina_precedente.show()
        self.close()

