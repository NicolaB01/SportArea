from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow

from Attività.Cliente import Cliente
from Viste.Account import Account
from Viste.Portafoglio import Portafoglio


class Home_cliente(QMainWindow):
    def __init__(self, pagina_precedente):
        super().__init__()
        uic.loadUi("/Users/nicola/PycharmProjects/ProgettoIDS/UI/SportArea-Cliente.ui", self)
        self.pagina_precedente = pagina_precedente

        self.portafoglio.clicked.connect(self.menu_portafoglio)
        self.account.clicked.connect(self.mostra_account)
        self.logout.clicked.connect(self.exit_account)

    def mostra_account(self):
        self.account = Account(self)
        self.account.show()
        self.close()

    def menu_portafoglio(self):
        self.menu_portafoglio = Portafoglio(self)
        self.menu_portafoglio.show()
        self.close()

    def exit_account(self):
        self.pagina_precedente.email.clear()
        self.pagina_precedente.pwd.clear()

        self.pagina_precedente.show()
        Cliente.get_account_connesso().exit_account()
        self.close()

    #TODO SE SI ESCE CON LA X SI FA IL LOG OUT
    def uscita_forzata(self, event):
        pass

