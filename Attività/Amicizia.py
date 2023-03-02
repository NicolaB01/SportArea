from Attività.Cliente import Cliente
from Gestore.Eccezioni import ExceptionAmicizia


class Amicizia:
    def __init__(self, email_amico):
        self.amico = Cliente.cerca_account(email_amico)
        self.account_connesso = Cliente.get_account_connesso()

    def richiesta_amicizia(self):
        if self.amico.__eq__(self.account_connesso):
            raise ExceptionAmicizia("Non puoi mandare l'amicizia a te stesso")
        if self.account_connesso in self.amico.amici_attivi and self.amico in self.account_connesso.amici_attivi:
            raise ExceptionAmicizia(f"{self.amico.nome} {self.amico.cognome} è già presente nella tua lista di amici")
        if self.account_connesso in self.amico.amici_attesa:
            raise ExceptionAmicizia(f"Richiesta di amicizia già effettuata")
        if self.amico in self.account_connesso.amici_attesa:
            raise ExceptionAmicizia(f"{self.amico.nome} {self.amico.cognome} è già presente nella tua lista di amici in attesa")

        self.amico.amici_attesa.append(self.account_connesso)
        self.amico.salva_modifiche_account()

    def accetta_amicizia(self):
        self.account_connesso.amici_attesa.remove(self.amico)
        self.account_connesso.amici_attivi.append(self.amico)

        self.amico.amici_attivi.append(self.account_connesso)

        self.account_connesso.salva_modifiche_account()
        self.amico.salva_modifiche_account()

    def rifiuta_amicizia(self):
        self.account_connesso.amici_attesa.remove(self.amico)

        self.account_connesso.salva_modifiche_account()

    def rimuovi_amicizia(self):
        self.account_connesso.amici_attivi.remove(self.amico)
        self.amico.amici_attivi.remove(self.account_connesso)

        self.account_connesso.salva_modifiche_account()
        self.amico.salva_modifiche_account()