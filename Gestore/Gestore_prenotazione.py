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
    #Questo metodo permette la ricerca di una determinata prenotazione attraverso i parametri passati
    @classmethod
    def cerca_prenotazione(cls, campo, data):
        prenotazioni = cls.get_prenotazioni_campo(campo)
        for prenotazione in prenotazioni:
            if prenotazione.get_data_attivita().__eq__(data):
                return prenotazione

        raise ExceptionPrenotazioneInesistente()

    #Questo metodo ridà un dizionario di campi con le relative fasce orarie disponibile alla prenotazione
    @classmethod
    def get_fasce_orarie_disponibili(cls, attivita, data):
        campi_idonei = cls.campi_idonei_attivita(attivita)

        fasce_orarie_disponibili = {}
        for campo in campi_idonei:
            lista_ore = list(range(data.hour, 22))
            prenotazioni = cls.get_prenotazioni_campo(campo)
            for prenotazione in prenotazioni:
                if prenotazione.get_data_attivita().strftime("%x").__eq__(data.strftime("%x")) and prenotazione.get_data_attivita().hour >= data.hour:
                    lista_ore.remove(prenotazione.get_data_attivita().hour)

            fasce_orarie_disponibili[campo.get_nome_campo()] = lista_ore

        return fasce_orarie_disponibili

    #Questo metodo ridà i campi salvati con la stessa attività passata come parametri
    @classmethod
    def campi_idonei_attivita(cls, attivita):
        campi_idonei = []
        campi = Gestore_campo.get_campi()
        for campo in campi:
            if campo.get_attivita() == attivita:
                campi_idonei.append(campo)

        return campi_idonei

    #Questo metodo ridà la lista delle prenotazioni del cliente connesso
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

            prenotazioni_effetuate.sort(key=lambda x: x.data_attivita)
            prenotazioni_per_campo[campo.get_nome_campo()] = prenotazioni_effetuate

        return prenotazioni_per_campo

    #Questo metodo controlla la scadenza delle prenotazioni effettuate, se questo si verifica allora si genera la ricevuta
    @classmethod
    def controlla_scadenza_prenotazioni(cls):
        campi = Gestore_campo.get_campi()
        for campo in campi:
            prenotazioni = cls.get_prenotazioni_campo(campo)
            for prenotazione in prenotazioni:
                if datetime.datetime.now() > prenotazione.get_data_attivita():
                    prenotazione.attiva = False
                    Ricevuta.crea_ricevuta(datetime.datetime.now(), campo.get_prezzo(), prenotazione)

            cls.set_prenotazioni_campo(campo, prenotazioni)

    #Questo metodo ridà la lista di tutte le prenotazioni effettuate su un campo pssato come parametro
    @classmethod
    def get_prenotazioni_campo(cls, campo):
        Controller_path.genera_path(campo.path_prenotazioni)

        if os.path.getsize(campo.path_prenotazioni) != 0:
            with open(campo.path_prenotazioni, "rb") as f:
                return pickle.load(f)
        return []

    #Questo metodo permette di salvare le prenotazioni di un campo in un apposito file
    @classmethod
    def set_prenotazioni_campo(cls, campo, prenotazioni):
        Controller_path.genera_path(campo.path_prenotazioni)

        with open(campo.path_prenotazioni, "wb") as f:
            pickle.dump(prenotazioni, f, pickle.HIGHEST_PROTOCOL)

    #Questo metodo controlla che la data passata non sia antecedente a quella attuale
    @classmethod
    def is_data_passata(cls, data_attivita):
        if datetime.datetime.now().strftime("%x") > data_attivita.strftime("%x"):
            raise ExceptionDataPassata("Non puoi prenotare nessuna attivitaà in questa giornata")

    #Questo metodo controlla che la data passata non si una data festiva
    @classmethod
    def is_data_festiva(cls, data_attivita):
        if data_attivita.weekday() == 6:
            raise ExceptionGiornoFestivo("Il centro sportivo è chiuso")

    #Questo metodo controlla l'ora passata non sia antecedente all'ora attuale
    @classmethod
    def is_ora_passata(cls, data_attivita):
        if datetime.datetime.now().strftime("%H") > data_attivita.strftime("%H") and datetime.datetime.now().strftime(
                "%x").__eq__(data_attivita.strftime("%x")):
            raise ExceptionOra()

    #Questo metodo controlla che la data non abbia un time delta minore di 5 ore
    @classmethod
    def is_modificabile(cls, data_attivita):
        if data_attivita.day == datetime.datetime.now().day and int(data_attivita.strftime("%H")) - int(datetime.datetime.now().strftime("%H")) <= 5:
            raise ExceptionPreotazioneNonModificabile("La prenotazione non può essere modificata")

    #Questo metodo ridà i partecipanti di una prenotzaione
    @classmethod
    def imposta_partecipanti(cls, campo, data):
        try:
            prenotazione = cls.cerca_prenotazione(campo, data)
            return prenotazione.get_partecipanti()
        except ExceptionPrenotazioneInesistente:
            return []