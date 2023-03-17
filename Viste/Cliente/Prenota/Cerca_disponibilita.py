import datetime

from PyQt6 import uic
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QMessageBox, QLabel

from Utils.Eccezioni import ExceptionGiornoFestivo, ExceptionDataPassata, ExceptionOra
from Gestore.Gestore_campo import Gestore_campo
from Gestore.Gestore_prenotazione import Gestore_prenotazione
from Gestore.Gestore_viste import Gestore_viste
from Path.Path_viste import PATH_CERCA_PRENOTAZIONI
from Viste.Cliente.Prenota.Prenota import Prenota


class Cerca_disponibilita(QMainWindow):
    def __init__(self, pagina_precedente):
        super().__init__()
        uic.loadUi(PATH_CERCA_PRENOTAZIONI, self)
        self.pagina_precedente = pagina_precedente
        for orario in range(8, 22):
            self.comboBox_orario.addItem(str(orario) + ":00")

        self.refresh()

        self.pushButton_ricerca.clicked.connect(self.cerca_disponibilita)
        self.pushButton_back.clicked.connect(self.torna_indietro)

    def refresh(self):
        campi = Gestore_campo.get_campi()
        for campo in campi:
            allItems = [self.comboBox_attivita.itemText(i) for i in range(self.comboBox_attivita.count())]
            if campo.get_attivita() not in allItems:
                self.comboBox_attivita.addItem(campo.get_attivita())

        self.cerca_disponibilita()

    #Quando il cliente cerca le fasce orarie disponibili per una certa attività, un certo giorno e da una
    #determinata ora. Il sistema verifica che i parametri per la ricerca siano giusti, se è così allora comparirà a
    #schermo una lista di prenotazioni disponibili relative alle fasce orarie disponibili. Altrimenti verrà
    #visualizzata una finestra di errore.
    def cerca_disponibilita(self):
        self.giorno = int(self.calendarWidget.selectedDate().day())
        self.mese = int(self.calendarWidget.selectedDate().month())
        self.anno = int(self.calendarWidget.selectedDate().year())
        attivita = self.comboBox_attivita.currentText()
        ora_inizio = int(self.comboBox_orario.currentText()[:self.comboBox_orario.currentText().index(":")])
        data_attivita = datetime.datetime(self.anno, self.mese, self.giorno, ora_inizio)

        scroll_area_widget_contents = QWidget()
        vertical_layout = QVBoxLayout(scroll_area_widget_contents)
        vertical_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        try:
            #Gestore_prenotazione.is_data_passata(data_attivita)
            Gestore_prenotazione.is_ora_passata(data_attivita)
            Gestore_prenotazione.is_data_festiva(data_attivita)

            self.prenotazioni_filtrate_diponibili = Gestore_prenotazione.get_fasce_orarie_disponibili(attivita, data_attivita)
            self.riempi_scrollArea()

        except ExceptionDataPassata as e:
            self.calendarWidget.setSelectedDate(datetime.datetime.now())
            self.cerca_disponibilita()
            QMessageBox.warning(self, "Attenzione", e.__str__())
        except ExceptionGiornoFestivo as e:
            vertical_layout.addWidget(self.crea_label_errore(e.__str__()))
            self.scrollArea_prenotazioni.setWidget(scroll_area_widget_contents)
        except ExceptionOra:
            self.prenotazioni_filtrate_diponibili = Gestore_prenotazione.get_fasce_orarie_disponibili(attivita, datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day, datetime.datetime.now().hour + 1))
            self.riempi_scrollArea()

    def riempi_scrollArea(self):
        scroll_area_widget_contents = QWidget()
        vertical_layout = QVBoxLayout(scroll_area_widget_contents)
        vertical_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        ore_prenotabili = self.get_ore_prenotabili()

        for bottoni in ore_prenotabili.values():
            for bottone in bottoni:
                vertical_layout.addWidget(bottone)

        if len(scroll_area_widget_contents.findChildren(QPushButton)) == 0:
            vertical_layout.addWidget(Gestore_viste.crea_label_comunicazione_cliente("Non ci sono più prenotazioni disponibili"))

        self.scrollArea_prenotazioni.setWidget(scroll_area_widget_contents)

    def get_ore_prenotabili(self):
        ore_prenotabili = {}
        for nome_campo, orari_dionibili in self.prenotazioni_filtrate_diponibili.items():
            for ora in orari_dionibili:
                bottone_prenotazione = self.crea_bottoni_prenotazioni(nome_campo, ora)
                bottone_prenotazione.clicked.connect((lambda n_campo=nome_campo,
                                                             data=datetime.datetime(self.anno, self.mese, self.giorno,
                                                                                    int(ora)): lambda: self.seleziona_prenotazione(n_campo, data))())
                if ora not in ore_prenotabili.keys():
                    ore_prenotabili.setdefault(ora, [bottone_prenotazione])
                else:
                    bottoni = ore_prenotabili.get(ora)
                    bottoni.append(bottone_prenotazione)
                    ore_prenotabili[ora] = bottoni

        return dict(sorted(ore_prenotabili.items(), key=lambda x: x[0]))

    def crea_bottoni_prenotazioni(self, nome_campo, ora):
        pusButton_prenotazione = QPushButton()
        pusButton_prenotazione.setMinimumSize(QSize(150, 0))
        pusButton_prenotazione.setFont(QFont("Arial", 15, 50, False))
        pusButton_prenotazione.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        pusButton_prenotazione.setStyleSheet("QPushButton\n"
                                             "{\n"
                                             "color:rgb(22, 29, 111);\n"
                                             "background-color: rgba(255, 255, 255, 0);\n"
                                             "border: 3px solid rgb(136, 216, 208);\n"
                                             "padding-left:-5px;\n"
                                             "padding-right:-5px;\n"
                                             "width=125px\n"
                                             "}\n"
                                             "\n"
                                             "QPushButton:hover\n"
                                             "{\n"
                                             "color:rgb(22, 29, 111);\n"
                                             "background-color: rgba(255, 255, 255, 0);\n"
                                             "border-radius:30px;\n"
                                             "}\n"
                                             "\n"
                                             "QPushButton:pressed\n"
                                             "{\n"
                                             "color:rgb(22, 29, 111);\n"
                                             "background-color: rgb(136, 216, 208);\n"
                                             "border-radius:25px;\n"
                                             "}\n"
                                             "\n"
                                             "\n"
                                             "\n"
                                             "\n"
                                             "")
        campo = Gestore_campo.cerca_campo(nome_campo)
        pusButton_prenotazione.setText(f"Attività:{campo.get_attivita()}\nCampo: {campo.get_nome_campo()}\nOra: {ora}:00\nPartecipanti: {campo.get_numero_max_partecipanti()}\nPrezzo: {campo.get_prezzo()}")
        return pusButton_prenotazione

    def seleziona_prenotazione(self, nome_campo, data):
        self.conferma_prenotazione = Prenota(self, self.pagina_precedente, nome_campo, data, False)
        self.conferma_prenotazione.show()
        self.close()

    def crea_label_errore(self, errore):
        prenotazione_passata = QLabel()
        prenotazione_passata.setFont(QFont("Arial", 14, 50, False))
        prenotazione_passata.setStyleSheet("background-color:rgba(255, 255, 255, 0);\n"
                                           "padding:5px;\n"
                                           "border-radius:20px;\n"
                                           "border:2px solid rgb(152, 222, 217);\n"
                                           "color:rgb(22, 29, 111);")
        prenotazione_passata.setText(errore)
        return prenotazione_passata

    def torna_indietro(self):
        self.pagina_precedente.show()
        self.close()
