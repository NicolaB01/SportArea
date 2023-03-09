import sys

from PyQt6.QtWidgets import QApplication

from Viste.Accesso.Home import Home

if __name__ == "__main__":
    global nuovo_processo
    app = QApplication(sys.argv)
    mainwindow = Home()
    mainwindow.show()
    sys.exit(app.exec())