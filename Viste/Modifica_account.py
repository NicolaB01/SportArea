import re
import time
from datetime import datetime

from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QMessageBox

from Attività.Cliente import Cliente


class Modifica_account(QMainWindow):
    def __init__(self, pagina_precedente):
        super().__init__()
        uic.loadUi("/Users/nicola/PycharmProjects/ProgettoIDS/UI/SportArea-ModificaAccount.ui", self)
        self.pagina_precedente = pagina_precedente

        self.refresh()

        self.pushButton_conferma.clicked.connect(self.modifica_account)
        self.back.clicked.connect(self.torna_indietro)



    def modifica_account(self):
        if self.check_campi():
            nuovo_nome = self.lineEdit_nome.text().capitalize().strip()
            nuovo_cognome = self.lineEdit_cognome.text().capitalize().strip()
            nuovo_CF = self.lineEdit_CF.text().upper().strip()
            nuova_data_nascita = self.lineEdit_data.text().strip()
            nuovo_telefono = self.lineEdit_telefono.text().strip()
            nuova_password = self.lineEdit_pwd.text().strip()

            Cliente.get_account_connesso().modifica_account(nuovo_nome, nuovo_cognome, nuovo_CF, nuovo_telefono, nuova_password, nuova_data_nascita)

            time.sleep(0.15)
            self.pagina_precedente.refresh()
            self.pagina_precedente.show()
            self.close()

        else:
            QMessageBox.warning(self, "Attenzione!", "campi non corretti!")

    def check_campi(self):
        # il nome deve avere minimo 3 caratteri
        if len(self.lineEdit_nome.text()) < 3:
            return False

        # il cognome deve avere minimo 3 caratteri
        elif len(self.lineEdit_cognome.text()) < 3:
            return False

        # il id_cliente fiscale deve essere esattamente di 16 caratteri
        elif len(self.lineEdit_CF.text()) != 16 or not self.lineEdit_CF.text().isalnum():
            return False

        elif len(self.lineEdit_data.text()) != 0:
            try:
                if self.lineEdit_data.text().count("/") == 2:
                    day, month, year = self.lineEdit_data.text().split('/')

                    if datetime.now().year > int(year) > 1905:
                        datetime(int(year), int(month), int(day))
                        return True

                raise ValueError
            except ValueError:
                return False

        elif not self.check_pwd():
            return False

        # il numero di telefono puo avere solo 10 cifre
        elif len(self.lineEdit_telefono.text()) != 10 or not str(self.lineEdit_telefono.text()).isnumeric():
            return False

        else:
            return True

    def check_pwd(self):
        if self.lineEdit_pwd == self.lineEdit_confermapwd:
            reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
            pat = re.compile(reg)

            return re.search(pat, self.lineEdit_pwd.text())
        else:
            return False

    def refresh(self):
        cliente = Cliente.get_account_connesso()

        self.lineEdit_nome.setText(cliente.nome)
        self.lineEdit_cognome.setText(cliente.cognome)
        self.lineEdit_pwd.setText(cliente.pwd)
        self.lineEdit_confermapwd.setText(cliente.pwd)
        self.lineEdit_CF.setText(cliente.codice_fiscale)
        self.lineEdit_data.setText(cliente.data_nascita)
        self.lineEdit_telefono.setText(cliente.numero_telefono)

    def torna_indietro(self):
        self.pagina_precedente.show()
        self.close()

    def keyPressEvent(self, event):
        if (event.key() == 16777220) or (event.key() == 43):
            self.modifica_account()