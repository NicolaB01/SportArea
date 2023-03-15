import os
import pickle

from Path.Path_database import PATH_RICEVUTE
from Utils.Controller_path import Controller_path


class Gestore_ricevuta:
    #Questo metodo ridà tutte le prenotazioni salvate
    @classmethod
    def get_ricevute(cls):
        Controller_path.genera_path(PATH_RICEVUTE)

        if os.path.getsize(PATH_RICEVUTE) != 0:
            with open(PATH_RICEVUTE, "rb") as f:
                return pickle.load(f)
        return []

    #Questo metodo permette la memorizzazione delle ricevute in un apposito file
    @classmethod
    def set_ricevute(cls, ricevute):
        Controller_path.genera_path(PATH_RICEVUTE)

        with open(PATH_RICEVUTE, "wb") as f:
            pickle.dump(ricevute, f, pickle.HIGHEST_PROTOCOL)
