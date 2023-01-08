from PyQt5.QtWidgets import QMainWindow, QLineEdit, QPushButton, QMessageBox
from PyQt5 import uic

from Attività.Cliente import Cliente
from Viste.Account_home import Account_home


class Login(QMainWindow):
    def __init__(self):
        super(Login, self).__init__()
        uic.loadUi("C:\\Users\\Nicola\\PycharmProjects\\SportArea\\GUI\\SportArea_Login.ui", self)

        self.accedi = self.findChild(QPushButton, "accedi_btn")
        self.accedi.clicked.connect(self.funzione_accedi)

        self.registrati = self.findChild(QPushButton, "registrati_bnt")
        self.accedi.clicked.connect(self.funzione_registrati)

        self.email_line = self.findChild(QLineEdit, "email_lineedit")

        self.password_line = self.findChild(QLineEdit, "password_lineedit")




    def funzione_accedi(self):
        self.email = self.email_line.text()
        self.password = self.password_line.text()

        cliente = Cliente.cerca_account(self.email)
        print(cliente)
        if cliente is not None:
            if cliente.pwd == self.password:
                self.account_home = Account_home()
                self.account_home.show()
                self.close()
            else:
                QMessageBox.about(self, "Errore!", "Password errata")
        else:
            QMessageBox.about(self, "Errore!", "Account errato")

    def funzione_registrati(self):
        pass

    def torna_inidetro(self):
        pass

    def recupera_pwd(self):
        pass
