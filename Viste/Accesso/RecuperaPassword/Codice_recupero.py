from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QMessageBox

from Gestore.Gestore_cliente import Gestore_cliente
from Utils.Eccezioni import ExceptionPassword, ExceptionCodiceRecupero
from Path.Path_viste import PATH_CODICE_RECUPERO


class Codice_recupero(QMainWindow):
    def __init__(self, pagina_precedente, email):
        super().__init__()
        uic.loadUi(PATH_CODICE_RECUPERO, self)
        self.pagina_precedente = pagina_precedente
        self.email = email
        self.tenattivi = 3

        self.pushButton_verifica.clicked.connect(self.controlla_codice)
        self.pushButton_back.clicked.connect(self.torna_indietro)

    #Il cliente immette il codice di recupero e la nuova password con la sua conferma, se tutto è corretto la
    # password viene cambiata e si ritorna la login. Altrimenti se il codice è errato scalano i tentativi per poter
    # reimpostare la password(massimo 3 tentativi). Le password se non rispettano i requisiti non comportano la
    # diminuzione dei tentativi.
    def controlla_codice(self):
        nuova_pwd = self.pwd.text()
        conferma_nuova_pwd = self.conferma_pwd.text()
        codice_da_verificare = self.codice_1.text()+self.codice_2.text()+self.codice_3.text()+ " " + self.codice_4.text()+self.codice_5.text()+self.codice_6.text()

        try:
            Gestore_cliente.verifica_dati_recupero_password(self.get_email(), codice_da_verificare, nuova_pwd, conferma_nuova_pwd)
            self.torna_indietro()

        except ExceptionPassword as e:
            QMessageBox.warning(self, "Attenzione", e.__str__())
        except ExceptionCodiceRecupero:
            self.tenattivi -= 1
            self.check_tentativi()

    def check_tentativi(self):
        if self.tenattivi == 0:
            QMessageBox.warning(self, "Attenzione", "Troppi tentativi, il codice di recupero è resettato")
            self.torna_indietro()
        else:
            QMessageBox.warning(self, "Attenzione!", f"Tentativi rimanenti {self.tenattivi}")

    def torna_indietro(self):
        self.pagina_precedente.show()
        self.close()

    def keyPressEvent(self, event):
        if (event.key() == 16777220) or (event.key() == 43):
            self.controlla_codice()