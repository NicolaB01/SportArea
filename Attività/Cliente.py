import datetime
import os
import random
import pickle
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


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
        self.saldo = 0.0
        self.data_iscrizione = datetime.datetime.now()
        self.amici_attivi = []
        self.amici_attesa = []

    def __str__(self):
        return f"""
        nome                :{self.nome}
        cognome             :{self.cognome}
        codice fiscale      :{self.codice_fiscale}
        email               :{self.email}
        data di nascita     :{self.data_nascita}
        numero di telefono  :{self.numero_telefono}
        password            :{self.pwd}
        saldo               :{self.saldo}
        data di iscrizione  :{self.data_iscrizione}
        """

    def __eq__(self, other):
        return isinstance(other, Cliente) and self.nome == other.nome and self.cognome == other.cognome and self.email == other.email and self.pwd == other.pwd and self.data_iscrizione == other.data_iscrizione and self.codice_fiscale == other.codice_fiscale and self.data_nascita == other.data_nascita


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
                print(type(nuovo_account))

            pickle.dump(account, f, pickle.HIGHEST_PROTOCOL)

    @classmethod
    def login_account(cls, email, pwd):
        account = Cliente.cerca_account(email)
        if account is not None:
            if account.pwd == pwd:
                with open(Cliente.PATH_ACCOUNT_CONNESSO, "wb") as f:
                    pickle.dump(account, f, pickle.HIGHEST_PROTOCOL)
            return True
        return

    def modifica_account(self, nuovo_nome, nuovo_cognome, nuovo_cf, nuovo_telefono, nuova_password):
        if os.path.getsize(Cliente.PATH_INFO_CLIENTI) != 0:
            with open(Cliente.PATH_INFO_CLIENTI, "rb") as f:
                clienti = pickle.load(f)
                print(clienti)
                indice = clienti.index(self)
                self.nome = nuovo_nome
                self.cognome = nuovo_cognome
                self.codice_fiscale = nuovo_cf
                self.numero_telefono = nuovo_telefono
                self.pwd = nuova_password
                clienti[indice] = self

            with open(Cliente.PATH_INFO_CLIENTI, "wb") as f:
                pickle.dump(clienti, f, pickle.HIGHEST_PROTOCOL)

            with open(Cliente.PATH_ACCOUNT_CONNESSO, "wb") as f:
                pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)

    def exit_account(self):
        with open(Cliente.PATH_INFO_CLIENTI, "rb") as f:
            account = pickle.load(f)
            for i in range(len(account)):
                if account[i].email == self.email:
                    account[i] = self

        with open(Cliente.PATH_INFO_CLIENTI, "wb") as f:
            pickle.dump(account, f, pickle.HIGHEST_PROTOCOL)

        with open(Cliente.PATH_ACCOUNT_CONNESSO, "rb+") as f:
            f.truncate()

    @classmethod
    def cerca_account(cls, email):
        if os.path.getsize(Cliente.PATH_INFO_CLIENTI) != 0:
            with open(Cliente.PATH_INFO_CLIENTI, "rb") as f:
                account = pickle.load(f)
                for i in range(len(account)):
                    if account[i].email == email:
                        return account[i]
        return None

    def preleva(self, prelievo):
        if prelievo <= self.saldo:
            self.saldo -= prelievo

            with open(Cliente.PATH_ACCOUNT_CONNESSO, "wb") as f:
                pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
        else:
            # TODO da trasformare in un errore per un messagebox
            print("il credito è insufficente")

    def deposito(self, deposito):
        self.saldo += deposito

        with open(Cliente.PATH_ACCOUNT_CONNESSO, "wb") as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)

    @classmethod
    def get_account_connesso(cls):
        with open(Cliente.PATH_ACCOUNT_CONNESSO, "rb") as f:
            return pickle.load(f)

    # su gestistore
    @classmethod
    def recupera_password(cls, email):
        account_esistente = False
        with open(Cliente.PATH_INFO_CLIENTI, "rb") as f:
            account = pickle.load(f)
            for i in range(len(account)):
                if account[i].email == email:
                    account_esistente = True

        if account_esistente:
            numero_conferma = " ".join([str(random.randint(0, 999)).zfill(3) for _ in range(2)])
            # creiamo la mail da inviare
            mittente = "nbiagioli01@gmail.com"

            oggetto = "Inserisci questo codice: [" + numero_conferma + "] per poter reimpostare la password"

            msg = MIMEMultipart()
            msg['From'] = mittente
            msg['To'] = email
            msg['Subject'] = "Recupero password"
            msg.attach(MIMEText(oggetto))

            with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
                smtp.ehlo()
                smtp.starttls()
                # email del sito tipo sportArea@gmail.com
                smtp.login(mittente, "nxnbnjutflbvvugv")
                smtp.send_message(msg)
                print("Sent...")

            # TODO inserire un QMassegeBox
            print("inserisci il numero di verifica")
            verifica_num = input()

            if numero_conferma == verifica_num:
                print("inserisci la nuova pwd")
                nuova_pwd = input()

                with open(Cliente.PATH_INFO_CLIENTI, "rb") as f:
                    account = pickle.load(f)
                    for i in range(len(account)):
                        if account[i].email == email:
                            account[i].pwd = nuova_pwd
                            print(account[i])

                with open(Cliente.PATH_INFO_CLIENTI, "wb") as f:
                    pickle.dump(account, f, pickle.HIGHEST_PROTOCOL)

        # controlliamo se la mail è presente, se si mandiamo una mail con un codice
        # tre tentativi per indpvinare il codice, dopo ti fa tornare al login
        # metti nuova pwd e conferma nuova pwd
        # torni al login


#Cliente.registra_account("nicola", "biagioli", "32434", "nbiagioli01@gmail.com", "29102001", 324325325, "tua")
#Cliente.registra_account("simone", "diba", "SM244", "diba@", "34325", 2443565346, "1234")

#Cliente.login_account("nbiagioli01@gmail.com", "tua")
#print(Cliente.get_account_connesso())
#Cliente.get_account_connesso().modifica_account("giovanni", "rana", 34325325, 431414, "nuova")
#Cliente.get_account_connesso().exit_account()
