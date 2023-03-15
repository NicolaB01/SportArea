import datetime

from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from Gestore.Gestore_statistiche import Gestore_statistiche
from Path.Path_viste import PATH_STATISTICHE_ATTIVITA


class Grafico_attivita(FigureCanvas):
    def __init__(self):
        self.fig = Figure(figsize=(10, 3), dpi=90)
        super(Grafico_attivita, self).__init__(self.fig)
        self.axes = self.fig.add_subplot(111)
        self.statistiche_attivita = Gestore_statistiche.stat_attivita()
        self.pie = None

    def update_chart(self, anno):
        anno = int(anno)

        self.fig.set_facecolor("#A5C9CA")
        self.axes.set_facecolor("#A5C9CA")
        self.axes.xaxis.set_label_position('top')

        if self.pie:
            self.axes.clear()

        self.pie = self.axes.pie(self.statistiche_attivita[anno].values(), wedgeprops={"edgecolor": "black"}, labels=self.statistiche_attivita[anno].keys(), autopct="%1.1f%%")

        self.draw()


class Statistiche_attivita(QMainWindow):
    def __init__(self, pagina_precedente):
        super().__init__()
        uic.loadUi(PATH_STATISTICHE_ATTIVITA, self)
        self.pagina_precedente = pagina_precedente
        self.anno.setText(str(datetime.datetime.now().year))
        self.statistiche_prenotazioni = Gestore_statistiche.stat_attivita()

        self.prenotazioni_tot.setText(str(Gestore_statistiche.prenotazioni_totali()))

        self.grafico = Grafico_attivita()
        self.grafico.update_chart(self.anno.text())
        vertical_layout = QVBoxLayout(self.frame_grafico)
        vertical_layout.addWidget(self.grafico)

        self.refresh()

        self.pushButton_prima.clicked.connect(self.anno_precedente)
        self.pushButton_dopo.clicked.connect(self.anno_successivo)
        self.pushButton_back.clicked.connect(self.torna_indietro)

    def refresh(self):
        anno_ricerca = int(self.anno.text())

        if anno_ricerca in self.statistiche_prenotazioni.keys():
            self.prenotazioni_annuali.setText(str(Gestore_statistiche.prenotazioni_annuali(anno_ricerca)))
        else:
            self.prenotazioni_annuali.setText(str(0))


        if anno_ricerca-1 in self.statistiche_prenotazioni.keys():
            self.pushButton_prima.setEnabled(True)
        else:
            self.pushButton_prima.setEnabled(False)

        if anno_ricerca+1 in self.statistiche_prenotazioni.keys():
            self.pushButton_dopo.setEnabled(True)
        else:
            self.pushButton_dopo.setEnabled(False)

    def anno_precedente(self):
        self.anno.setText(str(int(self.anno.text()) - 1))
        self.grafico.update_chart(self.anno.text())
        self.refresh()

    def anno_successivo(self):
        self.anno.setText(str(int(self.anno.text()) + 1))
        self.grafico.update_chart(self.anno.text())
        self.refresh()

    def torna_indietro(self):
        self.pagina_precedente.show()
        self.close()