import os
import pickle
import re

from Utils.Eccezioni import ExceptionNomeFormat, ExceptionCognomeFormat, ExceptionCFFormat, ExceptionEmailFormat, \
    ExceptionDataNascitaFormat, ExceptionTelefonoFormat, ExceptionPassword, \
    ExceptionEmailSconosciuta
from Path.Path_database import PATH_INFO_CLIENTI, PATH_ACCOUNT_CONNESSO


class Gestore_cliente:
    @classmethod
    def login_account(cls, email, pwd):
        account = cls.cerca_account(email)
        if account.get_pwd() != pwd:
            raise ExceptionPassword("La password non è corretta")

        cls.set_cliente_connesso(account)

    @classmethod
    def cerca_account(cls, email):
        clienti = cls.get_clienti()
        for cliente in clienti:
            if cliente.get_email() == email:
                return cliente

        raise ExceptionEmailSconosciuta("Non ci sono account con questa email")

    @classmethod
    def salva_modifiche_account(cls, account):
        clienti = cls.get_clienti()
        indice = clienti.index(account)
        clienti[indice] = account

        cls.set_clienti(clienti)

        if cls.get_account_connesso().__eq__(account):
            cls.set_cliente_connesso(account)

    @classmethod
    def get_clienti(cls):
        if os.path.getsize(PATH_INFO_CLIENTI) != 0:
            with open(PATH_INFO_CLIENTI, "rb") as f:
                return pickle.load(f)
        return []

    @classmethod
    def set_clienti(cls, clienti):
        with open(PATH_INFO_CLIENTI, "wb") as f:
            pickle.dump(clienti, f, pickle.HIGHEST_PROTOCOL)

    @classmethod
    def get_account_connesso(cls):
        with open(PATH_ACCOUNT_CONNESSO, "rb") as f:
            return pickle.load(f)

    @classmethod
    def set_cliente_connesso(cls, cliente):
        with open(PATH_ACCOUNT_CONNESSO, "wb") as f:
            pickle.dump(cliente, f, pickle.HIGHEST_PROTOCOL)

    @classmethod
    def check_nome(cls, nome):
        if len(nome) < 3:
            raise ExceptionNomeFormat("Il nome è troppo corto")

    @classmethod
    def check_congome(cls, cognome):
        if len(cognome) < 3:
            raise ExceptionCognomeFormat("Il cognome è troppo corto")

    @classmethod
    def check_CF(cls, CF):
        if len(CF) != 16 or not CF.isalnum():
            raise ExceptionCFFormat("Codice fiscale errato")

    @classmethod
    def check_email(cls, email):
        if "@" not in email:
            raise ExceptionEmailFormat("L'email non presenta la @")

    @classmethod
    def check_data_nascita(cls, data_nascita):
        try:
            if re.match(re.compile("[0-9]{2}/[0-9]{2}/[0-9]{4}"), data_nascita) is None:
                raise ExceptionDataNascitaFormat("La data non rispetta il formato dd/mm/YYYY")

        except ValueError:
            raise ExceptionDataNascitaFormat("La data non rispetta il formato dd/mm/YYYY")

    @classmethod
    def check_teleono(cls, telefono):
        if len(telefono) != 10 or not telefono.isnumeric():
            raise ExceptionTelefonoFormat("Il numero di telefono non presenta 10 carattero o non sono solo numeri")

    @classmethod
    def check_pwd(cls, pwd, conferma_password=None):
        if pwd != conferma_password and conferma_password is not None:
            raise ExceptionPassword("Le password non coincidono")

        if re.search(re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$"),
                     pwd) is None:
            raise ExceptionPassword(
                "La password deve essere di almeno 8 caratteri, maiuscole, minuscole, numeri e caratteri speciali")

