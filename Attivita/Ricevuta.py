from Gestore.Gestore_ricevuta import Gestore_ricevuta


class Ricevuta():
    def __init__(self, data_emissione, prezzo, prenotazione):
        self.data_emissione = data_emissione
        self.prezzo = prezzo
        self.prenotazione = prenotazione

    def __str__(self):
        return f"Data_emissione:\t{self.data_emissione.day}/{self.data_emissione.month}/{self.data_emissione.year} {self.data_emissione.strftime('%H')}:{self.data_emissione.strftime('%M')}" \
               f"\nPrezzo:\t\t{self.prezzo}" \
               f"\nCliente:\t\t{self.prenotazione.cliente.nome} {self.prenotazione.cliente.cognome}" \
               f"\nCampo:\t\t{self.prenotazione.nome_campo}" \
               f"\nData attività:\t{self.prenotazione.data_attivita.day}/{self.prenotazione.data_attivita.month}/{self.prenotazione.data_attivita.year} {self.prenotazione.data_attivita.strftime('%H')}:{self.prenotazione.data_attivita.strftime('%M')}"

    def __eq__(self, other):
        return isinstance(other,
                          Ricevuta) and self.prezzo == other.prezzo and self.prenotazione == other.prenotazione

    #Questo metodo crea una ricevuta con i parametri forniti
    @classmethod
    def crea_ricevuta(cls, data_emissione, prezzo, prenotazione):
        ricevuta = Ricevuta(data_emissione, prezzo, prenotazione)
        ricevuta.salva_ricevuta()

    #Questo metodo salva la ricevuta nel file
    def salva_ricevuta(self):
        ricevute = Gestore_ricevuta.get_ricevute()

        if self not in ricevute:
            ricevute.append(self)
            Gestore_ricevuta.set_ricevute(ricevute)

    def get_data_emissione(self):
        return self.data_emissione

    def set_data_emissione(self, data_emissione):
        self.data_emissione = data_emissione

    def get_prezzo(self):
        return self.prezzo

    def set_prezzo(self, prezzo):
        self.prezzo = prezzo

    def get_prenotazione(self):
        return self.prenotazione

    def set_prenotazione(self, prenotazione):
        self.prenotazione = prenotazione
