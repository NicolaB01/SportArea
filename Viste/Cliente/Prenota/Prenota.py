import threading

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QWidget, QVBoxLayout, QCheckBox

from Attivita.Prenotazione import Prenotazione
from Gestore.Gestore_email import Gestore_email
from Utils.Eccezioni import ExceptionEmailSconosciuta, ExceptionSaldoInsufficente
from Gestore.Gestore_campo import Gestore_campo
from Gestore.Gestore_cliente import Gestore_cliente
from Gestore.Gestore_prenotazione import Gestore_prenotazione
from Gestore.Gestore_viste import Gestore_viste
from Path.Path_viste import PATH_CONFERMA_PRENOTAZIONE


class Prenota(QMainWindow):
    def __init__(self, pagina_precedente, home_cliente, nome_campo, data, aggiungi_partecipanti):
        super().__init__()
        uic.loadUi(PATH_CONFERMA_PRENOTAZIONE, self)
        self.pagina_precedente = pagina_precedente
        self.home_cliente = home_cliente
        self.campo = Gestore_campo.cerca_campo(nome_campo)
        self.data = data
        self.aggiungi_partecipanti = aggiungi_partecipanti
        self.partecipanti = Gestore_prenotazione.imposta_partecipanti(self.campo, self.data)

        self.refresh()

        self.logout_rimuovi.clicked.connect(self.rimuovi_partecipante)
        self.logout_aggiungi.clicked.connect(self.aggiungi_partecipante)
        self.logout_conferma.clicked.connect(self.conferma_prenotazione)
        self.back.clicked.connect(self.torna_indietro)

    def refresh(self):
        self.label_attivita.setText(f"Attività: {self.campo.get_attivita()}")
        self.label_campo.setText(f"Campo: {self.campo.get_nome_campo()}")
        self.label_ora.setText(f"Ora: {self.data.strftime('%H')}:00")
        self.label_data.setText(f"Data: {self.data.strftime('%x')}")
        self.label_Npartecipanti.setText(f"Numero partecipanti: {self.campo.get_numero_max_partecipanti()}")
        self.label_prezzo.setText(f"Prezzo: {self.campo.get_prezzo()}")

        self.aggiugni_amici_scrollArea()
        self.aggiungi_partecipanti_scrollArea()

    def aggiugni_amici_scrollArea(self):
        scroll_area_widget_contents = QWidget()
        vertical_layout = QVBoxLayout(scroll_area_widget_contents)
        vertical_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        for amico in Gestore_cliente.get_account_connesso().get_amici_attivi():
            vertical_layout.addWidget(self.crea_checkBox(amico.get_email(), amico.get_nome(), amico.get_cognome()))

        if len(scroll_area_widget_contents.findChildren(QCheckBox)) == 0:
            vertical_layout.addWidget(Gestore_viste.crea_label_comunicazione_cliente("Nesun amico trovato"))

        self.scrollArea_amici.setWidget(scroll_area_widget_contents)

    def aggiungi_partecipanti_scrollArea(self):
        scroll_area_widget_contents = QWidget()
        vertical_layout = QVBoxLayout(scroll_area_widget_contents)
        vertical_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        for email_partecipante in self.partecipanti:
            vertical_layout.addWidget(self.crea_checkBox(email_partecipante))

        if len(scroll_area_widget_contents.findChildren(QCheckBox)) == 0:
            vertical_layout.addWidget(Gestore_viste.crea_label_comunicazione_cliente("Non sono stati aggiunti dei partecipanti"))

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
        try:
            if self.lineEdit_email.text():
                account = Gestore_cliente.cerca_account(self.lineEdit_email.text())
                if account.get_email() not in self.partecipanti and not account.__eq__(Gestore_cliente.get_account_connesso()):
                    self.partecipanti.append(account.get_email)
        except ExceptionEmailSconosciuta as e:
            QMessageBox.warning(self, "Attenzione", e.__str__())

        self.refresh()

    #Quando il cliente conferma la prenotazione. Se il saldo è sufficente la prenotazione va a buon fine e il sistema
    #invia una email al cliente con il resoconto della prenotazione. Altrimenti viene visualizzata una finestra di errore.
    def conferma_prenotazione(self):
        if self.aggiungi_partecipanti:
            prenotazione = Gestore_prenotazione.cerca_prenotazione(self.campo, self.data)
            prenotazione.partecipanti = self.partecipanti
            prenotazione.salva_prenotazione()
            self.torna_indietro()
        else:
            try:
                Gestore_cliente.get_account_connesso().preleva(self.campo.get_prezzo())
                Prenotazione.crea_prenotazione(self.campo, self.data, self.partecipanti)
                threading.Thread(target=Gestore_email.invia_email_prenotazione, args=(Gestore_cliente.get_account_connesso(), Gestore_prenotazione.cerca_prenotazione(self.campo, self.data), self.campo.get_attivita())).start()
                self.home_cliente.show()
                self.close()
            except ExceptionSaldoInsufficente as e:
                QMessageBox.warning(self, "Attenzione", e.__str__())

    def torna_indietro(self):
        self.pagina_precedente.refresh()
        self.pagina_precedente.show()
        self.close()

