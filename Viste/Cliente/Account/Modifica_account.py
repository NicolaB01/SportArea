import time

from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QMessageBox

from Attività.Cliente import Cliente
from Gestore.Eccezioni import *
from Gestore.Gestore_clienti import Gestore_clienti
from Path.Path_viste import PATH_MODIFICA_ACCOUNT


class Modifica_account(QMainWindow):
    def __init__(self, pagina_precedente):
        super().__init__()
        uic.loadUi(PATH_MODIFICA_ACCOUNT, self)
        self.pagina_precedente = pagina_precedente

        self.setUp()

        self.pushButton_conferma.clicked.connect(self.modifica_account)
        self.back.clicked.connect(self.torna_indietro)

    def setUp(self):
        cliente = Cliente.get_account_connesso()

        self.lineEdit_nome.setText(cliente.nome)
        self.lineEdit_cognome.setText(cliente.cognome)
        self.lineEdit_pwd.setText(cliente.pwd)
        self.lineEdit_confermapwd.setText(cliente.pwd)
        self.lineEdit_CF.setText(cliente.codice_fiscale)
        self.lineEdit_data.setText(cliente.data_nascita)
        self.lineEdit_telefono.setText(cliente.numero_telefono)

    def modifica_account(self):
        nuovo_nome = self.lineEdit_nome.text().capitalize().strip()
        nuovo_cognome = self.lineEdit_cognome.text().capitalize().strip()
        nuovo_CF = self.lineEdit_CF.text().upper().strip()
        nuova_data_nascita = self.lineEdit_data.text().strip()
        nuovo_telefono = self.lineEdit_telefono.text().strip()
        nuova_password = self.lineEdit_pwd.text().strip()

        gestore = Gestore_clienti()
        try:
            gestore.check_nome(nuovo_nome)
            gestore.check_congome(nuovo_cognome)
            gestore.check_pwd(nuova_password)
            gestore.check_CF(nuovo_CF)
            gestore.check_data_nascita(nuova_data_nascita)
            gestore.check_teleono(nuovo_telefono)

            Cliente.get_account_connesso().modifica_account(nuovo_nome, nuovo_cognome, nuovo_CF, nuovo_telefono, nuova_password, nuova_data_nascita)
            time.sleep(0.15)
            self.pagina_precedente.refresh()
            self.torna_indietro()

        #TODO considera che basta una sola eccezione generale siccome passi l'errore come messaggio
        except ExceptionNomeFormat as e:
            QMessageBox.warning(self, "Attenzione", e.__str__())
        except ExceptionCognomeFormat as e:
            QMessageBox.warning(self, "Attenzione", e.__str__())
        except ExceptionPassword as e:
            QMessageBox.warning(self, "Attenzione", e.__str__())
        except ExceptionCFFormat as e:
            QMessageBox.warning(self, "Attenzione", e.__str__())
        except ExceptionDataNascitaFormat as e:
            QMessageBox.warning(self, "Attenzione", e.__str__())
        except ExceptionTelefonoFormat as e:
            QMessageBox.warning(self, "Attenzione", e.__str__())

    def torna_indietro(self):
        self.pagina_precedente.show()
        self.close()

    def keyPressEvent(self, event):
        if (event.key() == 16777220) or (event.key() == 43):
            self.modifica_account()
