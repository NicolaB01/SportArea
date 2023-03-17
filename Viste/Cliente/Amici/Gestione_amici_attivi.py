from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QMainWindow, QCheckBox, QWidget, QVBoxLayout

from Gestore.Gestore_amicizia import Gestore_amicizia
from Gestore.Gestore_cliente import Gestore_cliente
from Gestore.Gestore_viste import Gestore_viste
from Path.Path_viste import PATH_AMICI_ATTIVI


class Gestione_amici_attivi(QMainWindow):
    def __init__(self, pagina_precedente):
        super().__init__()
        uic.loadUi(PATH_AMICI_ATTIVI, self)
        self.pagina_precedente = pagina_precedente

        self.refresh()

        self.pushButton_rimuoviAmico.clicked.connect(self.rimuovi_amico)
        self.pushButton_back.clicked.connect(self.torna_indietro)

    def refresh(self):
        scroll_area_widget_contents = QWidget()
        vertical_layout = QVBoxLayout(scroll_area_widget_contents)

        vertical_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        for amico in Gestore_cliente.get_account_connesso().get_amici_attivi():
            vertical_layout.addWidget(self.crea_checkBox(amico))

        if len(scroll_area_widget_contents.findChildren(QCheckBox)) == 0:
            vertical_layout.addWidget(Gestore_viste.crea_label_comunicazione_cliente("La lista degli amici è vuota"))

        self.scrollArea_amici.setWidget(scroll_area_widget_contents)

    def crea_checkBox(self, amico_attivo):
        checkBox_richiesta = QCheckBox()

        checkBox_richiesta.setFont(QFont("Arial", 14, 50, False))
        checkBox_richiesta.setObjectName(amico_attivo.get_email())
        checkBox_richiesta.setStyleSheet("background-color:rgba(255, 255, 255, 0);\n"
                                         "padding:5px;\n"
                                         "border-radius:20px;\n"
                                         "border:2px solid rgb(136, 216, 208);\n"
                                         "color:rgb(22, 29, 111);")

        checkBox_richiesta.setText(f"Nome: {amico_attivo.get_nome()}\nCognome: {amico_attivo.get_cognome()}\nEmail: {amico_attivo.get_email()}")

        return checkBox_richiesta

    def rimuovi_amico(self):
        scroll_area_widget_contents = self.scrollArea_amici.findChild(QWidget)
        for widget in scroll_area_widget_contents.findChildren(QCheckBox):
            if widget.isChecked():
                Gestore_amicizia(widget.objectName()).rimuovi_amicizia()

        self.refresh()

    def torna_indietro(self):
        self.pagina_precedente.show()
        self.close()