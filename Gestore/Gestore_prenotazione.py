import datetime
import os
import pickle

from Attivita.Ricevuta import Ricevuta
from Utils.Controller_path import Controller_path
from Utils.Eccezioni import ExceptionGiornoFestivo, ExceptionDataPassata, ExceptionOra, \
    ExceptionPrenotazioneInesistente, ExceptionPreotazioneNonModificabile
from Gestore.Gestore_campo import Gestore_campo
from Gestore.Gestore_cliente import Gestore_cliente


class Gestore_prenotazione:
    @classmethod
    def cerca_prenotazione(cls, campo, data):
        prenotazioni = cls.get_prenotazioni_campo(campo)
        for prenotazione in prenotazioni:
            if prenotazione.get_data_attività().__eq__(data):
                return prenotazione

        raise ExceptionPrenotazioneInesistente()

    @classmethod
    def get_fasce_orarie_disponibili(cls, attività, data):
        campi_idonei = cls.campi_idonei_attività(attività)

        fasce_orarie_disponibili = {}
        for campo in campi_idonei:
            lista_ore = list(range(data.hour, 22))
            prenotazioni = cls.get_prenotazioni_campo(campo)
            for prenotazione in prenotazioni:
                if prenotazione.get_data_attività().strftime("%x").__eq__(data.strftime("%x")) and prenotazione.get_data_attività().hour >= data.hour:
                    lista_ore.remove(prenotazione.get_data_attività().hour)

            fasce_orarie_disponibili[campo.get_nome_campo()] = lista_ore

        return fasce_orarie_disponibili

    @classmethod
    def campi_idonei_attività(cls, attività):
        campi_idonei = []
        campi = Gestore_campo.get_campi()
        for campo in campi:
            if campo.get_attività() == attività:
                campi_idonei.append(campo)

        return campi_idonei

    @classmethod
    def get_prenotazioni_cliente_connesso(cls):
        prenotazioni_per_campo = {}
        campi = Gestore_campo.get_campi()
        for campo in campi:
            prenotazioni_effetuate = []
            prenotazioni = cls.get_prenotazioni_campo(campo)
            for prenotazione in prenotazioni:
                if prenotazione.get_cliente().__eq__(Gestore_cliente.get_account_connesso()):
                    prenotazioni_effetuate.append(prenotazione)

            prenotazioni_effetuate.sort(key=lambda x: x.data_attività)
            prenotazioni_per_campo[campo.get_nome_campo()] = prenotazioni_effetuate

        return prenotazioni_per_campo

    @classmethod
    def controlla_scadenza_prenotazioni(cls):
        campi = Gestore_campo.get_campi()
        for campo in campi:
            prenotazioni = cls.get_prenotazioni_campo(campo)
            for prenotazione in prenotazioni:
                if datetime.datetime.now() > prenotazione.get_data_attività():
                    prenotazione.attiva = False
                    Ricevuta.crea(datetime.datetime.now(), campo.get_prezzo(), prenotazione)

            cls.set_prenotazioni_campo(campo, prenotazioni)

    @classmethod
    def get_prenotazioni_campo(cls, campo):
        Controller_path.genera_path(campo.path_prenotazioni)

        if os.path.getsize(campo.path_prenotazioni) != 0:
            with open(campo.path_prenotazioni, "rb") as f:
                return pickle.load(f)
        return []

    @classmethod
    def set_prenotazioni_campo(cls, campo, prenotazioni):
        Controller_path.genera_path(campo.path_prenotazioni)

        with open(campo.path_prenotazioni, "wb") as f:
            pickle.dump(prenotazioni, f, pickle.HIGHEST_PROTOCOL)

    @classmethod
    def is_data_passata(cls, data_attività):
        if datetime.datetime.now().strftime("%x") > data_attività.strftime("%x"):
            raise ExceptionDataPassata("Non puoi prenotare nessuna attività in questa giornata")

    @classmethod
    def is_data_festiva(cls, data_attività):
        if data_attività.weekday() == 6:
            raise ExceptionGiornoFestivo("Il centro sportivo è chiuso")

    @classmethod
    def is_ora_passata(cls, data_attività):
        if datetime.datetime.now().strftime("%H") > data_attività.strftime("%H") and datetime.datetime.now().strftime(
                "%x").__eq__(data_attività.strftime("%x")):
            raise ExceptionOra()

    @classmethod
    def is_modificabile(cls, data_attività):
        if data_attività.day == datetime.datetime.now().day and int(data_attività.strftime("%H")) - int(datetime.datetime.now().strftime("%H")) <= 5:
            raise ExceptionPreotazioneNonModificabile("La prenotazione non può essere modificata")

    @classmethod
    def imposta_partecipanti(cls, campo, data):
        try:
            prenotazione = cls.cerca_prenotazione(campo, data)
            return prenotazione.get_partecipanti()
        except ExceptionPrenotazioneInesistente:
            return []