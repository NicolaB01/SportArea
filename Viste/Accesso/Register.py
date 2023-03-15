import threading

from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QMessageBox

from Attivita.Cliente import Cliente
from Gestore.Gestore_email import Gestore_email
from Utils.Eccezioni import *
from Gestore.Gestore_cliente import Gestore_cliente
from Path.Path_viste import PATH_REGISTER


class Register(QMainWindow):
    def __init__(self, pagina_precedente):
        super().__init__()
        uic.loadUi(PATH_REGISTER, self)
        self.pagina_precedente = pagina_precedente

        self.pushButton_conferma.clicked.connect(self.registrati)
        self.pushButton_back.clicked.connect(self.torna_indietro)

    # Un cliente vuole creare un nuovo account e passa i nuovi dati, se giusti, l'account viene creato correttamente e si ritorna alla pagina di login
    def registrati(self):
        nome = self.lineEdit_nome.text().capitalize().strip()
        cognome = self.lineEdit_cognome.text().capitalize().strip()
        CF = self.lineEdit_CF.text().upper().strip()
        email = self.lineEdit_email.text().strip()
        data_nascita = self.lineEdit_data.text().strip()
        telefono = self.lineEdit_telefono.text().strip()
        password = self.lineEdit_pwd.text().strip()

        try:
            Gestore_cliente.check_nome(nome)
            Gestore_cliente.check_cognome(cognome)
            Gestore_cliente.check_CF(CF)
            Gestore_cliente.check_email(email)
            Gestore_cliente.check_data_nascita(data_nascita)
            Gestore_cliente.check_teleono(telefono)
            Gestore_cliente.check_pwd(password)

            Cliente.crea_cliente(nome, cognome, CF, email, data_nascita, telefono, password)
            threading.Thread(target=Gestore_email.invia_email_crea_account, args=(Gestore_cliente.cerca_account(email),)).start()
            self.torna_indietro()

        except ExceptionNomeFormat as e:
            QMessageBox.warning(self, "Attenzione", e.__str__())
        except ExceptionCognomeFormat as e:
            QMessageBox.warning(self, "Attenzione", e.__str__())
        except ExceptionEmailFormat as e:
            QMessageBox.warning(self, "Attenzione", e.__str__())
        except ExceptionPassword as e:
            QMessageBox.warning(self, "Attenzione", e.__str__())
        except ExceptionCFFormat as e:
            QMessageBox.warning(self, "Attenzione", e.__str__())
        except ExceptionDataNascitaFormat as e:
            QMessageBox.warning(self, "Attenzione", e.__str__())
        except ExceptionTelefonoFormat as e:
            QMessageBox.warning(self, "Attenzione", e.__str__())
        except ExceptionEmailUtilizzata as e:
            QMessageBox.warning(self, "Attenzione", e.__str__())


    def torna_indietro(self):
        self.pagina_precedente.show()
        self.close()
