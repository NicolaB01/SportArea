import os.path
import pickle
from Path.Path_database import *


class Campo:
    def __init__(self, nome, numero_max_partecipanti, prezzo, attività):
        self.nome = nome
        self.numero_max_partecipanti = numero_max_partecipanti
        self.prezzo = prezzo
        self.attività = attività
        self.path_prenotazioni = os.path.join("..", f"/DataBase/Campi/camppo_{self.nome}.txt")

    def __str__(self):
        return f"Nome:\t{self.nome}" \
               f"\nNumero max partecipanti:{self.numero_max_partecipanti}" \
               f"\nprezzo:\t{self.prezzo}" \
               f"\nattività:\t{self.attività}"

    def __eq__(self, other):
        return isinstance(other,
                          Campo) and self.nome == other.nome and self.prezzo == other.prezzo and self.numero_max_partecipanti == other.numero_max_partecipanti and self.attività == other.attività

    @classmethod
    def crea_campo(cls, nome, numero_max_partecipanti, prezzo, attività):
        già_presente = False
        campi = cls.get_campi()
        for campo in campi:
            if campo.nome == nome:
                già_presente = True

        if not già_presente:
            nuovo_campo = Campo(nome, numero_max_partecipanti, prezzo, attività)
            campi.append(nuovo_campo)
            cls.set_campi(campi)

            open(nuovo_campo.path_prenotazioni, "x")

    def elimina_campo(self):
        campi = self.get_campi()
        campi.remove(self)
        os.remove(self.path_prenotazioni)
        self.set_campi(campi)

    @classmethod
    def cerca_campo(cls, nome):
        campi = cls.get_campi()
        for campo in campi:
            if campo.nome == nome:
                return campo

        return None

    @classmethod
    def get_campi(cls):
        if os.path.getsize(PATH_INFO_CAMPI) != 0:
            with open(PATH_INFO_CAMPI, "rb") as f:
                return pickle.load(f)
        return []

    def set_campi(self, campi):
        with open(PATH_INFO_CAMPI, "wb") as f:
            pickle.dump(campi, f, pickle.HIGHEST_PROTOCOL)