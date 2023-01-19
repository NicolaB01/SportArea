from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel

from Attività.Campo import Campo
from Attività.Prenotazione import Prenotazione


class Prenotazioni_passate(QMainWindow):
    def __init__(self, pagina_precedente):
        super().__init__()
        uic.loadUi("/Users/nicola/PycharmProjects/ProgettoIDS/UI/SportArea-PrenotazioniPassate.ui", self)
        self.pagina_precedente = pagina_precedente

        self.setUp()

        self.back.clicked.connect(self.torna_indietro)

    def setUp(self):
        scroll_area_widget_contents = QWidget()
        vertical_layout = QVBoxLayout(scroll_area_widget_contents)
        vertical_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        for nome_campo, prenotazioni_effettuate in Prenotazione.get_prenotazioni_cliente_connesso().items():
            for prenotazione in prenotazioni_effettuate:
                if not prenotazione.attiva:
                    vertical_layout.addWidget(self.crea_label_prenotazione_passata(nome_campo, prenotazione.data_attività))

        self.scrollArea_prenotazioniPassate.setWidget(scroll_area_widget_contents)

    def crea_label_prenotazione_passata(self, nome_campo, data_attività):
        campo = Campo.cerca_campo(nome_campo)
        prenotazione_passata = QLabel()
        prenotazione_passata.setFont(QFont("Arial", 14, 50, False))
        prenotazione_passata.setStyleSheet("background-color:rgba(255, 255, 255, 0);\n"
                                   "padding:5px;\n"
                                   "border-radius:20px;\n"
                                   "border:2px solid rgb(152, 222, 217);\n"
                                   "color:rgb(22, 29, 111);")
        prenotazione_passata.setText(f"Attività: {campo.attività}\nCampo: {campo.nome}\nData: {data_attività.strftime('%x')}\nOra: {data_attività.strftime('%H')}:00\nPrezzo: {campo.prezzo}")
        return prenotazione_passata

    def torna_indietro(self):
        self.pagina_precedente.refresh()
        self.pagina_precedente.show()
        self.close()
