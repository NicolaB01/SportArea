import datetime
import os
import shutil

from Gestore.Gestore_campo import Gestore_campo
from Gestore.Gestore_cliente import Gestore_cliente
from Gestore.Gestore_ricevuta import Gestore_ricevuta
from Path.Path_database import PATH_BACKUP, PATH_DATI


class Backup:
    def __init__(self):
        self.clienti = Gestore_cliente.get_clienti()
        self.campi = Gestore_campo.get_campi()
        self.ricevute = Gestore_ricevuta.get_ricevute()

    @classmethod
    def esegui_backup(cls):
        file_name = datetime.datetime.now().strftime("%d_%b_%Y")
        percorsoBackup = os.path.join(PATH_BACKUP, file_name)
        shutil.copytree(PATH_DATI, percorsoBackup)
