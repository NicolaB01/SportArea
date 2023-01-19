import datetime
import multiprocessing

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QRadioButton, QMessageBox

from Attività.Campo import Campo
from Attività.Cliente import Cliente
from Attività.Prenotazione import Prenotazione
from Viste.Cliente.Prenota.Prenota import Prenota


class Prenotazioni_attive(QMainWindow):
    def __init__(self, pagina_precedente):
        super().__init__()
        uic.loadUi("/Users/nicola/PycharmProjects/ProgettoIDS/UI/SportArea-PrenotazioniAttive.ui", self)
        self.pagina_precedente = pagina_precedente
        self.nuovo_processo = multiprocessing.Process(target=Prenotazione.controlla_scadenza_prenotazioni)
        self.nuovo_processo.start()

        self.refresh()

        self.pushButton_aggiungiPartecipante.clicked.connect(self.aggiungi_partecipanti)
        self.pushButton_elimina.clicked.connect(self.elimina_prenotazione)
        self.back.clicked.connect(self.torna_indietro)

    #TODO fare in modo che il controllo delle prenotazioni refreshi anche la pagina(ora funziona ma è più bello)
    def refresh(self):
        scroll_area_widget_contents = QWidget()
        vertical_layout = QVBoxLayout(scroll_area_widget_contents)
        vertical_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        for nome_campo, prenotazioni_effettuate in Prenotazione.get_prenotazioni_cliente_connesso().items():
            for prenotazione in prenotazioni_effettuate:
                if prenotazione.attiva:
                    vertical_layout.addWidget(self.crea_radioButton(nome_campo, prenotazione.data_attività))

        self.scrollArea_ListaPrenotazioni.setWidget(scroll_area_widget_contents)

    def crea_radioButton(self, nome_campo, data_attività):
        campo = Campo.cerca_campo(nome_campo)
        radio_button = QRadioButton()
        radio_button.setFont(QFont("Arial", 14, 50, False))
        radio_button.setObjectName(f"{data_attività.day}/{data_attività.month}/{data_attività.year}/{data_attività.hour}/{nome_campo}")
        radio_button.setStyleSheet("background-color:rgba(255, 255, 255, 0);\n"
                                   "padding:5px;\n"
                                   "border-radius:20px;\n"
                                   "border:2px solid rgb(152, 222, 217);\n"
                                   "color:rgb(22, 29, 111);")
        radio_button.setText(f"Attività: {campo.attività}\nCampo: {campo.nome}\nData: {data_attività.strftime('%x')}\nOra: {data_attività.strftime('%H')}:00")
        # TODO aggiungere il testo della radio button
        return radio_button

    def aggiungi_partecipanti(self):
        scroll_area_widget_contents = self.scrollArea_ListaPrenotazioni.findChild(QWidget)
        for widget in scroll_area_widget_contents.findChildren(QRadioButton):
            if widget.isChecked():
                giorno, mese, anno, ora, nome_campo = widget.objectName().split("/")
                data_prenotazione = datetime.datetime(int(anno), int(mese), int(giorno), int(ora))
                if self.is_modificabile(data_prenotazione):
                    self.aggiungi_partecipanti = Prenota(self, self, nome_campo, data_prenotazione, True)
                    self.aggiungi_partecipanti.show()
                    self.close()
                else:
                    QMessageBox.warning(self, "Attenizione", "Mancano meno di 5 ore alla prenotazione, non è più modificabile")

        self.refresh()

    def elimina_prenotazione(self):
        scroll_area_widget_contents = self.scrollArea_ListaPrenotazioni.findChild(QWidget)
        for widget in scroll_area_widget_contents.findChildren(QRadioButton):
            if widget.isChecked():
                giorno, mese, anno, ora, nome_campo = widget.objectName().split("/")
                data_prenotazione = datetime.datetime(int(anno), int(mese), int(giorno), int(ora))
                if self.is_modificabile(data_prenotazione):
                    prenotazione = Prenotazione.get_prenotazione_data(Campo.cerca_campo(nome_campo), data_prenotazione)
                    Cliente.get_account_connesso().deposito(Campo.cerca_campo(prenotazione.nome_campo).prezzo)
                    prenotazione.elimina_prenotazione()
                else:
                    QMessageBox.warning(self, "Attenizione", "Mancano meno di 5 ore alla prenotazione, non è più modificabile")


        self.refresh()

    def is_modificabile(self, data_evento):
        if data_evento.strftime("%x") == datetime.datetime.now().strftime("%x"):
            if int(data_evento.strftime("%H")) - int(datetime.datetime.now().strftime("%H")) <= 5:
                return False

        return True

    def torna_indietro(self):
        self.pagina_precedente.refresh()
        self.pagina_precedente.show()
        self.close()

    def closeEvent(self, event):
        self.nuovo_processo.terminate()





