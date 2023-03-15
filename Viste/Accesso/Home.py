from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow

from Path.Path_viste import PATH_HOME
from Viste.Accesso.Login import Login
from Viste.Accesso.Register import Register


class Home(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(PATH_HOME, self)

        self.pushButton_accedi.clicked.connect(self.menu_accesso)
        self.pushButton_registrati.clicked.connect(self.menu_registrazione)

    def menu_accesso(self):
        self.login = Login(self)
        self.login.show()
        self.close()

    def menu_registrazione(self):
        self.registrati = Register(self)
        self.registrati.show()
        self.close()
