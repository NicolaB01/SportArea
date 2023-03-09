import datetime
import unittest

from Attivita.Campo import Campo
from Attivita.Cliente import Cliente
from Attivita.Prenotazione import Prenotazione
from Attivita.Ricevuta import Ricevuta


class Test(unittest.TestCase):

    def test_registra_cliente(self):
        cliente = Cliente("nicola", "biagioli", "BBBBBBBBB", "nico@", "29/10/2001", 3334445556, "pwd123")
        self.assertEqual(cliente.email, "nico@")
        self.assertEqual(cliente.saldo, 0)

    def test_creazione_prenotazione(self):
        cliente = Cliente("nicola", "biagioli", "BBBBBBBBB", "nico@", "29/10/2001", 3334445556, "pwd123")
        prenotazione = Prenotazione(cliente, datetime.datetime(2023,1,12,14), "Messi", ["Luca", "Giovanni"])

        self.assertEqual(prenotazione.data_attività, datetime.datetime(2023,1,12,14))
        self.assertEqual(prenotazione.partecipanti[0], "Luca")

    def test_creazione_campo(self):
        campo = Campo("Messi", 24, 96, "Calcio")

        self.assertEqual(campo.attività, "Calcio")
        self.assertEqual(campo.numero_max_partecipanti, 24)

    def test_creazione_ricevuta(self):
        cliente = Cliente("nicola", "biagioli", "BBBBBBBBB", "nico@", "29/10/2001", 3334445556, "pwd123")
        prenotazione = Prenotazione(cliente, datetime.datetime(2023,1,12,14), "Messi", None)
        ricevuta = Ricevuta(datetime.datetime.now(), 75, prenotazione)

        self.assertEqual(ricevuta.prezzo, 75)



