from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow

from Viste.Login import Login
from Viste.Register import Register


class Home(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("/Users/nicola/PycharmProjects/ProgettoIDS/UI/SportArea-Home.ui", self)

        self.accedi.clicked.connect(self.menu_accedi)
        self.registrati.clicked.connect(self.menu_registrati)

    def menu_accedi(self):
        self.login = Login(self)
        self.login.show()
        self.close()

    def menu_registrati(self):
        self.registrati = Register(self)
        self.registrati.show()
        self.close()