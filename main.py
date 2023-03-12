import sys
import threading
import time

import schedule
from PyQt6.QtWidgets import QApplication

from Gestore.Gestore_prenotazione import Gestore_prenotazione
from Gestore.Backup import Backup
from Viste.Accesso.Home import Home

schedule.every(5).seconds.do(Gestore_prenotazione.controlla_scadenza_prenotazioni)
schedule.every().day.at("23:30").do(Backup.esegui_backup)

#Questo metodo effettua i controlli ogni 5 secondi per la scadenza delle prenotazioni e ogni giorno alle 23:30
#effettua il backup del sistema.
def pianificazione():
    while not closing:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    closing = False
    app = QApplication(sys.argv)
    mainwindow = Home()
    mainwindow.show()
    threading.Thread(target=pianificazione).start()
    try:
        sys.exit(app.exec())
    except:
        closing = True

