import time

from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QMessageBox

from Attivita.Campo import Campo
from Path.Path_viste import PATH_CREA_CAMPO
from Utils.Eccezioni import ExceptionNomeCampoUtilizzato


class Crea_campo(QMainWindow):
    def __init__(self, pagina_precedente):
        super().__init__()
        uic.loadUi(PATH_CREA_CAMPO, self)
        self.pagina_precedente = pagina_precedente

        self.pushButton_back.clicked.connect(self.torna_indietro)
        self.pushButton_conferma.clicked.connect(self.crea_campo)

    #Quando l'amministratore vuole inserire un nuovo campo passando i parametri per la registrazione, se il nome
    # del campo non è già in uso, il campo viene aggiungo ai campi disponibili.
    def crea_campo(self):
        nome = self.lineEdit_nomeCampo.text().strip().capitalize()
        numero_max_partecipanti = self.spinBox_partecipanti.value()
        prezzo =  self.doubleSpinBox_prezzo.value()
        attività = self.lineEdit_attivita.text().strip().capitalize()

        try:
            Campo.crea_campo(nome, numero_max_partecipanti, prezzo, attività)
        except ExceptionNomeCampoUtilizzato as e:
            QMessageBox.warning(self, "Attenzione", e.__str__())

        self.torna_indietro()

    def torna_indietro(self):
        time.sleep(0.15)
        self.pagina_precedente.refresh()
        self.pagina_precedente.show()
        self.close()