from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow

from Gestore.Gestore_cliente import Gestore_cliente
from Path.Path_viste import PATH_ACCOUNT
from Viste.Cliente.Account.Modifica_account import Modifica_account


class Account(QMainWindow):
    def __init__(self, pagina_precedente):
        super().__init__()
        uic.loadUi(PATH_ACCOUNT, self)
        self.pagina_precedente = pagina_precedente

        self.refresh()

        self.pushButton_modifca.clicked.connect(self.menu_modifica_account)
        self.pushButton_back.clicked.connect(self.torna_indietro)

    def refresh(self):
        cliente = Gestore_cliente.get_account_connesso()

        self.label_nome.setText(cliente.get_nome())
        self.label_cognome.setText(cliente.get_cognome())
        self.label_email.setText(cliente.get_email())
        self.label_pwd.setText(cliente.get_pwd())
        self.label_CF.setText(cliente.get_CF())
        self.label_data.setText(cliente.get_data_nascita())
        self.label_telefono.setText(cliente.get_numero_telefono())

    def menu_modifica_account(self):
        self.menu_modifica_account = Modifica_account(self)
        self.menu_modifica_account.show()
        self.close()

    def torna_indietro(self):
        self.pagina_precedente.show()
        self.close()