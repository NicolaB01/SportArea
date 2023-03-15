import threading

from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QMessageBox

from Attivita.Cliente import Cliente
from Gestore.Gestore_email import Gestore_email
from Utils.Eccezioni import *
from Gestore.Gestore_cliente import Gestore_cliente
from Path.Path_viste import PATH_MODIFICA_ACCOUNT


class Modifica_account(QMainWindow):
    def __init__(self, pagina_precedente):
        super().__init__()
        uic.loadUi(PATH_MODIFICA_ACCOUNT, self)
        self.pagina_precedente = pagina_precedente

        self.setup()

        self.pushButton_conferma.clicked.connect(self.modifica_account)
        self.pushButton_back.clicked.connect(self.torna_indietro)

    def setup(self):
        cliente = Gestore_cliente.get_account_connesso()

        self.lineEdit_nome.setText(cliente.get_nome())
        self.lineEdit_cognome.setText(cliente.get_cognome())
        self.lineEdit_pwd.setText(cliente.get_pwd())
        self.lineEdit_confermapwd.setText(cliente.get_pwd())
        self.lineEdit_CF.setText(cliente.get_CF())
        self.lineEdit_data.setText(cliente.get_data_nascita())
        self.lineEdit_telefono.setText(cliente.get_numero_telefono())

    #Quando il cliente vuole modificare i dati del suo account. Inserisce i nuovi dati, che se corretti portano
    #alla effettiva modifica dell'account, altrimenti verrà mostrata una finestra dfi errore. Dopo la modifica si
    # ritorna alla finestra di visualizzazione dell'account.
    def modifica_account(self):
        nuovo_nome = self.lineEdit_nome.text().capitalize().strip()
        nuovo_cognome = self.lineEdit_cognome.text().capitalize().strip()
        nuovo_CF = self.lineEdit_CF.text().upper().strip()
        nuova_data_nascita = self.lineEdit_data.text().strip()
        nuovo_telefono = self.lineEdit_telefono.text().strip()
        nuova_password = self.lineEdit_pwd.text().strip()
        nuova_password_conferma = self.lineEdit_confermapwd.text().strip()

        try:
            Gestore_cliente.check_nome(nuovo_nome)
            Gestore_cliente.check_cognome(nuovo_cognome)
            Gestore_cliente.check_CF(nuovo_CF)
            Gestore_cliente.check_data_nascita(nuova_data_nascita)
            Gestore_cliente.check_teleono(nuovo_telefono)
            Gestore_cliente.check_pwd(nuova_password, nuova_password_conferma)

            Cliente.modifica_account(nuovo_nome, nuovo_cognome, nuovo_CF, nuovo_telefono, nuova_password, nuova_data_nascita)
            threading.Thread(target=Gestore_email.invia_email_modifica_account, args=(Gestore_cliente.get_account_connesso(),)).start()
            self.pagina_precedente.refresh()
            self.torna_indietro()

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
