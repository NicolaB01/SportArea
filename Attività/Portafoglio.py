class Portafoglio:
    def __init__(self):
        self.saldo = 0.0

    def preleva(self, prelievo):
        if prelievo <= self.saldo:
            self.saldo -= prelievo
        else:
            print("il credito è insufficente")

    def deposito(self, deposito):
        self.saldo += deposito