from Gestore.Gestore_campo import Gestore_campo
from Gestore.Gestore_cliente import Gestore_cliente
from Gestore.Gestore_prenotazione import Gestore_prenotazione


class Prenotazione:
    def __init__(self, cliente, data_attivita, nome_campo, partecipanti):
        self.cliente = cliente
        self.data_attivita = data_attivita
        self.nome_campo = nome_campo
        self.partecipanti = partecipanti
        self.attiva = True

    def __str__(self):
        return f"Cliente:\t\t{self.cliente.nome}" \
               f"\nData attivita:\t{self.data_attivita}" \
               f"\nCampo:\t\t{self.nome_campo}" \
               f"\nPartecipanti:\t{self.partecipanti} "

    def __eq__(self, other):
        return isinstance(other, Prenotazione) and \
               self.cliente == other.cliente and \
               self.data_attivita == other.data_attivita and \
               self.nome_campo == other.nome_campo

    #Questo metodo crea una prenotazione con i parametri passati
    @classmethod
    def crea_prenotazione(cls, campo, data_attivita, partecipanti):
        prenotazioni = Gestore_prenotazione.get_prenotazioni_campo(campo)
        nuova_prenotazione = Prenotazione(Gestore_cliente.get_account_connesso(), data_attivita, campo.nome, partecipanti)
        prenotazioni.append(nuova_prenotazione)

        Gestore_prenotazione.set_prenotazioni_campo(campo, prenotazioni)

    #Questo metodo elimina la prenotazione passata
    def elimina_prenotazione(self):
        campo = Gestore_campo.cerca_campo(self.get_nome_campo())
        prenotazioni = Gestore_prenotazione.get_prenotazioni_campo(campo)
        prenotazioni.remove(self)

        Gestore_prenotazione.set_prenotazioni_campo(campo, prenotazioni)

    #Questo metodo salava la prenotazione nel file
    def salva_prenotazione(self):
        campo = Gestore_campo.cerca_campo(self.get_nome_campo())
        prenotazioni = Gestore_prenotazione.get_prenotazioni_campo(campo)
        prenotazioni[prenotazioni.index(self)] = self

        Gestore_prenotazione.set_prenotazioni_campo(campo, prenotazioni)

    def get_cliente(self):
        return self.cliente

    def set_cliente(self, cliente):
        self.cliente = cliente

    def get_data_attivita(self):
        return self.data_attivita

    def set_data_attivita(self, data_attivita):
        self.data_attivita = data_attivita

    def get_nome_campo(self):
        return self.nome_campo

    def set_nome_campo(self, nome_campo):
        self.nome_campo = nome_campo

    def get_partecipanti(self):
        return self.partecipanti

    def set_partecipanti(self, partecipanti):
        self.partecipanti = partecipanti
