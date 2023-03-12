import datetime
import shutil
import unittest

from Attivita.Campo import Campo
from Attivita.Cliente import Cliente
from Attivita.Prenotazione import Prenotazione
from Attivita.Ricevuta import Ricevuta
from Gestore.Gestore_campo import Gestore_campo
from Gestore.Gestore_cliente import Gestore_cliente
from Gestore.Gestore_prenotazione import Gestore_prenotazione
from Gestore.Gestore_ricevuta import Gestore_ricevuta
from Path.Path_database import PATH_DATI


class Test_ricevuta(unittest.TestCase):
    def test_crea_ricevuta(self):
        Campo.crea_campo("messi", 22, 50, "calcio")
        campo = Gestore_campo.cerca_campo("messi")
        Cliente.crea_cliente("nicola", "biagioli", "BBBBBBBBB", "nico@", "29/10/2001", 3334445556, "pwd123")
        Gestore_cliente.login_account("nico@", "pwd123")
        Prenotazione.crea_prenotazione(campo, datetime.datetime(2023, 4, 15, 18, 00), None)
        prenotazione = Gestore_prenotazione.cerca_prenotazione(campo, datetime.datetime(2023, 4, 15, 18, 00))

        Ricevuta.crea_ricevuta(datetime.datetime(2023, 2, 12, 18, 30), 100, prenotazione)
        Ricevuta.crea_ricevuta(datetime.datetime(2023, 3, 12, 19, 30), 60, prenotazione)

        numero_ricevute = len(Gestore_ricevuta.get_ricevute())

        self.assertEqual(numero_ricevute, 2)
        shutil.rmtree(PATH_DATI, ignore_errors=True)
