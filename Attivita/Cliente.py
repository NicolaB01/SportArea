import datetime

from Utils.Eccezioni import ExceptionEmailUtilizzata, ExceptionEmailSconosciuta, ExceptionSaldoInsufficente
from Gestore.Gestore_cliente import Gestore_cliente


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

    #Questo metodo crea un account con i parametri passati
    @classmethod
    def crea_cliente(cls, nome, cognome, CF, email, data_nascita, telefono, pwd):
        try:
            Gestore_cliente.cerca_account(email)
            raise ExceptionEmailUtilizzata("Email già in uso")
        except ExceptionEmailSconosciuta:
            clienti = Gestore_cliente.get_clienti()
            nuovo_cliente = Cliente(nome, cognome, CF, email, data_nascita, telefono, pwd)
            clienti.append(nuovo_cliente)
            Gestore_cliente.set_clienti(clienti)

    #Questo metodo modifica l'account connesso con i nuovo parametri
    @classmethod
    def modifica_account(cls, nuovo_nome, nuovo_cognome, nuovo_CF, nuovo_telefono, nuova_password, nuova_data_nascita):
        clienti = Gestore_cliente.get_clienti()
        account_connesso = Gestore_cliente.get_account_connesso()
        indice = clienti.index(account_connesso)

        account_connesso.set_nome(nuovo_nome)
        account_connesso.set_cognome(nuovo_cognome)
        account_connesso.set_CF(nuovo_CF)
        account_connesso.set_numero_telefono(nuovo_telefono)
        account_connesso.set_pwd(nuova_password)
        account_connesso.set_data_nascita(nuova_data_nascita)

        clienti[indice] = account_connesso

        Gestore_cliente.salva_modifiche_account(account_connesso)

    #Questo metodo effettua il prelievo di un importo dal saldo del cliente passato
    def preleva(self, prelievo):
        if prelievo > self.get_saldo():
            raise ExceptionSaldoInsufficente("Il tuo saldo è insufficente")

        self.set_saldo(self.get_saldo() - prelievo)
        Gestore_cliente.salva_modifiche_account(self)

    #Questo metodo effettua il deposito di un importo al saldo del cliente passato
    def deposito(self, deposito):
        self.set_saldo(self.get_saldo() + deposito)
        Gestore_cliente.salva_modifiche_account(self)

    #Questo metodo ritorna l'eta del cliente
    def eta(self):
        oggi = datetime.datetime.now()
        giorno, mese, anno = self.data_nascita.split('/')
        data_nascita = datetime.datetime(int(anno), int(mese), int(giorno))
        return oggi.year - data_nascita.year - ((oggi.month, oggi.day) < (data_nascita.month, data_nascita.day))

    def get_nome(self):
        return self.nome

    def set_nome(self, nome):
        self.nome = nome

    def get_cognome(self):
        return self.cognome

    def set_cognome(self, cognome):
        self.cognome = cognome

    def get_CF(self):
        return self.codice_fiscale

    def set_CF(self, CF):
        self.codice_fiscale = CF

    def get_email(self):
        return self.email

    def set_email(self, email):
        self.email = email

    def get_data_nascita(self):
        return self.data_nascita

    def set_data_nascita(self, data_nascita):
        self.data_nascita = data_nascita

    def get_numero_telefono(self):
        return self.numero_telefono

    def set_numero_telefono(self, numero_telefono):
        self.numero_telefono = numero_telefono

    def get_pwd(self):
        return self.pwd

    def set_pwd(self, pwd):
        self.pwd = pwd

    def get_saldo(self):
        return self.saldo

    def set_saldo(self, saldo):
        self.saldo = saldo

    def get_amici_attivi(self):
        return self.amici_attivi

    def set_amici_attivi(self, amici_attivi):
        self.amici_attivi = amici_attivi

    def get_amici_attesa(self):
        return self.amici_attesa

    def set_amici_attesa(self, amici_attesa):
        self.amici_attesa = amici_attesa
