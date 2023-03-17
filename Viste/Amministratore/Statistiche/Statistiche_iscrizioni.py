import datetime

from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from Utils.Eccezioni import ExceptionAnnoNonPresente
from Gestore.Gestore_cliente import Gestore_cliente
from Gestore.Gestore_statistiche import Gestore_statistiche
from Path.Path_viste import PATH_STATISTICHE_ISCRIZIONI


class Grafico_iscrizioni(FigureCanvas):
    def __init__(self,statistiche_iscrizioni):
        self.fig = Figure(figsize=(10, 3), dpi=90)
        super(Grafico_iscrizioni, self).__init__(self.fig)
        self.axes = self.fig.add_subplot(111)
        self.statistiche_iscrizioni = statistiche_iscrizioni

    def update_chart(self, anno):
        anno = int(anno)

        self.fig.set_facecolor("#A5C9CA")
        self.axes.set_facecolor("#A5C9CA")
        self.axes.set_xlabel("Mesi")
        self.axes.xaxis.set_label_position('top')
        self.axes.set_ylabel("Numero di iscritti")

        self.axes.clear()
        self.axes.bar(self.statistiche_iscrizioni[anno].keys(), self.statistiche_iscrizioni[anno].values(), label="Iscrizioni", color="royalblue")
        self.axes.axhline(Gestore_statistiche.iscrizioni_medie_annuali(anno), color="r", label="Media")
        self.axes.legend(facecolor='#A5C9CA', framealpha=0)
        self.axes.margins(0.2, 0.2)

        barre = self.axes.patches
        for rect, label in zip(barre, self.statistiche_iscrizioni[anno].values()):
            height = rect.get_height()
            if label:
                self.axes.text(rect.get_x() + rect.get_width() / 2, height + 0.01, int(label), ha="center", va="bottom")

        self.draw()


class Statistiche_iscrizioni(QMainWindow):
    def __init__(self, pagina_precedente):
        super().__init__()
        uic.loadUi(PATH_STATISTICHE_ISCRIZIONI, self)
        self.pagina_precedente = pagina_precedente
        self.anno.setText(str(datetime.datetime.now().year))
        self.statistiche_iscrizioni = Gestore_statistiche.get_statistiche_iscrizioni()

        self.grafico = Grafico_iscrizioni(self.statistiche_iscrizioni)
        self.grafico.update_chart(self.anno.text())
        vertical_layout = QVBoxLayout(self.frame_grafico)
        vertical_layout.addWidget(self.grafico)

        self.refresh()

        self.pushButton_prima.clicked.connect(self.anno_precedente)
        self.pushButton_dopo.clicked.connect(self.anno_successivo)
        self.pushButton_back.clicked.connect(self.torna_indietro)

    def refresh(self):
        anno_ricerca = int(self.anno.text())

        try:
            self.numero_iscrizioni_tot.setText(str(len(Gestore_cliente.get_clienti())))
            self.numero_iscrizioni_annue.setText(str(Gestore_statistiche.iscrizioni_annuali(anno_ricerca)))
            self.numero_iscrizioni_media.setText(str(round(Gestore_statistiche.iscrizioni_medie_annuali(anno_ricerca), 2)))
        except ExceptionAnnoNonPresente:
            self.numero_iscrizioni_tot.setText(str(0))
            self.numero_iscrizioni_annue.setText(str(0))
            self.numero_iscrizioni_media.setText(str(0))

        if anno_ricerca-1 in self.statistiche_iscrizioni.keys():
            self.pushButton_prima.setEnabled(True)
        else:
            self.pushButton_prima.setEnabled(False)

        if anno_ricerca+1 in self.statistiche_iscrizioni.keys():
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