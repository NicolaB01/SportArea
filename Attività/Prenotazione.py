import os.path
import pickle
import time
import datetime

from Attività.Campo import Campo
from Attività.Cliente import Cliente
from Attività.Ricevuta import Ricevuta
from Path.Path_database import *


class Prenotazione:
    def __init__(self, cliente, data_attività, nome_campo, partecipanti):
        self.cliente = cliente
        self.data_attività = data_attività
        self.nome_campo = nome_campo
        self.partecipanti = partecipanti
        self.attiva = True

    def __str__(self):
        return f"Cliente:\t\t{self.cliente.nome}" \
               f"\nData attività:\t{self.data_attività}" \
               f"\nCampo:\t\t{self.nome_campo}" \
               f"\nPartecipanti:\t{self.partecipanti} "

    def __eq__(self, other):
        return isinstance(other, Prenotazione) and \
               self.cliente == other.cliente and \
               self.data_attività == other.data_attività and \
               self.nome_campo == other.nome_campo

    @classmethod
    def prenota_campo(cls, campo, data_attività, partecipanti):
        prenotazioni = cls.get_prenotazioni_campo(campo)
        prenotazioni.append(Prenotazione(Cliente.get_account_connesso(), data_attività, campo.nome, partecipanti))

        cls.set_prenotazioni_campo(campo, prenotazioni)

    @classmethod
    def filtra_prenotazione(cls, attività, data):
        campi_idonei = []
        campi = Campo.get_campi()
        for campo in campi:
            if campo.attività == attività:
                campi_idonei.append(campo)

        prenotazioni_disponibili = {}
        for campo in campi_idonei:
            lista_ore = list(range(data.hour, 22))
            prenotazioni_effetuate = cls.get_prenotazioni_campo(campo)
            for prenotazione in prenotazioni_effetuate:
                if prenotazione.data_attività.strftime("%x") == data.strftime("%x") and prenotazione.data_attività.hour >= data.hour:
                    lista_ore.remove(prenotazione.data_attività.hour)

            prenotazioni_disponibili[campo.nome] = lista_ore

        return prenotazioni_disponibili

    @classmethod
    def set_prenotazioni_campo(cls, campo, prenotazioni):
        with open(campo.path_prenotazioni, "wb") as f:
            pickle.dump(prenotazioni, f, pickle.HIGHEST_PROTOCOL)

    @classmethod
    def get_prenotazioni_campo(cls, campo):
        if os.path.getsize(campo.path_prenotazioni) != 0:
            with open(campo.path_prenotazioni, "rb") as f:
                return pickle.load(f)
        return []

    @classmethod
    def get_prenotazione_data(cls, campo, data):
        prenotazioni = cls.get_prenotazioni_campo(campo)
        for prenotazione in prenotazioni:
            if prenotazione.data_attività == data:
                return prenotazione
        return None

    def elimina_prenotazione(self):
        campo = Campo.cerca_campo(self.nome_campo)
        prenotazioni = self.get_prenotazioni_campo(campo)
        prenotazioni.remove(self)

        self.set_prenotazioni_campo(campo, prenotazioni)

    def salva_prenotazione(self):
        campo = Campo.cerca_campo(self.nome_campo)
        prenotazioni = self.get_prenotazioni_campo(campo)
        prenotazioni[prenotazioni.index(self)] = self

        self.set_prenotazioni_campo(campo, prenotazioni)

    @classmethod
    def get_prenotazioni_cliente_connesso(cls):
        prenotazioni_per_campo = {}
        campi = Campo.get_campi()
        for campo in campi:
            prenotazioni_effetuate = []
            prenotazioni = cls.get_prenotazioni_campo(campo)
            for prenotazione in prenotazioni:
                if prenotazione.cliente.email == Cliente.get_account_connesso().email:
                    prenotazioni_effetuate.append(prenotazione)

            prenotazioni_effetuate.sort(key=lambda x: x.data_attività)
            prenotazioni_per_campo[campo.nome] = prenotazioni_effetuate

            return prenotazioni_per_campo

    @classmethod
    def controlla_scadenza_prenotazioni(cls):
        while True:
            campi = Campo.get_campi()
            for campo in campi:
                prenotazioni = cls.get_prenotazioni_campo(campo)
                for prenotazione in prenotazioni:
                    if datetime.datetime.now() > prenotazione.data_attività:
                        ricevuta = Ricevuta(datetime.datetime.now(), campo.prezzo, prenotazione)
                        ricevuta.salva_ricevuta()
                        prenotazione.attiva = False

                cls.set_prenotazioni_campo(campo, prenotazioni)

            time.sleep(60)





