import threading

from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QMessageBox

from Utils.Eccezioni import ExceptionEmailSconosciuta
from Gestore.Gestore_cliente import Gestore_cliente
from Gestore.Gestore_email import Gestore_email
from Path.Path_viste import PATH_EMAIL_RECUPERO
from Viste.Accesso.RecuperaPassword.Codice_recupero import Codice_recupero


class Email_recupero(QMainWindow):
    def __init__(self, pagina_precedente):
        super().__init__()
        uic.loadUi(PATH_EMAIL_RECUPERO, self)
        self.pagina_precedente = pagina_precedente

        self.pushButton_invia.clicked.connect(self.controlla_email)
        self.pushButton_back.clicked.connect(self.torna_indietro)

    # Qunado un cliente vuole cambiare password attraverso la email. Il programma controlla che esista un account con tale
    # email, se esiste manda una mail con il codice di recupero della password. Fatto ciò apre una pagina per reimpostare la password.
    def controlla_email(self):
        email = self.email.text()

        try:
            Gestore_cliente.cerca_account(email)

            threading.Thread(target=Gestore_email.invia_email_recupero_pwd, args=(Gestore_cliente.cerca_account(email),)).start()
            self.conferma_codice_recupero = Codice_recupero(self.pagina_precedente, email)
            self.conferma_codice_recupero.show()
            self.close()
        except ExceptionEmailSconosciuta as e:
            QMessageBox.about(self, "Attenzione!", e.__str__())

    def torna_indietro(self):
        self.pagina_precedente.show()
        self.close()

    def keyPressEvent(self, event):
        if (event.key() == 16777220) or (event.key() == 43):
            self.controlla_email()