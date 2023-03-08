import datetime
import os
import pickle

from Gestore.Eccezioni import ExceptionEmailSconosciuta, ExceptionPassword, ExceptionSaldoInsufficente, \
    ExceptionEmailUtilizzata
from Path.Path_database import PATH_INFO_CLIENTI, PATH_ACCOUNT_CONNESSO


class Cliente:
    def __init__(self, nome, cognome, codice_fiscale, email, data_nascita, numero_telefono, pwd):
        self.nome = nome
        self.cognome = cognome
        self.codice_fiscale = codice_fiscale
        self.email = email
        self.data_nascita = data_nascita
        self.numero_telefono = numero_telefono
        self.pwd = pwd
        self.saldo = 0.0
        self.data_iscrizione = datetime.datetime.now()
        self.amici_attivi = []
        self.amici_attesa = []

    def __str__(self):
        return f"Nome:\t\t{self.nome}" \
               f"\nCognome:\t{self.cognome}" \
               f"\nEmail:\t\t{self.email}" \
               f"\nCodice fiscale:\t{self.codice_fiscale}" \
               f"\nTelefono:\t{self.numero_telefono}" \
               f"\nData di nascita:\t{self.data_nascita}" \
               f"\nData di iscrizione:\t{self.data_iscrizione.day}/{self.data_iscrizione.month}/{self.data_iscrizione.year}"

    def __eq__(self, other):
        return isinstance(other,
                          Cliente) and self.email == other.email

    @classmethod
    def crea(cls, nome, cognome, CF, email, data_nascita, telefono, pwd):
        try:
            Cliente.cerca_account(email)
            raise ExceptionEmailUtilizzata("Email già in uso")
        except ExceptionEmailSconosciuta:
            clienti = Cliente.get_clienti()
            nuovo_cliente = Cliente(nome, cognome, CF, email, data_nascita, telefono, pwd)
            clienti.append(nuovo_cliente)
            Cliente.set_clienti(clienti)

    @classmethod
    def login_account(cls, email, pwd):
        account = Cliente.cerca_account(email)
        if account.pwd != pwd:
            raise ExceptionPassword("La password non è corretta")

        cls.set_cliente_connesso(account)

    @classmethod
    def modifica_account(cls, nuovo_nome, nuovo_cognome, nuovo_cf, nuovo_telefono, nuova_password, nuova_data_nascita):
        clienti = cls.get_clienti()
        account_connesso = cls.get_account_connesso()
        indice = clienti.index(account_connesso)

        account_connesso.nome = nuovo_nome
        account_connesso.cognome = nuovo_cognome
        account_connesso.codice_fiscale = nuovo_cf
        account_connesso.numero_telefono = nuovo_telefono
        account_connesso.pwd = nuova_password
        account_connesso.data_nascita = nuova_data_nascita

        clienti[indice] = account_connesso

        account_connesso.salva_modifiche_account()

    def salva_modifiche_account(self):
        clienti = self.get_clienti()
        indice = clienti.index(self)
        clienti[indice] = self

        self.set_clienti(clienti)

        if self.get_account_connesso() == self:
            self.set_cliente_connesso(self)

    def get_saldo(self):
        return self.saldo

    def preleva(self, prelievo):
        if prelievo > self.saldo:
            raise ExceptionSaldoInsufficente("Il tuo saldo è insufficente")

        self.saldo -= prelievo
        self.salva_modifiche_account()

    def deposito(self, deposito):
        self.saldo += deposito
        self.salva_modifiche_account()

    @classmethod
    def cerca_account(cls, email):
        clienti = cls.get_clienti()
        for cliente in clienti:
            if cliente.email == email:
                return cliente

        raise ExceptionEmailSconosciuta("Non ci sono account con questa email")

    @classmethod
    def get_clienti(cls):
        if os.path.getsize(PATH_INFO_CLIENTI) != 0:
            with open(PATH_INFO_CLIENTI, "rb") as f:
                return pickle.load(f)
        return []

    @classmethod
    def get_account_connesso(cls):
        with open(PATH_ACCOUNT_CONNESSO, "rb") as f:
            return pickle.load(f)

    def età(self):
        oggi = datetime.datetime.now()
        giorno, mese, anno = self.data_nascita.split('/')
        data_nascita = datetime.datetime(int(anno), int(mese), int(giorno))
        return oggi.year - data_nascita.year - ((oggi.month, oggi.day) < (data_nascita.month, data_nascita.day))

    @classmethod
    def set_clienti(cls, clienti):
        with open(PATH_INFO_CLIENTI, "wb") as f:
            pickle.dump(clienti, f, pickle.HIGHEST_PROTOCOL)

    @classmethod
    def set_cliente_connesso(cls, cliente):
        with open(PATH_ACCOUNT_CONNESSO, "wb") as f:
            pickle.dump(cliente, f, pickle.HIGHEST_PROTOCOL)

    def get_amici_attivi(self):
        return self.amici_attivi

    def get_amici_attesa(self):
        return self.amici_attesa