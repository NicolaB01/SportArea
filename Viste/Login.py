import pickle

from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QMessageBox

from Attività.Cliente import Cliente
from Viste.Amministratore import Amministratore
from Viste.Home_cliente import Home_cliente
from Viste.Register import Register


class Login(QMainWindow):
    def __init__(self, pagina_precedente):
        super().__init__()
        uic.loadUi("/Users/nicola/PycharmProjects/ProgettoIDS/UI/SportArea-LogIn.ui", self)
        self.pagina_precedente = pagina_precedente

        self.accedi.clicked.connect(self.menu_accedi)
        self.registrati.clicked.connect(self.menu_registrati)
        self.back.clicked.connect(self.torna_indietro)

    def menu_accedi(self):
        email = self.email.text().strip()
        password = self.pwd.text()

        if email == "admin" and password == "password":
            self.home_amministratore = Amministratore(self)
            self.home_amministratore.show()
            self.close()
        else:
            accaout_connesso = Cliente.cerca_account(email)
            if accaout_connesso is not None:
                if accaout_connesso.pwd == password:
                    with open(Cliente.PATH_ACCOUNT_CONNESSO, "wb") as f:
                        pickle.dump(accaout_connesso, f, pickle.HIGHEST_PROTOCOL)

                    self.homepage = Home_cliente(self)
                    self.homepage.show()
                    self.close()
                else:
                    QMessageBox.warning(self, "Attenzione!", "Password errata!")
            else:
                QMessageBox.warning(self, "Attenzione!", "Cliente non trovato con questa email")

    def menu_registrati(self):
        self.registati_menu = Register(self)
        self.registati_menu.show()
        self.close()

    def torna_indietro(self):
        self.pagina_precedente.show()
        self.close()

    def keyPressEvent(self, event):
        if (event.key() == 16777220) or (event.key() == 43):
            self.menu_accedi()