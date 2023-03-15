import numpy as np
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from Gestore.Gestore_statistiche import Gestore_statistiche
from Path.Path_viste import PATH_STATISTICHE_ETA


class Grafico_eta_media(FigureCanvas):
    def __init__(self):
        self.fig = Figure(figsize=(10, 3), dpi=90)
        super(Grafico_eta_media, self).__init__(self.fig)
        self.axes = self.fig.add_subplot(111)
        self.statistiche_eta = Gestore_statistiche.get_statistiche_eta()

    def update_chart(self):
        self.fig.set_facecolor("#A5C9CA")
        self.axes.set_facecolor("#A5C9CA")
        self.axes.xaxis.set_label_position('top')
        self.axes.set_ylabel("Numero di iscritti")

        self.axes.clear()

        self.axes.hist(self.statistiche_eta, range(0,100,5), label="Fasce d'età", color="royalblue")
        self.axes.axvline(Gestore_statistiche.eta_media(), color = "r", label="Età media")
        self.axes.legend(facecolor='#A5C9CA', framealpha=0)
        self.axes.set_xticks(np.arange(0, 100, 5))

        self.draw()


class Statistiche_eta(QMainWindow):
    def __init__(self, pagina_precedente):
        super().__init__()
        uic.loadUi(PATH_STATISTICHE_ETA, self)
        self.pagina_precedente = pagina_precedente

        self.eta_media.setText(str(round(Gestore_statistiche.eta_media(), 2)))

        self.grafico = Grafico_eta_media()
        self.grafico.update_chart()
        vertical_layout = QVBoxLayout(self.frame_grafico)
        vertical_layout.addWidget(self.grafico)

        self.pushButton_back.clicked.connect(self.torna_indietro)

    def torna_indietro(self):
        self.pagina_precedente.show()
        self.close()