import datetime
import random
import pickle
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from Gestore.Eccezioni import ExceptionEmailSconosciuta, ExceptionPassword, ExceptionCodiceRecupero, \
    ExceptionEmailFormat, ExceptionAmicizia, ExceptionSaldoInsufficente
from Path.Path_database import *


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
        self.data_iscrizione = datetime.datetime.now().strftime("%x")
        self.amici_attivi = []
        self.amici_attesa = []

    def __str__(self):
        return f"Nome:\t\t{self.nome}" \
               f"\nCognome:\t{self.cognome}" \
               f"\nEmail:\t\t{self.email}" \
               f"\nCodice fiscale:\t{self.codice_fiscale}" \
               f"\nTelefono:\t{self.numero_telefono}" \
               f"\nData di nascita:\t{self.data_nascita}" \
               f"\nData di iscrizione:\t{self.data_iscrizione}"

    def __eq__(self, other):
        return isinstance(other,
                          Cliente) and self.nome == other.nome and self.cognome == other.cognome and self.email == other.email and self.pwd == other.pwd and self.data_iscrizione == other.data_iscrizione and self.codice_fiscale == other.codice_fiscale and self.data_nascita == other.data_nascita

    @classmethod
    def registra_account(cls, nome, cognome, codice, email, nascita, tel, pwd):
        clienti = cls.get_clienti()
        try:
            cls.cerca_account(email)

        except ExceptionEmailSconosciuta:
            nuovo_cliente = Cliente(nome, cognome, codice, email, nascita, tel, pwd)
            clienti.append(nuovo_cliente)
            cls.set_clienti(clienti)

    @classmethod
    def login_account(cls, email, pwd):
        account = Cliente.cerca_account(email)
        if account.pwd != pwd:
            raise ExceptionPassword("La password non è corretta")

        cls.set_cliente_connesso(account)

    def modifica_account(self, nuovo_nome, nuovo_cognome, nuovo_cf, nuovo_telefono, nuova_password, nuova_data_nascita):
        clienti = self.get_clienti()
        indice = clienti.index(self)

        self.nome = nuovo_nome
        self.cognome = nuovo_cognome
        self.codice_fiscale = nuovo_cf
        self.numero_telefono = nuovo_telefono
        self.pwd = nuova_password
        self.data_nascita = nuova_data_nascita

        clienti[indice] = self

        self.set_clienti(clienti)
        self.set_cliente_connesso(self)

    def salva_modifiche_account(self):
        clienti = self.get_clienti()
        indice = clienti.index(self)
        clienti[indice] = self

        self.set_clienti(clienti)

        if self.get_account_connesso() == self:
            self.set_cliente_connesso(self)

    def richiesta_amicizia(self, email):
        nuovo_amico = self.cerca_account(email)

        if nuovo_amico == self:
            raise ExceptionEmailFormat("Non puoi mandare l'amicizia a te stesso")

        if self in nuovo_amico.amici_attesa or nuovo_amico in self.amici_attivi:
            raise ExceptionAmicizia(f"{nuovo_amico} è già presente nella tua lista di amici")

        nuovo_amico.amici_attesa.append(self)
        nuovo_amico.salva_modifiche_account()

    def accetta_amicizia(self, email):
        nuovo_amico = self.cerca_account(email)
        self.amici_attesa.remove(nuovo_amico)
        self.amici_attivi.append(nuovo_amico)

        nuovo_amico.amici_attivi.append(self)

        self.salva_modifiche_account()
        nuovo_amico.salva_modifiche_account()

    def rifiuta_amicizia(self, email):
        self.amici_attesa.remove(self.cerca_account(email))

        self.salva_modifiche_account()

    def rimuovi_amicizia(self, email):
        amico = self.cerca_account(email)
        self.amici_attivi.remove(amico)
        amico.amici_attivi.remove(self)

        self.salva_modifiche_account()
        amico.salva_modifiche_account()

    def preleva(self, prelievo):
        if prelievo > self.saldo:
            raise ExceptionSaldoInsufficente("Il tuo saldo è insufficente")

        self.saldo -= prelievo
        self.salva_modifiche_account()

    def deposito(self, deposito):
        self.saldo += deposito
        self.salva_modifiche_account()

    @classmethod
    def invia_email_recupero_pwd(cls, email):
        cls.codice_di_verifica = " ".join([str(random.randint(0, 999)).zfill(3) for _ in range(2)])

        mittente = "nbiagioli01@gmail.com"
        oggetto = f"Inserisci questo codice: [{Cliente.codice_di_verifica}] per poter reimpostare la password"

        msg = MIMEMultipart()
        msg['From'] = mittente
        msg['To'] = email
        msg['Subject'] = "Recupero password"
        msg.attach(MIMEText(oggetto))

        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(mittente, "nxnbnjutflbvvugv")
            smtp.send_message(msg)

    @classmethod
    def verifica_codice_recupero_password(cls, email, codice_da_verificare, nuova_pwd):
        if cls.codice_di_verifica != codice_da_verificare:
            raise ExceptionCodiceRecupero("Il codice di recupero non coincide")

        cliente = cls.cerca_account(email)
        cliente.pwd = nuova_pwd

        cliente.salva_modifiche_account()

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

    @classmethod
    def set_clienti(cls, clienti):
        with open(PATH_INFO_CLIENTI, "wb") as f:
            pickle.dump(clienti, f, pickle.HIGHEST_PROTOCOL)

    @classmethod
    def set_cliente_connesso(cls, cliente):
        with open(PATH_ACCOUNT_CONNESSO, "wb") as f:
            pickle.dump(cliente, f, pickle.HIGHEST_PROTOCOL)