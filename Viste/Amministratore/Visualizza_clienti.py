from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel

from Attività.Cliente import Cliente


class Visualizza_clienti(QMainWindow):
    def __init__(self, pagina_precedente):
        super().__init__()
        uic.loadUi("/Users/nicola/PycharmProjects/ProgettoIDS/UI/SportArea-V_Clienti.ui", self)
        self.pagina_precedente = pagina_precedente

        self.setUp()

        self.pushButton_back.clicked.connect(self.torna_indietro)

    def setUp(self):
        scroll_area_widget_contents = QWidget()
        vertical_layout = QVBoxLayout(scroll_area_widget_contents)
        vertical_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        for cliente in Cliente.get_clienti():
            vertical_layout.addWidget(self.crea_label_cliente(cliente))

        self.scrollArea_clienti.setWidget(scroll_area_widget_contents)

    def crea_label_cliente(self, cliente):
        prenotazione_passata = QLabel()
        prenotazione_passata.setFont(QFont("Arial", 14, 50, False))
        prenotazione_passata.setStyleSheet("background-color:rgba(255, 255, 255, 0);\n"
                                           "padding:5px;\n"
                                           "border-radius:20px;\n"
                                           "border:2px solid rgb(52, 119, 134);\n"
                                           "color:rgb(44, 51, 51);")
        prenotazione_passata.setText(cliente.__str__())
        return prenotazione_passata


    def torna_indietro(self):
        self.pagina_precedente.show()
        self.close()