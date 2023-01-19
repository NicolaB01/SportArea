from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QMessageBox

from Attività.Cliente import Cliente
from Gestore.Eccezioni import *
from Gestore.Gestore_clienti import Gestore_clienti
from Path.Path_viste import PATH_REGISTER


class Register(QMainWindow):
    def __init__(self, pagina_precedente):
        super().__init__()
        uic.loadUi(PATH_REGISTER, self)
        self.pagina_precedente = pagina_precedente

        self.pushButton_conferma.clicked.connect(self.registrati)
        self.back.clicked.connect(self.torna_indietro)

    def registrati(self):
        nome = self.lineEdit_nome.text().capitalize().strip()
        cognome = self.lineEdit_cognome.text().capitalize().strip()
        CF = self.lineEdit_CF.text().upper().strip()
        email = self.lineEdit_email.text().strip()
        data_nascita = self.lineEdit_data.text().strip()
        telefono = self.lineEdit_telefono.text().strip()
        password = self.lineEdit_pwd.text().strip()

        gestore = Gestore_clienti()
        try:
            gestore.check_nome(nome)
            gestore.check_congome(cognome)
            gestore.check_email(email)
            gestore.check_pwd(password)
            gestore.check_CF(CF)
            gestore.check_data_nascita(data_nascita)
            gestore.check_teleono(telefono)

            Cliente.registra_account(nome, cognome, CF, email, data_nascita, telefono, password)

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


    def torna_indietro(self):
        self.pagina_precedente.show()
        self.close()
