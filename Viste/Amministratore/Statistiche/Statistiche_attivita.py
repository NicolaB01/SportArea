from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from Gestore.Statistiche import Statistiche
from Path.Path_viste import PATH_STATISTICHE_ATTIVITA


class Grafico_attività(FigureCanvas):
    def __init__(self):
        self.fig = Figure(figsize=(10, 3), dpi=90)
        super(Grafico_attività, self).__init__(self.fig)
        self.axes = self.fig.add_subplot(111)
        self.statistiche_attività = Statistiche.stat_attività()
        print(self.statistiche_attività)
        self.pie = None
        self.legenda = None

    def update_chart(self):
        self.fig.set_facecolor("#A5C9CA")
        self.axes.set_facecolor("#A5C9CA")
        self.axes.xaxis.set_label_position('top')

        if self.pie or self.legenda:
            self.pie.remove()
            self.legenda.remove()

        self.pie = self.axes.pie(self.statistiche_attività.values(), wedgeprops={"edgecolor": "black"}, autopct=lambda p : '{:.2f}%  ({:,.0f})'.format(p,p * sum(self.statistiche_attività.values())/100))
        self.legenda = self.axes.legend(self.statistiche_attività.keys(), facecolor='#A5C9CA', framealpha=1, title="Attività", loc="best", bbox_to_anchor=(1, 1))

        self.draw()


class Statistiche_attivita(QMainWindow):
    def __init__(self, pagina_precedente):
        super().__init__()
        uic.loadUi(PATH_STATISTICHE_ATTIVITA, self)
        self.pagina_precedente = pagina_precedente

        self.prenotazioni_tot.setText(str(Statistiche.prenotazioni_totali()))

        self.grafico = Grafico_attività()
        self.grafico.update_chart()
        vertical_layout = QVBoxLayout(self.frame_grafico)
        vertical_layout.addWidget(self.grafico)

        self.pushButton_back.clicked.connect(self.torna_indietro)

    def torna_indietro(self):
        self.pagina_precedente.show()
        self.close()