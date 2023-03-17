import datetime

from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from Gestore.Gestore_statistiche import Gestore_statistiche
from Path.Path_viste import PATH_STATISTICHE_FATTURATO


class Grafico_fatturato(FigureCanvas):
    def __init__(self,statistiche_fatturato):
        self.fig = Figure(figsize=(10, 3), dpi=90)
        super(Grafico_fatturato, self).__init__(self.fig)
        self.axes = self.fig.add_subplot(111)
        self.statistiche_fatturato = statistiche_fatturato

    def update_chart(self, anno):
        anno = int(anno)

        self.fig.set_facecolor("#A5C9CA")
        self.axes.set_facecolor("#A5C9CA")
        self.axes.set_xlabel("Mesi")
        self.axes.xaxis.set_label_position('top')
        self.axes.set_ylabel("Incassi")

        self.axes.clear()

        media = Gestore_statistiche.guadagno_medio_annuale(anno)
        self.axes.plot(self.statistiche_fatturato[anno].keys(), self.statistiche_fatturato[anno].values(), label="Incassi", marker=".", color="royalblue")
        self.axes.fill_between(self.statistiche_fatturato[anno].keys(), self.statistiche_fatturato[anno].values(), media, alpha=0.1, color="royalblue")
        self.axes.axhline(media, color="r", label="Media")
        self.axes.legend(facecolor='#A5C9CA', framealpha=0)

        self.draw()


class Statistiche_fatturato(QMainWindow):
    def __init__(self, pagina_precedente):
        super().__init__()
        uic.loadUi(PATH_STATISTICHE_FATTURATO, self)
        self.pagina_precedente = pagina_precedente
        self.anno.setText(str(datetime.datetime.now().year))
        self.statistiche_fatturato = Gestore_statistiche.get_statistiche_fatturato()

        self.grafico = Grafico_fatturato(self.statistiche_fatturato)
        self.grafico.update_chart(self.anno.text())
        vertical_layout = QVBoxLayout(self.frame_grafico)
        vertical_layout.addWidget(self.grafico)


        self.refresh()

        self.pushButton_prima.clicked.connect(self.anno_precedente)
        self.pushButton_dopo.clicked.connect(self.anno_successivo)
        self.pushButton_back.clicked.connect(self.torna_indietro)

    def refresh(self):
        anno_ricerca = int(self.anno.text())

        self.fatturato_annuo.setText(str(Gestore_statistiche.guadagno_annuale(anno_ricerca)))
        self.fatturato_medio.setText(str(round(Gestore_statistiche.guadagno_medio_annuale(anno_ricerca), 2)))

        if anno_ricerca-1 in self.statistiche_fatturato.keys():
            self.pushButton_prima.setEnabled(True)
        else:
            self.pushButton_prima.setEnabled(False)

        if anno_ricerca+1 in self.statistiche_fatturato.keys():
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