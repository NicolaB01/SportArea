import pickle
import time

import schedule as schedule

from Gestore.Gestore_campo import Gestore_campo
from Gestore.Gestore_cliente import Gestore_cliente
from Gestore.Gestore_ricevuta import Gestore_ricevuta
from Path.Path_database import PATH_BACKUP


class Backup:
    def __init__(self):
        self.clienti = Gestore_cliente.get_clienti()
        self.campi = Gestore_campo.get_campi()
        self.ricevute = Gestore_ricevuta.get_ricevute()

    def esegui_backup(self):
        with open(PATH_BACKUP, "wb") as f:
            pickle.dump(self.clienti, f)
            pickle.dump(self.campi, f)
            pickle.dump(self.ricevute, f)

    def backup_daily(self):
        schedule.every().day.at("00:00").do(self.esegui_backup)
        while True:
            schedule.run_pending()
            time.sleep(1)