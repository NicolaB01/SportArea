import os.path

from Utils.Controller_path import Controller_path
from Utils.Eccezioni import ExceptionCampoInesistente, ExceptionNomeCampoUtilizzato
from Gestore.Gestore_campo import Gestore_campo


class Campo:
    def __init__(self, nome, numero_max_partecipanti, prezzo, attivita):
        self.nome = nome
        self.numero_max_partecipanti = numero_max_partecipanti
        self.prezzo = prezzo
        self.attivita = attivita
        self.path_prenotazioni = os.path.join("DataBase", "Campi", f"campo_{self.nome}.txt")

    def __str__(self):
        return f"Nome:\t{self.nome}" \
               f"\nNumero partecipanti:{self.numero_max_partecipanti}" \
               f"\nPrezzo:\t{self.prezzo} €" \
               f"\nAttivita:\t{self.attivita}"

    def __eq__(self, other):
        return isinstance(other,
                          Campo) and self.nome == other.nome and self.prezzo == other.prezzo and self.numero_max_partecipanti == other.numero_max_partecipanti and self.attivita == other.attivita


    #Questo metodo permette la creazione di un campo con i parametri passati
    @classmethod
    def crea_campo(cls, nome, numero_max_partecipanti, prezzo, attivita):
        campi = Gestore_campo.get_campi()
        try:
            Gestore_campo.cerca_campo(nome)
            raise ExceptionNomeCampoUtilizzato("Nome campo già presente")
        except ExceptionCampoInesistente:
            nuovo_campo = Campo(nome, numero_max_partecipanti, prezzo, attivita)
            campi.append(nuovo_campo)
            Gestore_campo.set_campi(campi)
            Controller_path.genera_path(nuovo_campo.path_prenotazioni)

    #Questo metodo permette la rimozione di un dato campo
    def elimina_campo(self):
        campi = Gestore_campo.get_campi()
        campi.remove(self)
        os.remove(self.path_prenotazioni)
        Gestore_campo.set_campi(campi)

    def get_nome_campo(self):
        return self.nome

    def set_nome_campo(self, nome):
        self.nome = nome

    def get_numero_max_partecipanti(self):
        return self.numero_max_partecipanti

    def set_numero_max_partecipanti(self, numero_max_partecipanti):
        self.numero_max_partecipanti = numero_max_partecipanti

    def get_prezzo(self):
        return self.prezzo

    def set_prezzp(self, prezzo):
        self.prezzo = prezzo

    def get_attivita(self):
        return self.attivita

    def set_attivita(self, attivita):
        self.attivita = attivita
