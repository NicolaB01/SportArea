import random

from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QMessageBox

from Attività.Cliente import Cliente
from Gestore.Eccezioni import ExceptionPassword, ExceptionTentativi, ExceptionCodiceRecupero
from Path.Path_viste import PATH_CODICE_RECUPERO


class Codice_recupero(QMainWindow):
    def __init__(self, pagina_precedente, email):
        super().__init__()
        uic.loadUi(PATH_CODICE_RECUPERO, self)
        self.pagina_precedente = pagina_precedente
        self.email = email
        self.tenattivi = 3

        self.registrati.clicked.connect(self.controlla_codice)
        self.back.clicked.connect(self.torna_indietro)

    def controlla_codice(self):
        nuova_pwd = self.pwd.text()
        conferma_nuova_pwd = self.conferma_pwd.text()
        codice_da_verificare = self.codice_1.text()+self.codice_2.text()+self.codice_3.text()+ " " + self.codice_4.text()+self.codice_5.text()+self.codice_6.text()

        try:
            Cliente.check_pwd(nuova_pwd, conferma_nuova_pwd)
            self.check_tentativi()
            Cliente.verifica_codice_recupero_password(self.email, codice_da_verificare, nuova_pwd)

            self.torna_indietro()

        except ExceptionPassword as e:
            QMessageBox.warning(self, "Attenzione", e.__str__())

        except ExceptionTentativi as e:
            QMessageBox.warning(self, "Attenzione", e.__str__())
            Cliente.codice_di_verifica = " ".join([str(random.randint(0, 999)).zfill(3) for _ in range(2)])
            self.torna_indietro()

        except ExceptionCodiceRecupero as e:
            self.tenattivi -= 1
            QMessageBox.warning(self, "Attenzione!", f"{e.__str__()}, tentativi rimanenti {self.tenattivi}")

    def check_tentativi(self):
        if self.tenattivi == 0:
            raise ExceptionTentativi("Troppi tentativi, il codice di recupero è resettato")

    def torna_indietro(self):
        self.pagina_precedente.show()
        self.close()

    def keyPressEvent(self, event):
        if (event.key() == 16777220) or (event.key() == 43):
            self.controlla_codice()