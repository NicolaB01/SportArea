import pickle
import time

import schedule as schedule

from Attività.Campo import Campo
from Attività.Cliente import Cliente
from Attività.Ricevuta import Ricevuta
from Path.Path_database import PATH_BACKUP


class Backup:
    def __init__(self):
        self.clienti = Cliente.get_clienti()
        self.campi = Campo.get_campi()
        self.ricevute = Ricevuta.get_ricevute()

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