from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QMainWindow, QCheckBox, QWidget, QVBoxLayout

from Gestore.Gestore_amicizia import Gestore_amicizia
from Gestore.Gestore_cliente import Gestore_cliente
from Gestore.Gestore_viste import Gestore_viste
from Path.Path_viste import PATH_AMICI_ATTESA


class Gestione_amici_attesa(QMainWindow):
    def __init__(self, pagina_precedente):
        super().__init__()
        uic.loadUi(PATH_AMICI_ATTESA, self)
        self.pagina_precedente = pagina_precedente

        self.refresh()

        self.pushButton_rifiuta.clicked.connect(self.rifiuta_richiesta)
        self.pushButton_accetta.clicked.connect(self.accetta_richiesta)
        self.pushButton_back.clicked.connect(self.torna_indietro)

    def refresh(self):
        scroll_area_widget_contents = QWidget()
        vertical_layout = QVBoxLayout(scroll_area_widget_contents)
        vertical_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        for amico_attesa in Gestore_cliente.get_account_connesso().get_amici_attesa():
            vertical_layout.addWidget(self.crea_checkBox(amico_attesa))

        if len(scroll_area_widget_contents.findChildren(QCheckBox)) == 0:
            vertical_layout.addWidget(Gestore_viste.crea_label_comunicazione_cliente("Non ci sono richieste di amicizia in attesa"))

        self.scrollArea_richieste.setWidget(scroll_area_widget_contents)

    def crea_checkBox(self, amico_attesa):
        checkBox_richiesta = QCheckBox()

        checkBox_richiesta.setFont(QFont("Arial", 14, 50, False))
        checkBox_richiesta.setObjectName(amico_attesa.get_email())
        checkBox_richiesta.setStyleSheet("background-color:rgba(255, 255, 255, 0);\n"
                                         "padding:5px;\n"
                                         "border-radius:20px;\n"
                                         "border:2px solid rgb(136, 216, 208);\n"
                                         "color:rgb(22, 29, 111);")

        checkBox_richiesta.setText(f"Nome: {amico_attesa.get_nome()}\nCognome: {amico_attesa.get_cognome()}\nEmail: {amico_attesa.get_email()}")

        return checkBox_richiesta

    def rifiuta_richiesta(self):
        scroll_area_widget_contents = self.scrollArea_richieste.findChild(QWidget)
        for widget in scroll_area_widget_contents.findChildren(QCheckBox):
            if widget.isChecked():
                Gestore_amicizia(widget.objectName()).rifiuta_richiesta_amicizia()

        self.refresh()

    def accetta_richiesta(self):
        scroll_area_widget_contents = self.scrollArea_richieste.findChild(QWidget)
        for widget in scroll_area_widget_contents.findChildren(QCheckBox):
            if widget.isChecked():
                Gestore_amicizia(widget.objectName()).accetta_richiesta_amicizia()

        self.refresh()

    def torna_indietro(self):
        self.pagina_precedente.show()
        self.close()