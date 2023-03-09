from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QCheckBox, QWidget, QLabel

from Gestore.Gestore_campo import Gestore_campo
from Gestore.Gestore_viste import Gestore_viste
from Path.Path_viste import PATH_VISUALIZZA_CAMPI
from Viste.Amministratore.Struttura.Crea_campo import Crea_campo


class Menu_campi(QMainWindow):
    def __init__(self, pagina_precedente):
        super().__init__()
        uic.loadUi(PATH_VISUALIZZA_CAMPI, self)
        self.pagina_precedente = pagina_precedente

        self.refresh()

        self.pushButton_elimina.clicked.connect(self.elimina_campi)
        self.pushButton_nuovo.clicked.connect(self.menu_nuovo_campo)
        self.pushButton_back.clicked.connect(self.torna_indietro)

    def refresh(self):
        scroll_area_widget_contents = QWidget()
        vertical_layout = QVBoxLayout(scroll_area_widget_contents)

        vertical_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        campi = Gestore_campo.get_campi()
        for campo in campi:
            vertical_layout.addWidget(self.crea_checkBox(campo))

        if len(scroll_area_widget_contents.findChildren(QCheckBox)) == 0:
            vertical_layout.addWidget(Gestore_viste.crea_label_comunicazione_admin("La lista dei campi è vuota!\nCreane uno premendo Nuovo Campo"))

        self.scrollArea_campi.setWidget(scroll_area_widget_contents)

    def crea_checkBox(self, campo):
        checkBox_richiesta = QCheckBox()

        checkBox_richiesta.setFont(QFont("Arial", 14, 50, False))
        checkBox_richiesta.setObjectName(campo.get_nome_campo())
        checkBox_richiesta.setStyleSheet("background-color:rgba(255, 255, 255, 0);\n"
                                         "padding:5px;\n"
                                         "border-radius:20px;\n"
                                         "border:2px solid rgb(52, 119, 134);\n"
                                         "color:rgb(44, 51, 51);")

        checkBox_richiesta.setText(campo.__str__())
        return checkBox_richiesta

    def elimina_campi(self):
        scroll_area_widget_contents = self.scrollArea_campi.findChild(QWidget)
        for widget in scroll_area_widget_contents.findChildren(QCheckBox):
            if widget.isChecked():
                nome_campo = widget.objectName()
                Gestore_campo.cerca_campo(nome_campo).elimina_campo()

        self.refresh()

    def menu_nuovo_campo(self):
        self.menu_crea_campo = Crea_campo(self)
        self.menu_crea_campo.show()
        self.close()

    def torna_indietro(self):
        self.pagina_precedente.show()
        self.close()
