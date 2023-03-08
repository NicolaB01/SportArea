import os.path
import pickle
from Path.Path_database import *


class Ricevuta():
    def __init__(self, data_emissione, prezzo, prenotazione):
        self.data_emissione = data_emissione
        self.prezzo = prezzo
        self.prenotazione = prenotazione

    def __str__(self):
        return f"Data_emissione:\t{self.data_emissione.day}/{self.data_emissione.month}/{self.data_emissione.year} {self.data_emissione.strftime('%H')}:{self.data_emissione.strftime('%M')}" \
               f"\nPrezzo:\t\t{self.prezzo}" \
               f"\nCliente:\t\t{self.prenotazione.cliente.nome} {self.prenotazione.cliente.cognome}" \
               f"\nCampo:\t\t{self.prenotazione.nome_campo}" \
               f"\nData attività:\t{self.prenotazione.data_attività.day}/{self.prenotazione.data_attività.month}/{self.prenotazione.data_attività.year} {self.prenotazione.data_attività.strftime('%H')}:{self.prenotazione.data_attività.strftime('%M')}"

    def __eq__(self, other):
        return isinstance(other,
                          Ricevuta) and self.prezzo == other.prezzo and self.prenotazione == other.prenotazione

    def salva_ricevuta(self):
        ricevute = self.get_ricevute()

        if self not in ricevute:
            ricevute.append(self)
            self.set_ricevute(ricevute)

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