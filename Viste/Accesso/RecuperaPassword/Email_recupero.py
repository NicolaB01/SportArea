import threading

from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QMessageBox

from Attività.Cliente import Cliente
from Gestore.Eccezioni import ExceptionEmailSconosciuta
from Path.Path_viste import PATH_EMAIL_RECUPERO
from Viste.Accesso.RecuperaPassword.Codice_recupero import Codice_recupero


class Email_recupero(QMainWindow):
    def __init__(self, pagina_precedente):
        super().__init__()
        uic.loadUi(PATH_EMAIL_RECUPERO, self)
        self.pagina_precedente = pagina_precedente

        self.registrati.clicked.connect(self.controlla_email)
        self.back.clicked.connect(self.torna_indietro)

    def controlla_email(self):
        email = self.email.text()

        try:
            Cliente.cerca_account(email)

            self.conferma_codice_recupero = Codice_recupero(self.pagina_precedente, email)
            self.conferma_codice_recupero.show()
            threading.Thread(target=Cliente.invia_email_recupero_pwd, args=(email,)).start()
            self.close()
        except ExceptionEmailSconosciuta as e:
            QMessageBox.about(self, "Attenzione!", e.__str__())

    def torna_indietro(self):
        self.pagina_precedente.show()
        self.close()

    def keyPressEvent(self, event):
        if (event.key() == 16777220) or (event.key() == 43):
            self.controlla_email()