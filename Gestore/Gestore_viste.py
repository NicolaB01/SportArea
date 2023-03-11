import time

import schedule
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel


class Gestore_viste:
    @classmethod
    def crea_label_comunicazione_admin(cls, msg):
        prenotazione_passata = QLabel()
        prenotazione_passata.setFont(QFont("Arial", 14, 50, False))
        prenotazione_passata.setStyleSheet("background-color:rgba(255, 255, 255, 0);\n"
                                           "padding:5px;\n"
                                           "border-radius:20px;\n"
                                           "border:2px solid rgb(52, 119, 134);\n"
                                           "color:rgb(44, 51, 51);")
        prenotazione_passata.setText(f"Comunicazione\n{msg}")
        return prenotazione_passata

    @classmethod
    def crea_label_comunicazione_cliente(cls, msg):
        prenotazione_passata = QLabel()
        prenotazione_passata.setFont(QFont("Arial", 14, 50, False))
        prenotazione_passata.setStyleSheet("background-color:rgba(255, 255, 255, 0);\n"
                                           "padding:5px;\n"
                                           "border-radius:20px;\n"
                                           "border:2px solid rgb(136, 216, 208);\n"
                                           "color:rgb(22, 29, 111);")
        prenotazione_passata.setText(f"Comunicazione\n{msg}")
        return prenotazione_passata

