import os
import pickle

from Utils.Controller_path import Controller_path
from Utils.Eccezioni import ExceptionCampoInesistente
from Path.Path_database import PATH_INFO_CAMPI


class Gestore_campo:
    #Questo metodo permetta la ricerca di un campo attraverso il nome
    @classmethod
    def cerca_campo(cls, nome):
        campi = cls.get_campi()
        for campo in campi:
            if campo.get_nome_campo() == nome:
                return campo
        raise ExceptionCampoInesistente()

    #Questo metodo restituisce tutti i campi salvati
    @classmethod
    def get_campi(cls):
        Controller_path.genera_path(PATH_INFO_CAMPI)

        if os.path.getsize(PATH_INFO_CAMPI) != 0:
            with open(PATH_INFO_CAMPI, "rb") as f:
                return pickle.load(f)
        return []

    #Questo metodo permette il salvataggio dei campi su un file
    @classmethod
    def set_campi(cls, campi):
        Controller_path.genera_path(PATH_INFO_CAMPI)

        with open(PATH_INFO_CAMPI, "wb") as f:
            pickle.dump(campi, f, pickle.HIGHEST_PROTOCOL)
