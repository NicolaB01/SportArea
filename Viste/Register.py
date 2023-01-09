import re
from datetime import datetime

from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QMessageBox

from Attività.Cliente import Cliente


class Register(QMainWindow):
    def __init__(self, pagina_precedente):
        super().__init__()
        self.data_nascita = None
        uic.loadUi("/Users/nicola/PycharmProjects/ProgettoIDS/UI/SportArea-SignIn.ui", self)
        self.pagina_precedente = pagina_precedente

        self.pushButton_conferma.clicked.connect(self.registrati)
        self.back.clicked.connect(self.torna_indietro)

    def registrati(self):
        if self.check_campi():
            nome = self.lineEdit_nome.text().capitalize().strip()
            cognome = self.lineEdit_cognome.text().capitalize().strip()
            CF = self.lineEdit_CF.text().upper().strip()
            email = self.lineEdit_email.text().strip()
            data_nascita = self.lineEdit_data.text().strip()
            telefono = self.lineEdit_telefono.text().strip()
            password = self.lineEdit_pwd.text().strip()

            Cliente.registra_account(nome, cognome, CF, email, data_nascita, telefono, password)

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

        elif "@" not in self.lineEdit_email.text():
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
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
        pat = re.compile(reg)

        return re.search(pat, self.lineEdit_pwd.text())

    def torna_indietro(self):
        self.pagina_precedente.show()
        self.close()
