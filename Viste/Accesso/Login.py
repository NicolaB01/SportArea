from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QMessageBox

from Utils.Eccezioni import ExceptionEmailSconosciuta, ExceptionPassword
from Gestore.Gestore_cliente import Gestore_cliente
from Path.Path_viste import PATH_LOGIN
from Viste.Amministratore.Amministratore import Amministratore
from Viste.Accesso.RecuperaPassword.Email_recupero import Email_recupero
from Viste.Cliente.Home_cliente import Home_cliente
from Viste.Accesso.Register import Register


class Login(QMainWindow):
    def __init__(self, pagina_precedente):
        super().__init__()
        uic.loadUi(PATH_LOGIN, self)
        self.pagina_precedente = pagina_precedente

        self.pushButton_accedi.clicked.connect(self.login)
        self.pushButton_registrati.clicked.connect(self.register)
        self.pushButton_recuperaPwd.clicked.connect(self.recupera_pwd)
        self.pushButton_back.clicked.connect(self.torna_indietro)

    # si verificano due casi:
    # se le credinziali inserite sono "admin" e "password", mostra il pannello di controllo amministratore
    # se le credenziali inserite sono di un utente qualsiasi:
    # controllo se esiste un cliente con tale credenziali, se esiste, mostro la homepage del cliente
    def login(self):
        email = self.email.text().strip()
        password = self.pwd.text()

        if not self.login_amministratore(email, password):
            self.login_cliente(email, password)

    def login_amministratore(self, email, password):
        if email == "admin" and password == "password":
            self.home_amministratore = Amministratore(self.pagina_precedente)
            self.home_amministratore.show()
            self.close()
            return True
        return False


    def login_cliente(self, email, password):
        try:
            Gestore_cliente.login_account(email, password)
            self.homepage = Home_cliente(self.pagina_precedente)
            self.homepage.show()
            self.close()
        except ExceptionEmailSconosciuta as e:
            QMessageBox.warning(self, "Attenzione!", e.__str__())
        except ExceptionPassword as e:
            QMessageBox.warning(self, "Attenzione!", e.__str__())

    def register(self):
        self.registati_menu = Register(self)
        self.registati_menu.show()
        self.close()

    def recupera_pwd(self):
        self.conferma_email_recupero = Email_recupero(self)
        self.conferma_email_recupero.show()
        self.close()

    def torna_indietro(self):
        self.pagina_precedente.show()
        self.close()

    def keyPressEvent(self, event):
        if (event.key() == 16777220) or (event.key() == 43):
            self.login()
