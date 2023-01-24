import datetime

from PyQt6 import uic
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QMessageBox, QLabel

from Attività.Campo import Campo
from Attività.Prenotazione import Prenotazione
from Gestore.Eccezioni import ExceptionGiornoFestivo, ExceptionDataPassata, ExceptionOra
from Gestore.Gestore_viste import Gestore_viste
from Path.Path_viste import PATH_CERCA_PRENOTAZIONI
from Viste.Cliente.Prenota.Prenota import Prenota


class Cerca_prenotazioni(QMainWindow):
    def __init__(self, pagina_precedente):
        super().__init__()
        uic.loadUi(PATH_CERCA_PRENOTAZIONI, self)
        self.pagina_precedente = pagina_precedente
        for orario in range(8, 22):
            self.comboBox_orario.addItem(str(orario) + ":00")

        self.refresh()

        self.pushButton_ricerca.clicked.connect(self.cerca_prenotazioni)
        self.back.clicked.connect(self.torna_indietro)

    def refresh(self):
        self.comboBox_attivita.clear()
        campi = Campo.get_campi()
        for campo in campi:
            allItems = [self.comboBox_attivita.itemText(i) for i in range(self.comboBox_attivita.count())]
            if campo.attività not in allItems:
                self.comboBox_attivita.addItem(campo.attività)

        self.cerca_prenotazioni()

    def cerca_prenotazioni(self):
        self.giorno = int(self.calendarWidget.selectedDate().day())
        self.mese = int(self.calendarWidget.selectedDate().month())
        self.anno = int(self.calendarWidget.selectedDate().year())
        attività = self.comboBox_attivita.currentText()
        ora_inizio = int(self.comboBox_orario.currentText()[:self.comboBox_orario.currentText().index(":")])
        data_attività = datetime.datetime(self.anno, self.mese, self.giorno, ora_inizio)

        scroll_area_widget_contents = QWidget()
        vertical_layout = QVBoxLayout(scroll_area_widget_contents)
        vertical_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        try:
            self.is_data_passata(data_attività)
            if datetime.datetime.now().strftime("%H") > data_attività.strftime("%H") and datetime.datetime.now().strftime("%x").__eq__(data_attività.strftime("%x")):
                raise ExceptionOra("")
            self.is_data_festiva(data_attività)

            self.riempi_scrollArea(attività, data_attività)

        except ExceptionDataPassata as e:
            self.calendarWidget.setSelectedDate(datetime.datetime.now())
            self.cerca_prenotazioni()
            QMessageBox.warning(self, "Attenzione", e.__str__())
        except ExceptionGiornoFestivo as e:
            vertical_layout.addWidget(self.crea_label_errore(e.__str__()))
            self.scrollArea_prenotazioni.setWidget(scroll_area_widget_contents)
        except ExceptionOra:
            self.riempi_scrollArea(attività, datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day, datetime.datetime.now().hour + 1))

    def is_data_passata(self, data_attività):
        if datetime.datetime.now().strftime("%x") > data_attività.strftime("%x"):
            raise ExceptionDataPassata("Non puoi prenotare nessuna attività in questa giornata")

    def is_data_festiva(self, data_attività):
        if data_attività.weekday() == 6:
            raise ExceptionGiornoFestivo("Il cantro sportivo è chiuso")

    #TODO mettere i bottoni ordinati per ora non per campi usa un dizionario es {ora: [lista bottoni per quell'ora ad esempio ordinati in base all'ordine alfabetico del campo}
    def riempi_scrollArea(self, attività, data_attività):
        scroll_area_widget_contents = QWidget()
        vertical_layout = QVBoxLayout(scroll_area_widget_contents)
        vertical_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        prenotazioni_filtrate_diponibili = Prenotazione.filtra_prenotazione(attività, data_attività)

        for nome_campo, orari_dionibili in prenotazioni_filtrate_diponibili.items():
            for ora in orari_dionibili:
                bottone_prenotazione = self.crea_bottoni_prenotazioni(nome_campo, ora)
                bottone_prenotazione.clicked.connect((lambda n_campo=nome_campo, data=datetime.datetime(self.anno, self.mese, self.giorno, int(ora)): lambda: self.prenota(n_campo, data))())
                vertical_layout.addWidget(bottone_prenotazione)

        if len(scroll_area_widget_contents.findChildren(QPushButton)) == 0:
            vertical_layout.addWidget(Gestore_viste.crea_label_comunicazione("Non ci sono più prenotazioni disponibili"))

        self.scrollArea_prenotazioni.setWidget(scroll_area_widget_contents)

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
        campo = Campo.cerca_campo(nome_campo)
        pusButton_prenotazione.setText(f"Campo: {campo.nome}\nOra: {ora}:00\nPartecipanti: {campo.numero_max_partecipanti}\nPrezzo: {campo.prezzo}")
        return pusButton_prenotazione

    def prenota(self, nome_campo, data):
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
