import pickle
import shutil

from Gestore.Gestore_campo import Gestore_campo
from Gestore.Gestore_cliente import Gestore_cliente
from Gestore.Gestore_ricevuta import Gestore_ricevuta
from Path.Path_database import PATH_BACKUP


class Backup:
    def __init__(self):
        self.clienti = Gestore_cliente.get_clienti()
        self.campi = Gestore_campo.get_campi()
        self.ricevute = Gestore_ricevuta.get_ricevute()

    @classmethod
    def esegui_backup(cls):
        pass