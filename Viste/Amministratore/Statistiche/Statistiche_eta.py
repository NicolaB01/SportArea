from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from Gestore.Statistiche import Statistiche
from Path.Path_viste import PATH_STATISTICHE_ETA


class Grafico_età_media(FigureCanvas):
    def __init__(self):
        self.fig = Figure(figsize=(10, 3), dpi=90)
        super(Grafico_età_media, self).__init__(self.fig)
        self.axes = self.fig.add_subplot(111)
        self.statistiche_età = Statistiche.stat_anagrafiche()
        self.hist = None
        self.linea_media = None
        self.legenda = None

    def update_chart(self):
        self.fig.set_facecolor("#A5C9CA")
        self.axes.set_facecolor("#A5C9CA")
        self.axes.xaxis.set_label_position('top')
        self.axes.set_ylabel("Numero di iscritti")

        if self.hist or self.linea_media or self.legenda:
            self.hist.remove()
            self.linea_media.remove()
            self.legenda.remove()

        self.hist = self.axes.hist(self.statistiche_età, range(0,111,5), label="Fasce d'età", color="royalblue")
        self.linea_media = self.axes.axvline(Statistiche.età_media(), color = "r", label="Età media")
        self.legenda = self.axes.legend(facecolor='#A5C9CA', framealpha=0)

        self.draw()


class Statistiche_eta(QMainWindow):
    def __init__(self, pagina_precedente):
        super().__init__()
        uic.loadUi(PATH_STATISTICHE_ETA, self)
        self.pagina_precedente = pagina_precedente

        self.eta_media.setText(str(Statistiche.età_media()))

        self.grafico = Grafico_età_media()
        self.grafico.update_chart()
        vertical_layout = QVBoxLayout(self.frame_grafico)
        vertical_layout.addWidget(self.grafico)

        self.pushButton_back.clicked.connect(self.torna_indietro)

    def torna_indietro(self):
        self.pagina_precedente.show()
        self.close()