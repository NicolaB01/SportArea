from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel

from Gestore.Gestore_campo import Gestore_campo
from Gestore.Gestore_prenotazione import Gestore_prenotazione
from Gestore.Gestore_viste import Gestore_viste
from Path.Path_viste import PATH_PRENOTAZIONI_PASSATE


class Prenotazioni_passate(QMainWindow):
    def __init__(self, pagina_precedente):
        super().__init__()
        uic.loadUi(PATH_PRENOTAZIONI_PASSATE, self)
        self.pagina_precedente = pagina_precedente

        self.setup()

        self.back.clicked.connect(self.torna_indietro)

    def setup(self):
        scroll_area_widget_contents = QWidget()
        vertical_layout = QVBoxLayout(scroll_area_widget_contents)
        vertical_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        for nome_campo, prenotazioni_effettuate in Gestore_prenotazione.get_prenotazioni_cliente_connesso().items():
            for prenotazione in prenotazioni_effettuate:
                if not prenotazione.attiva:
                    vertical_layout.addWidget(self.crea_label_prenotazione_passata(nome_campo,
                                                                                   prenotazione.get_data_attivita()))

        if len(scroll_area_widget_contents.findChildren(QLabel)) == 0:
            vertical_layout.addWidget(Gestore_viste.crea_label_comunicazione_cliente("Non ci sono prenotazioni Passate"))

        self.scrollArea_prenotazioniPassate.setWidget(scroll_area_widget_contents)

    def crea_label_prenotazione_passata(self, nome_campo, data_attivita):
        campo = Gestore_campo.cerca_campo(nome_campo)
        prenotazione_passata = QLabel()
        prenotazione_passata.setFont(QFont("Arial", 14, 50, False))
        prenotazione_passata.setStyleSheet("background-color:rgba(255, 255, 255, 0);\n"
                                   "padding:5px;\n"
                                   "border-radius:20px;\n"
                                   "border:2px solid rgb(152, 222, 217);\n"
                                   "color:rgb(22, 29, 111);")
        prenotazione_passata.setText(f"Attività: {campo.get_attivita()}\nCampo: {campo.get_nome_campo()}\nData: {data_attivita.strftime('%x')}\nOra: {data_attivita.strftime('%H')}:00\nPrezzo: {campo.get_prezzo()}")
        return prenotazione_passata

    def torna_indietro(self):
        self.pagina_precedente.show()
        self.close()