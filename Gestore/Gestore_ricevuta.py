import os
import pickle

from Path.Path_database import PATH_RICEVUTE


class Gestore_ricevuta:
    @classmethod
    def get_ricevute(cls):
        if os.path.getsize(PATH_RICEVUTE) != 0:
            with open(PATH_RICEVUTE, "rb") as f:
                return pickle.load(f)
        return []

    @classmethod
    def set_ricevute(cls, ricevute):
        with open(PATH_RICEVUTE, "wb") as f:
            pickle.dump(ricevute, f, pickle.HIGHEST_PROTOCOL)
