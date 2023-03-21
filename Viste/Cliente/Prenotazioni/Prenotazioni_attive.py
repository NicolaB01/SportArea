import datetime

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QRadioButton, QMessageBox

from Utils.Eccezioni import ExceptionPreotazioneNonModificabile
from Gestore.Gestore_campo import Gestore_campo
from Gestore.Gestore_cliente import Gestore_cliente
from Gestore.Gestore_prenotazione import Gestore_prenotazione
from Gestore.Gestore_viste import Gestore_viste
from Path.Path_viste import PATH_PRENOTAZIONI_ATTIVE
from Viste.Cliente.Prenota.Prenota import Prenota


class Prenotazioni_attive(QMainWindow):
    def __init__(self, pagina_precedente):
        super().__init__()
        uic.loadUi(PATH_PRENOTAZIONI_ATTIVE, self)
        self.pagina_precedente = pagina_precedente

        self.refresh()

        self.pushButton_aggiungiPartecipante.clicked.connect(self.aggiungi_partecipanti)
        self.pushButton_elimina.clicked.connect(self.elimina_prenotazione)
        self.back.clicked.connect(self.torna_indietro)

    def refresh(self):
        scroll_area_widget_contents = QWidget()
        vertical_layout = QVBoxLayout(scroll_area_widget_contents)
        vertical_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        for nome_campo, prenotazioni_effettuate in Gestore_prenotazione.get_prenotazioni_cliente_connesso().items():
            for prenotazione in prenotazioni_effettuate:
                if prenotazione.attiva:
                    vertical_layout.addWidget(self.crea_radioButton(nome_campo, prenotazione.get_data_attivita()))

        if len(scroll_area_widget_contents.findChildren(QRadioButton)) == 0:
            vertical_layout.addWidget(Gestore_viste.crea_label_comunicazione_cliente("Non ci sono prenotazioni attive"))

        self.scrollArea_ListaPrenotazioni.setWidget(scroll_area_widget_contents)

    def crea_radioButton(self, nome_campo, data_attivita):
        campo = Gestore_campo.cerca_campo(nome_campo)
        radio_button = QRadioButton()
        radio_button.setFont(QFont("Arial", 14, 50, False))
        radio_button.setObjectName(f"{data_attivita.day}/{data_attivita.month}/{data_attivita.year}/{data_attivita.hour}/{nome_campo}")
        radio_button.setStyleSheet("background-color:rgba(255, 255, 255, 0);\n"
                                   "padding:5px;\n"
                                   "border-radius:20px;\n"
                                   "border:2px solid rgb(152, 222, 217);\n"
                                   "color:rgb(22, 29, 111);")
        radio_button.setText(f"Attività: {campo.get_attivita()}\nCampo: {campo.get_nome_campo()}\nData: {data_attivita.strftime('%d/%m/%Y')}\nOra: {data_attivita.strftime('%H:00')}")
        return radio_button

    #Quando il cliente vuole aggiungere un partecipante a una prenotazione attiva. Il sistema controlla che la
    #prenotazione sia ancora modificabile, se è così apre un altra pagina per poter modificare i
    #partecipanti alla prenotazione
    def aggiungi_partecipanti(self):
        scroll_area_widget_contents = self.scrollArea_ListaPrenotazioni.findChild(QWidget)
        for widget in scroll_area_widget_contents.findChildren(QRadioButton):
            if widget.isChecked():
                giorno, mese, anno, ora, nome_campo = widget.objectName().split("/")
                data_prenotazione = datetime.datetime(int(anno), int(mese), int(giorno), int(ora))
                try:
                    Gestore_prenotazione.is_modificabile(data_prenotazione)
                    self.aggiungi_partecipanti = Prenota(self, self, nome_campo, data_prenotazione, True)
                    self.aggiungi_partecipanti.show()
                    self.close()
                except ExceptionPreotazioneNonModificabile as e:
                    QMessageBox.warning(self, "Attenizione", e.__str__())

        self.refresh()

    #Quando il cliente vuole eliinare una prenotazione attiva il sistema verifica che quest'ultima si ancora
    #modificabile, se così è allora la prenotazioen viene rimossa con successo altrimenti comparirà a
    # schermo una finestra di errore.
    def elimina_prenotazione(self):
        scroll_area_widget_contents = self.scrollArea_ListaPrenotazioni.findChild(QWidget)
        for widget in scroll_area_widget_contents.findChildren(QRadioButton):
            if widget.isChecked():
                giorno, mese, anno, ora, nome_campo = widget.objectName().split("/")
                data_prenotazione = datetime.datetime(int(anno), int(mese), int(giorno), int(ora))
                try:
                    Gestore_prenotazione.is_modificabile(data_prenotazione)
                    prenotazione = Gestore_prenotazione.cerca_prenotazione(Gestore_campo.cerca_campo(nome_campo), data_prenotazione)
                    prezzo = Gestore_campo.cerca_campo(prenotazione.nome_campo).prezzo
                    Gestore_cliente.get_account_connesso().deposito(prezzo)
                    prenotazione.elimina_prenotazione()
                    QMessageBox.about(self, "Comunicazione", f"La prenotazione è stata rimossa con successo, ti sono stati riaccreditati: {prezzo}€")
                except ExceptionPreotazioneNonModificabile as e:
                    QMessageBox.warning(self, "Attenizione", e.__str__())

        self.refresh()

    def torna_indietro(self):
        self.pagina_precedente.show()
        self.close()

