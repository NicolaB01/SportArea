from Utils.Eccezioni import ExceptionAmicizia
from Gestore.Gestore_cliente import Gestore_cliente


class Gestore_amicizia:
    def __init__(self, email_amico):
        self.amico = Gestore_cliente.cerca_account(email_amico)
        self.account_connesso = Gestore_cliente.get_account_connesso()

    #Questo metodo invia la richiesta di amicizia
    def invia_richiesta_amicizia(self):
        if self.amico.__eq__(self.account_connesso):
            raise ExceptionAmicizia("Non puoi mandare l'amicizia a te stesso")
        if self.account_connesso in self.amico.amici_attivi and self.amico in self.account_connesso.amici_attivi:
            raise ExceptionAmicizia(f"{self.amico.nome} {self.amico.cognome} è già presente nella tua lista di amici")
        if self.account_connesso in self.amico.amici_attesa:
            raise ExceptionAmicizia(f"Richiesta di amicizia già effettuata")
        if self.amico in self.account_connesso.amici_attesa:
            raise ExceptionAmicizia(f"{self.amico.nome} {self.amico.cognome} è già presente nella tua lista di amici in attesa")

        self.aggiungi_amico_attesa(self.amico, self.account_connesso)
        Gestore_cliente.salva_modifiche_account(self.amico)

    #Questo metodo accetta l'amicizia inviata da un altro account
    def accetta_richiesta_amicizia(self):
        self.rimuovi_amico_attesa(self.account_connesso, self.amico)
        self.aggiungi_amico_attivi(self.account_connesso, self.amico)
        self.aggiungi_amico_attivi(self.amico, self.account_connesso)

        Gestore_cliente.salva_modifiche_account(self.account_connesso)
        Gestore_cliente.salva_modifiche_account(self.amico)

    #Questo metodo rifiuta l'amicizia inviata da un altro account
    def rifiuta_richiesta_amicizia(self):
        self.rimuovi_amico_attesa(self.account_connesso, self.amico)

        Gestore_cliente.salva_modifiche_account(self.account_connesso)

    #Questo metodo rimuove un account dalla lista degli amici attivi
    def rimuovi_amicizia(self):
        self.rimuovi_amico_attivi(self.account_connesso, self.amico)
        self.rimuovi_amico_attivi(self.amico, self.account_connesso)

        Gestore_cliente.salva_modifiche_account(self.account_connesso)
        Gestore_cliente.salva_modifiche_account(self.amico)

    def aggiungi_amico_attesa(self, amico_connesso, amico_da_rimuovere):
        amico_connesso.get_amici_attesa().append(amico_da_rimuovere)

    def rimuovi_amico_attesa(self,amico_connesso, amico_da_rimuovere):
        amico_connesso.get_amici_attesa().remove(amico_da_rimuovere)

    def aggiungi_amico_attivi(self, amico_connesso, amico_da_rimuovere):
        amico_connesso.get_amici_attivi().append(amico_da_rimuovere)

    def rimuovi_amico_attivi(self, amico_connesso, amico_da_rimuovere):
        amico_connesso.get_amici_attivi().remove(amico_da_rimuovere)