import os
import pickle

from Utils.Eccezioni import ExceptionCampoInesistente
from Path.Path_database import PATH_INFO_CAMPI


class Gestore_campo:
    @classmethod
    def cerca_campo(cls, nome):
        campi = cls.get_campi()
        for campo in campi:
            if campo.get_nome_campo() == nome:
                return campo
        raise ExceptionCampoInesistente()

    @classmethod
    def get_campi(cls):
        if os.path.getsize(PATH_INFO_CAMPI) != 0:
            with open(PATH_INFO_CAMPI, "rb") as f:
                return pickle.load(f)
        return []

    @classmethod
    def set_campi(cls, campi):
        with open(PATH_INFO_CAMPI, "wb") as f:
            pickle.dump(campi, f, pickle.HIGHEST_PROTOCOL)