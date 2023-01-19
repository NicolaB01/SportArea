from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QWidget, QVBoxLayout, QCheckBox

from Attività.Campo import Campo
from Attività.Cliente import Cliente
from Attività.Prenotazione import Prenotazione


class Prenota(QMainWindow):
    def __init__(self, pagina_precedente, home_cliente, nome_campo, data, aggiungi_partecipanti):
        super().__init__()
        uic.loadUi("/Users/nicola/PycharmProjects/ProgettoIDS/UI/SportArea-ConfermaPrenotazione.ui", self)
        self.pagina_precedente = pagina_precedente
        self.home_cliente = home_cliente
        self.campo = Campo.cerca_campo(nome_campo)
        self.data = data
        self.aggiungi_partecipanti = aggiungi_partecipanti
        prenotazione = Prenotazione.get_prenotazione_data(self.campo, self.data)
        if prenotazione is not None:
            self.partecipanti = prenotazione.partecipanti
        else:
            self.partecipanti = []

        self.refresh()

        self.logout_rimuovi_partecipante.clicked.connect(self.rimuovi_partecipante)
        self.logout_aggiungi.clicked.connect(self.aggiungi_partecipante)
        self.logout_conferma.clicked.connect(self.conferma_prenotazione)
        self.back.clicked.connect(self.torna_indietro)

    def refresh(self):
        self.label_attivita.setText(f"Attività: {self.campo.attività}")
        self.label_campo.setText(f"Campo: {self.campo.nome}")
        self.label_ora.setText(f"Ora: {self.data.strftime('%H')}:00")
        self.label_data.setText(f"Data: {self.data.strftime('%x')}")
        self.label_Npartecipanti.setText(f"Numero partecipanti: {self.campo.numero_max_partecipanti}")
        self.label_prezzo.setText(f"Prezzo: {self.campo.prezzo}")

        scroll_area_widget_contents = QWidget()
        vertical_layout = QVBoxLayout(scroll_area_widget_contents)

        vertical_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        for amico in Cliente.get_account_connesso().amici_attivi:
            nome = amico.nome
            cognome = amico.cognome
            email = amico.email
            vertical_layout.addWidget(self.crea_checkBox(email, nome, cognome))

        self.scrollArea_amici.setWidget(scroll_area_widget_contents)

        scroll_area_widget_contents = QWidget()
        vertical_layout = QVBoxLayout(scroll_area_widget_contents)

        for email_partecipante in self.partecipanti:
            vertical_layout.addWidget(self.crea_checkBox(email_partecipante))

        self.scrollArea_partecipanti.setWidget(scroll_area_widget_contents)

    def crea_checkBox(self, email, nome = None, cognome = None):
        checkBox_richiesta = QCheckBox()

        checkBox_richiesta.setFont(QFont("Arial", 14, 50, False))

        checkBox_richiesta.setObjectName(email)
        checkBox_richiesta.setStyleSheet("background-color:rgba(255, 255, 255, 0);\n"
                                         "padding:5px;\n"
                                         "border-radius:20px;\n"
                                         "border:2px solid rgb(136, 216, 208);\n"
                                         "color:rgb(22, 29, 111);")

        if nome is None and cognome is None:
            testo = f"Email: {email}"
        else:
            testo = f"Nome: {nome}\nCognome: {cognome}\nEmail: {email}"

        checkBox_richiesta.setText(testo)

        return checkBox_richiesta

    def rimuovi_partecipante(self):
        scroll_area_widget_contents = self.scrollArea_partecipanti.findChild(QWidget)
        for widget in scroll_area_widget_contents.findChildren(QCheckBox):
            if widget.isChecked():
                self.partecipanti.remove(widget.objectName())

        self.refresh()

    def aggiungi_partecipante(self):
        scroll_area_widget_contents = self.scrollArea_amici.findChild(QWidget)
        for widget in scroll_area_widget_contents.findChildren(QCheckBox):
            if widget.isChecked():
                if widget.objectName() not in self.partecipanti:
                    self.partecipanti.append(widget.objectName())

        if len(self.lineEdit_email.text()) != 0:
            account = Cliente.cerca_account(self.lineEdit_email.text())
            if account is not None and account.email not in self.partecipanti and account.email != Cliente.get_account_connesso().email:
                self.partecipanti.append(account.email)
            else:
                QMessageBox.warning(self, "Attenzione", "Email errata")

        self.refresh()

    def conferma_prenotazione(self):
        if self.aggiungi_partecipanti:
            prenotazione = Prenotazione.get_prenotazione_data(self.campo, self.data)
            prenotazione.partecipanti = self.partecipanti
            prenotazione.salva_prenotazione()
            self.pagina_precedente.show()
            self.close()
        else:
            if Cliente.get_account_connesso().preleva(self.campo.prezzo):
                Prenotazione.prenota_campo(self.campo, self.data, self.partecipanti)
                self.home_cliente.show()
                self.close()
            else:
                QMessageBox.warning(self, "Attenzione", "Il credito è insufficente per effettuare la prenotazione")

    def torna_indietro(self):
        self.pagina_precedente.refresh()
        self.pagina_precedente.show()
        self.close()

