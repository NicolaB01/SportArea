from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow

from Path.Path_viste import PATH_HOME_CLIENTE
from Viste.Cliente.Account.Account import Account
from Viste.Cliente.Amici.Menu_amicizia import Menu_amicizia
from Viste.Cliente.Portafoglio.Portafoglio import Portafoglio
from Viste.Cliente.Prenota.Cerca_disponibilita import Cerca_disponibilita
from Viste.Cliente.Prenotazioni.Visualizza_prenotazioni import Visualizza_prenotazioni


class Home_cliente(QMainWindow):
    def __init__(self, pagina_precedente):
        super().__init__()
        uic.loadUi(PATH_HOME_CLIENTE, self)
        self.pagina_precedente = pagina_precedente

        self.pushButton_amici.clicked.connect(self.menu_amici)
        self.pushButton_prenota.clicked.connect(self.menu_disponibilita)
        self.pushButton_prenotazioni.clicked.connect(self.visualizza_prenotazioni)
        self.pushButton_portafoglio.clicked.connect(self.menu_portafoglio)
        self.pushButton_account.clicked.connect(self.mostra_account)
        self.pushButton_logout.clicked.connect(self.exit_account)

    def menu_amici(self):
        self.menu_amicizia = Menu_amicizia(self)
        self.menu_amicizia.show()
        self.close()

    def menu_disponibilita(self):
        self.menu_disponibilita = Cerca_disponibilita(self)
        self.menu_disponibilita.show()
        self.close()

    def visualizza_prenotazioni(self):
        self.visualizza_prenotazioni = Visualizza_prenotazioni(self)
        self.visualizza_prenotazioni.show()
        self.close()

    def menu_portafoglio(self):
        self.menu_portafoglio = Portafoglio(self)
        self.menu_portafoglio.show()
        self.close()

    def mostra_account(self):
        self.account = Account(self)
        self.account.show()
        self.close()

    def exit_account(self):
        self.pagina_precedente.show()
        self.close()

