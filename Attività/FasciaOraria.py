import datetime

class Fascia_oraria:
    Fasce_orarie = list(range(8,23))

    def __init__(self, ora_inizio, ora_fine, giorno, mese, anno):
        self.ora_inizio = ora_inizio
        self.ora_fine = ora_fine
        self.data = datetime.datetime(anno, mese, giorno)



