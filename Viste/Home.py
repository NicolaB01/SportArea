from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
from Viste.Login import Login


class Home(QMainWindow):
    def __init__(self):
        super(Home, self).__init__()
        uic.loadUi("C:\\Users\\Nicola\\PycharmProjects\\SportArea\\GUI\\SportArea_Home.ui", self)
        self.accedi.clicked.connect(self.menu_accedi)
        self.registrati.clicked.connect(self.menu_registrati)



    def menu_accedi(self):
        self.login = Login()
        self.close()
        self.login.show()

    def menu_registrati(self):
        pass



