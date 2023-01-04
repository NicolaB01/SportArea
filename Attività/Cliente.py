import os
import shutil
import pickle
from Portafoglio import *


class Cliente:
    PATH_INFO_CLIENTI = os.path.join("../DataBase", "Utenti", "Credenziali.txt")
    PATH_ACCOUNT_CONNESSO = os.path.join("../DataBase", "Utenti", "Account_connesso.txt")

    def __init__(self, nome, cognome, codice_fiscale, email, data_nascita, numero_telefono, pwd):
        self.nome = nome
        self.cognome = cognome
        self.codice_fiscale = codice_fiscale
        self.email = email
        self.data_nascita = data_nascita
        self.numero_telefono = numero_telefono
        self.pwd = pwd
        self.portafoglio = Portafoglio()
        self.amici_attivi = []
        self.amici_attesa = []
        #self.prenotazioni = [] da sistema dopo forse da divide in due liste

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

    #TODO controllo pwd
    @classmethod
    def registra_account(cls, nome, cognome, codice, email, nascita, tel, pwd):
        già_presente = False
        account = []
        if os.path.getsize(Cliente.PATH_INFO_CLIENTI) != 0:
            with open(Cliente.PATH_INFO_CLIENTI, "rb") as f:
                account = pickle.load(f)
                for i in range(len(account)):
                    if account[i].email == email:
                        già_presente = True

        with open(Cliente.PATH_INFO_CLIENTI, "wb") as f:
            if not già_presente:
                nuovo_account = Cliente(nome, cognome, codice, email, nascita, tel, pwd)
                account.append(nuovo_account)

            pickle.dump(account, f, pickle.HIGHEST_PROTOCOL)

    @classmethod
    def login_account(cls, email, pwd):
        if os.path.getsize(Cliente.PATH_INFO_CLIENTI) != 0:
            with open(Cliente.PATH_INFO_CLIENTI, "rb") as f:
                account = pickle.load(f)
                for i in range(len(account)):
                    if account[i].email == email:
                        if account[i].pwd == pwd:
                            print("Connesso correttamente")
                            with open(Cliente.PATH_ACCOUNT_CONNESSO, "wb") as f:
                                pickle.dump(account[i], f, pickle.HIGHEST_PROTOCOL)

    def modifica_account(self, nuovo_nome, nuovo_cognome, nuovo_cf, nuovo_telefono, nuova_password):
        if os.path.getsize(Cliente.PATH_INFO_CLIENTI) != 0:
            self.nome = nuovo_nome
            self.cognome = nuovo_cognome
            self.codice_fiscale = nuovo_cf
            self.numero_telefono = nuovo_telefono
            self.pwd = nuova_password

            with open(Cliente.PATH_INFO_CLIENTI, "rb") as f:
                account = pickle.load(f)
                for i in range(len(account)):
                    if account[i].email == self.email:
                        account[i] = self

            with open(Cliente.PATH_INFO_CLIENTI, "wb") as f:
                pickle.dump(account, f, pickle.HIGHEST_PROTOCOL)

    #TODO cambia in lista
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

    @classmethod
    def get_account_connesso(cls):
        with open(Cliente.PATH_ACCOUNT_CONNESSO, "rb") as f:
            return pickle.load(f)

    #su gestistore
    @classmethod
    def recupera_password(cls, email):
        #controlliamo se la mail è presente, se si mandiamo una mail con un codice
        # 3 tentativi per indpvinare il codice, dopo ti fa tornare al login
        #metti nuova pwd e conferma nuova pwd
        #torni al login
        pass

    #su gestore
    def visualizza_account(self):
        pass


#Cliente.registra_account("nicola", "biagioli", "32434", "nico@", "29102001", 324325325, "cazzi")
#Cliente.registra_account("simone", "diba", "SM244", "diba@", "34325", 2443565346, "1234")
#diba = Cliente.login_account("diba@", "bene")
#diba.modifica_account("tommaso", "mazzarini", "CDff", 344445556, "bene")
#print(diba)


#{email:account, }
#{email:[nome, cognome ...]}
