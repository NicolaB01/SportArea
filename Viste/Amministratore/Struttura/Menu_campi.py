import os.path
import pickle

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QCheckBox, QWidget

from Attività.Campo import Campo
from Viste.Amministratore.Struttura.Crea_campo import Crea_campo


class Menu_campi(QMainWindow):
    def __init__(self, pagina_precedente):
        super().__init__()
        uic.loadUi("/Users/nicola/PycharmProjects/ProgettoIDS/UI/SportArea-V_Campi.ui", self)
        self.pagina_precedente = pagina_precedente

        self.refresh()

        self.pushButton_elimina.clicked.connect(self.elimina_campi)
        self.pushButton_nuovo.clicked.connect(self.menu_nuovo_campo)
        self.pushButton_back.clicked.connect(self.torna_indietro)

    def refresh(self):
        scroll_area_widget_contents = QWidget()
        vertical_layout = QVBoxLayout(scroll_area_widget_contents)

        vertical_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        if os.path.getsize(Campo.PATH_INFOCAMPI) != 0:
            with open(Campo.PATH_INFOCAMPI, "rb") as f:
                campi = pickle.load(f)
                for campo in campi:
                    vertical_layout.addWidget(self.crea_checkBox(campo))

        self.scrollArea_campi.setWidget(scroll_area_widget_contents)

    def crea_checkBox(self, campo):
        checkBox_richiesta = QCheckBox()

        checkBox_richiesta.setFont(QFont("Arial", 14, 50, False))
        checkBox_richiesta.setObjectName(campo.nome)
        checkBox_richiesta.setStyleSheet("background-color:rgba(255, 255, 255, 0);\n"
                                         "padding:5px;\n"
                                         "border-radius:20px;\n"
                                         "border:2px solid rgb(52, 119, 134);\n"
                                         "color:rgb(44, 51, 51);")

        checkBox_richiesta.setText(
            f"Nome: {campo.nome}\nAttività: {campo.attività}\nPrezzo: {campo.prezzo}\nNumero partecipanti: {campo.numero_max_partecipanti}")

        return checkBox_richiesta

    def elimina_campi(self):
        scroll_area_widget_contents = self.scrollArea_campi.findChild(QWidget)
        for widget in scroll_area_widget_contents.findChildren(QCheckBox):
            if widget.isChecked():

                nome_campo = widget.objectName()
                Campo.elimina_campo(Campo.cerca_campo(nome_campo))

        self.refresh()

    def menu_nuovo_campo(self):
        self.menu_crea_campo = Crea_campo(self)
        self.menu_crea_campo.show()
        self.close()

    def torna_indietro(self):
        self.pagina_precedente.show()
        self.close()
