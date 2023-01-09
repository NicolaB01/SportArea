import sys

from PyQt6.QtWidgets import QApplication

from Viste.Home import Home

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = Home()
    mainwindow.show()
    sys.exit(app.exec())