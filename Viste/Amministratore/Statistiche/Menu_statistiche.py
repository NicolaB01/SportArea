import datetime

from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QMessageBox

from Gestore.Gestore_statistiche import Gestore_statistiche
from Path.Path_viste import PATH_MENU_STATISTICHE
from Viste.Amministratore.Statistiche.Statistiche_attivita import Statistiche_attivita
from Viste.Amministratore.Statistiche.Statistiche_eta import Statistiche_eta
from Viste.Amministratore.Statistiche.Statistiche_fatturato import Statistiche_fatturato
from Viste.Amministratore.Statistiche.Statistiche_iscrizioni import Statistiche_iscrizioni


class Menu_statistiche(QMainWindow):
    def __init__(self, pagina_precedente):
        super().__init__()
        uic.loadUi(PATH_MENU_STATISTICHE, self)
        self.pagina_precedente = pagina_precedente


        self.pushButton_stat_iscrizioni.clicked.connect(self.statistiche_iscrizioni)
        self.pushButton_stat_eta.clicked.connect(self.statistiche_eta)
        self.pushButton_stat_attivita.clicked.connect(self.statistiche_attivita)
        self.pushButton_stat_fatturato.clicked.connect(self.statistiche_fatturato)
        self.pushButton_back.clicked.connect(self.torna_indietro)

    #Quando l'amministratore vuole vedere le statistiche relative alle iscrizioni e non ci sono dati disponibili il
    # programma visualizza una finse tra di errore. Se i dati sono presenti si apre la pagina con il grafico delle
    # statistiche
    def statistiche_iscrizioni(self):
        if datetime.datetime.now().year in Gestore_statistiche.stat_iscrizioni().keys():
            self.stat1 = Statistiche_iscrizioni(self)
            self.stat1.show()
            self.close()
        else:
            QMessageBox.warning(self, "Attenzione!", "Non ci sono statistiche relative alle iscrizioni")

    # Quando l'amministratore vuole vedere le statistiche relative all'età dei clienti e non ci sono dati disponibili il
    # programma visualizza una finse tra di errore. Se i dati sono presenti si apre la pagina con il grafico delle
    # statistiche
    def statistiche_eta(self):
        if len(Gestore_statistiche.get_statistiche_eta()):
            self.stat2 = Statistiche_eta(self)
            self.stat2.show()
            self.close()
        else:
            QMessageBox.warning(self, "Attenzione!", "Non ci sono statistiche relative ai dati anagrafici")

    # Quando l'amministratore vuole vedere le statistiche relative alle attività e non ci sono dati disponibili il
    # programma visualizza una finse tra di errore. Se i dati sono presenti si apre la pagina con il grafico delle
    # statistiche
    def statistiche_attivita(self):
        if datetime.datetime.now().year in Gestore_statistiche.stat_attivita().keys():
            self.stat3 = Statistiche_attivita(self)
            self.stat3.show()
            self.close()
        else:
            QMessageBox.warning(self, "Attenzione!", "Non ci sono statistiche relative alle attività")

    # Quando l'amministratore vuole vedere le statistiche relative al fatturato e non ci sono dati disponibili il
    # programma visualizza una finse tra di errore. Se i dati sono presenti si apre la pagina con il grafico delle
    # statistiche
    def statistiche_fatturato(self):
        if datetime.datetime.now().year in Gestore_statistiche.stat_bilancio().keys():
            self.stat4 = Statistiche_fatturato(self)
            self.stat4.show()
            self.close()
        else:
            QMessageBox.warning(self, "Attenzione!", "Non ci sono statistiche relative al fatturato")

    def torna_indietro(self):
        self.pagina_precedente.show()
        self.close()