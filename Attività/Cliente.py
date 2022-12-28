import os
import shutil
import pickle
from Portafoglio import *


class Cliente:

    def __init__(self, nome, cognome, codice_fiscale, email, data_nascita, numero_telefono, pwd):
        self.nome = nome
        self.cognome = cognome
        self.codice_fiscale = codice_fiscale
        self.email = email
        self.data_nascita = data_nascita
        self.numero_telefono = numero_telefono
        self.pwd = pwd
        self.portafoglio = Portafoglio()
        self.prenotazioni = []

    def __str__(self):
        return (f"""
        nome                :{self.nome}
        cognome             :{self.cognome}
        codice fiscale      :{self.codice_fiscale}
        email               :{self.email}
        data di nascita     :{self.data_nascita}
        numero di telefono  :{self.numero_telefono}
        password            :{self.pwd}
        saldo               :{self.portafoglio.saldo}
        """)

    @classmethod
    def registra_account(cls, nome, cognome, codice, email, nascita, tel, pwd):
        gia_presente = False
        with open(os.path.join("../DataBase", "Credenziali"), "rb+") as f:
            while True:
                try:
                    if pickle.load(f).email == email:
                        gia_presente = True
                        print("Gia presente")
                except (EOFError, pickle.UnpicklingError):
                    break
            if not gia_presente:
                pickle.dump(Cliente(nome, cognome, codice, email, nascita, tel, pwd), f, pickle.HIGHEST_PROTOCOL)

    @classmethod
    def login_account(cls, email, pwd):
        gia_presente = False
        with open(os.path.join("../DataBase", "Credenziali"), "rb") as f:
            while True:
                try:
                    account = pickle.load(f)
                    if account.email == email:
                        gia_presente = True
                        if account.pwd == pwd:
                            print("Connesso correttamente")
                            return account
                        else:
                            print("password errata")
                except (EOFError, pickle.UnpicklingError):
                    break
            if not gia_presente:
                print("account inesistente")

    def modifica_account(self, nuovo_nome, nuovo_cognome, nuovo_cf, nuovo_telefono, nuova_password):
        self.nome = nuovo_nome
        self.cognome = nuovo_cognome
        self.codice_fiscale = nuovo_cf
        self.numero_telefono = nuovo_telefono
        self.pwd = nuova_password

        with open(os.path.join("../DataBase", "Credenziali"), "rb+") as f:
            with open(os.path.join("../DataBase", "temp"), "wb") as temp:

                while True:
                    try:
                        account = pickle.load(f)
                        if account.email == self.email:
                            pickle.dump(self, temp, pickle.HIGHEST_PROTOCOL)
                        else:
                            pickle.dump(account, temp, pickle.HIGHEST_PROTOCOL)

                    except (EOFError, pickle.UnpicklingError):
                        break

            shutil.copy("./DataBase/temp", "../DataBase/Credenziali")
            os.remove(os.path.join("../DataBase", "temp"))

    def exit_account(self):
        with open(os.path.join("../DataBase", "Credenziali"), "rb+") as f:
            with open(os.path.join("../DataBase", "temp"), "wb") as temp:

                while True:
                    try:
                        account = pickle.load(f)
                        if account.email == self.email:
                            pickle.dump(self, temp, pickle.HIGHEST_PROTOCOL)
                        else:
                            pickle.dump(account, temp, pickle.HIGHEST_PROTOCOL)

                    except (EOFError, pickle.UnpicklingError):
                        break

            shutil.copy("./DataBase/temp", "../DataBase/Credenziali")
            os.remove(os.path.join("../DataBase", "temp"))
