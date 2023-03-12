import datetime
import shutil
import unittest

from Attivita.Campo import Campo
from Attivita.Cliente import Cliente
from Attivita.Prenotazione import Prenotazione
from Gestore.Gestore_campo import Gestore_campo
from Gestore.Gestore_cliente import Gestore_cliente
from Gestore.Gestore_prenotazione import Gestore_prenotazione
from Path.Path_database import PATH_DATI


class Test_prenotazione(unittest.TestCase):
    def test_crea_prenotazione(self):
        Cliente.crea_cliente("nicola", "biagioli", "BBBBBBBBB", "nico@", "29/10/2001", 3334445556, "pwd123")
        Gestore_cliente.login_account("nico@", "pwd123")
        Campo.crea_campo("messi", 22, 50, "calcio")
        campo = Gestore_campo.cerca_campo("messi")
        data = datetime.datetime(2023, 2, 12, 10, 00)

        Prenotazione.crea_prenotazione(campo, data, None)
        self.assertEqual(Gestore_prenotazione.cerca_prenotazione(campo, data).get_nome_campo(), "messi")
        shutil.rmtree(PATH_DATI, ignore_errors=True)

    def test_cerca_prenotazione(self):
        Cliente.crea_cliente("nicola", "biagioli", "BBBBBBBBB", "nico@", "29/10/2001", 3334445556, "pwd123")
        Gestore_cliente.login_account("nico@", "pwd123")
        Campo.crea_campo("messi", 22, 50, "calcio")
        campo = Gestore_campo.cerca_campo("messi")
        data = datetime.datetime(2023, 2, 12, 10, 00)
        Prenotazione.crea_prenotazione(campo, data, None)

        self.assertEqual(Gestore_prenotazione.cerca_prenotazione(campo, data).get_cliente().get_nome(), "nicola")
        shutil.rmtree(PATH_DATI, ignore_errors=True)

    def test_elimina_prenotazione(self):
        Cliente.crea_cliente("nicola", "biagioli", "BBBBBBBBB", "nico@", "29/10/2001", 3334445556, "pwd123")
        Gestore_cliente.login_account("nico@", "pwd123")
        Campo.crea_campo("messi", 22, 50, "calcio")
        campo = Gestore_campo.cerca_campo("messi")
        data = datetime.datetime(2023, 2, 12, 10, 00)
        Prenotazione.crea_prenotazione(campo, data, None)
        prenotazione = Gestore_prenotazione.cerca_prenotazione(campo, data)

        prenotazione.elimina_prenotazione()
        numero_prenotazioni = len(Gestore_prenotazione.get_prenotazioni_campo(campo))

        self.assertEqual(numero_prenotazioni, 0)
        shutil.rmtree(PATH_DATI, ignore_errors=True)

    def test_get_fasce_orarie_disponibili(self):
        Cliente.crea_cliente("nicola", "biagioli", "BBBBBBBBB", "nico@", "29/10/2001", 3334445556, "pwd123")
        Gestore_cliente.login_account("nico@", "pwd123")
        Campo.crea_campo("messi", 22, 50, "calcio")
        campo = Gestore_campo.cerca_campo("messi")
        data = datetime.datetime(2023, 2, 12, 10, 00)
        Prenotazione.crea_prenotazione(campo, data, None)
        data = datetime.datetime(2023, 2, 12, 14, 00)
        Prenotazione.crea_prenotazione(campo, data, None)
        data = datetime.datetime(2023, 2, 12, 15, 00)
        Prenotazione.crea_prenotazione(campo, data, None)

        ora_inizio_filtro = 10
        data = datetime.datetime(2023, 2, 12, ora_inizio_filtro)
        self.assertEqual(Gestore_prenotazione.get_fasce_orarie_disponibili("calcio", data), {"messi":[11,12,13,16,17,18,19,20,21]})
        shutil.rmtree(PATH_DATI, ignore_errors=True)



