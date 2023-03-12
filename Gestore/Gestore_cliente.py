import os
import pickle
import re

from Gestore.Gestore_email import Gestore_email
from Utils.Controller_path import Controller_path
from Utils.Eccezioni import ExceptionNomeFormat, ExceptionCognomeFormat, ExceptionCFFormat, ExceptionEmailFormat, \
    ExceptionDataNascitaFormat, ExceptionTelefonoFormat, ExceptionPassword, \
    ExceptionEmailSconosciuta, ExceptionCodiceRecupero
from Path.Path_database import PATH_INFO_CLIENTI, PATH_ACCOUNT_CONNESSO


class Gestore_cliente:
    #Questo metodo permette di effettuare il login in base ai parametri, se connesso correttamente i dati vengono salvati su un file apposito
    @classmethod
    def login_account(cls, email, pwd):
        account = cls.cerca_account(email)
        if account.get_pwd() != pwd:
            raise ExceptionPassword("La password non è corretta")

        cls.set_account_connesso(account)

    #Questo metodo permette la ricerca di uno specifico cliente attraverso la sua email
    @classmethod
    def cerca_account(cls, email):
        clienti = cls.get_clienti()
        for cliente in clienti:
            if cliente.get_email() == email:
                return cliente

        raise ExceptionEmailSconosciuta("Non ci sono account con questa email")

    #Questo metodo salva il cliente passato in un apposito file
    @classmethod
    def salva_modifiche_account(cls, account):
        clienti = cls.get_clienti()
        indice = clienti.index(account)
        clienti[indice] = account

        cls.set_clienti(clienti)

        if cls.get_account_connesso().__eq__(account):
            cls.set_account_connesso(account)

    #Questo metodo ridà la lista di tutti i clienti salavati
    @classmethod
    def get_clienti(cls):
        Controller_path.genera_path(PATH_INFO_CLIENTI)

        if os.path.getsize(PATH_INFO_CLIENTI) != 0:
            with open(PATH_INFO_CLIENTI, "rb") as f:
                return pickle.load(f)
        return []

    #Questo metodo permette di salvare dei clienti su un apposito file
    @classmethod
    def set_clienti(cls, clienti):
        Controller_path.genera_path(PATH_INFO_CLIENTI)

        with open(PATH_INFO_CLIENTI, "wb") as f:
            pickle.dump(clienti, f, pickle.HIGHEST_PROTOCOL)

    #Questo metodo ridà l'account dell'ultimo cliente che ha effettuato il login
    @classmethod
    def get_account_connesso(cls):
        Controller_path.genera_path(PATH_ACCOUNT_CONNESSO)

        with open(PATH_ACCOUNT_CONNESSO, "rb") as f:
            return pickle.load(f)

    #Questo metodo permette il salvataggio dell'account connesso in un fil apposito
    @classmethod
    def set_account_connesso(cls, cliente):
        Controller_path.genera_path(PATH_ACCOUNT_CONNESSO)

        with open(PATH_ACCOUNT_CONNESSO, "wb") as f:
            pickle.dump(cliente, f, pickle.HIGHEST_PROTOCOL)

    #Questo metodo controlla che il nome passato sia almeno di 3 caratteri
    @classmethod
    def check_nome(cls, nome):
        if len(nome) < 3:
            raise ExceptionNomeFormat("Il nome è troppo corto")

    #Questo metodo controlla che il cognome passato sia almeno di 3 caratteri
    @classmethod
    def check_cognome(cls, cognome):
        if len(cognome) < 3:
            raise ExceptionCognomeFormat("Il cognome è troppo corto")

    #Questo metodo controlla che il codoce fiscale passato sia di 16 caratteri alfanumerici
    @classmethod
    def check_CF(cls, CF):
        if len(CF) != 16 or not CF.isalnum():
            raise ExceptionCFFormat("Codice fiscale errato")

    #Questo metodo controlla che la mail passata contenga il carattere '@'
    @classmethod
    def check_email(cls, email):
        if "@" not in email:
            raise ExceptionEmailFormat("L'email non presenta la @")

    #Questo metodo controlla che la data di nascita passata soddisfi il formato dd/mm/YY
    @classmethod
    def check_data_nascita(cls, data_nascita):
        try:
            if re.match(re.compile("[0-9]{2}/[0-9]{2}/[0-9]{4}"), data_nascita) is None:
                raise ExceptionDataNascitaFormat("La data non rispetta il formato dd/mm/YYYY")

        except ValueError:
            raise ExceptionDataNascitaFormat("La data non rispetta il formato dd/mm/YYYY")

    #Questo metodo controlla che il numero di telefono passato sia di 10 numeri
    @classmethod
    def check_teleono(cls, telefono):
        if len(telefono) != 10 or not telefono.isnumeric():
            raise ExceptionTelefonoFormat("Il numero di telefono non presenta 10 carattero o non sono solo numeri")

    #Questo metodo controlla che la password passata contenga una lettere maiuscola, una minuscola, un carattere speciale e sia di almeno 8 caratteri
    @classmethod
    def check_pwd(cls, pwd, conferma_password=None):
        if pwd != conferma_password and conferma_password is not None:
            raise ExceptionPassword("Le password non coincidono")

        if re.search(re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$"),
                     pwd) is None:
            raise ExceptionPassword(
                "La password deve essere di almeno 8 caratteri, maiuscole, minuscole, numeri e caratteri speciali")

    #Questo metodo controlla che il codice di recupero passato coincida con quello generato dall'applicazione
    @classmethod
    def verifica_dati_recupero_password(cls, email, codice_da_verificare, nuova_pwd, conferma_nuova_pwd):
        if Gestore_email.codice_di_verifica != codice_da_verificare:
            raise ExceptionCodiceRecupero("Il codice di recupero non coincide")

        Gestore_cliente.check_pwd(nuova_pwd, conferma_nuova_pwd)

        cliente = Gestore_cliente.cerca_account(email)
        cliente.pwd = nuova_pwd

        Gestore_cliente.salva_modifiche_account(cliente)