import multiprocessing

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel

from Gestore.Gestore_prenotazione import Gestore_prenotazione
from Gestore.Gestore_ricevuta import Gestore_ricevuta
from Gestore.Gestore_viste import Gestore_viste
from Path.Path_viste import PATH_VISUALIZZA_RICEVUTE


class Visualizza_ricevute(QMainWindow):
    def __init__(self, pagina_precedente):
        super().__init__()
        uic.loadUi(PATH_VISUALIZZA_RICEVUTE, self)
        self.pagina_precedente = pagina_precedente

        self.setUp()

        self.pushButton_back.clicked.connect(self.torna_indietro)

    def setUp(self):
        self.nuovo_processo = multiprocessing.Process(target=Gestore_prenotazione.controlla_scadenza_prenotazioni)
        self.nuovo_processo.start()

        scroll_area_widget_contents = QWidget()
        vertical_layout = QVBoxLayout(scroll_area_widget_contents)
        vertical_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        for ricevuta in Gestore_ricevuta.get_ricevute():
            vertical_layout.addWidget(self.crea_label_ricevuta(ricevuta))

        if len(scroll_area_widget_contents.findChildren(QLabel)) == 0:
            vertical_layout.addWidget(Gestore_viste.crea_label_comunicazione_admin("Al momento non ci sono ricevute nel database"))

        self.scrollArea_ricevute.setWidget(scroll_area_widget_contents)

    def crea_label_ricevuta(self, ricevuta):
        prenotazione_passata = QLabel()
        prenotazione_passata.setFont(QFont("Arial", 14, 50, False))
        prenotazione_passata.setStyleSheet("background-color:rgba(255, 255, 255, 0);\n"
                                           "padding:5px;\n"
                                           "border-radius:20px;\n"
                                           "border:2px solid rgb(52, 119, 134);\n"
                                           "color:rgb(44, 51, 51);")
        prenotazione_passata.setText(ricevuta.__str__())
        return prenotazione_passata

    def torna_indietro(self):
        self.pagina_precedente.show()
        self.close()

    def closeEvent(self, event):
        self.nuovo_processo.terminate()