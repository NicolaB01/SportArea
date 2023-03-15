import shutil
import unittest

from Attivita.Campo import Campo
from Gestore.Gestore_campo import Gestore_campo
from Path.Path_database import PATH_DATI
from Utils.Eccezioni import ExceptionNomeCampoUtilizzato, ExceptionCampoInesistente


class Test_campo(unittest.TestCase):
    def test_crea_campo(self):
        Campo.crea_campo("messi", 22, 50, "calcio")
        self.assertEqual(Gestore_campo.cerca_campo("messi").get_nome_campo(), "messi")
        self.assertEqual(Gestore_campo.cerca_campo("messi").get_prezzo(), 50)

        with self.assertRaises(ExceptionNomeCampoUtilizzato):
            Campo.crea_campo("messi", 100, 30, "padel")

        shutil.rmtree(PATH_DATI, ignore_errors=True)

    def test_cerca_campo(self):
        Campo.crea_campo("messi", 22, 50, "calcio")
        self.assertEqual(Gestore_campo.cerca_campo("messi").get_nome_campo(), "messi")
        self.assertEqual(Gestore_campo.cerca_campo("messi").get_prezzo(), 50)

        with self.assertRaises(ExceptionCampoInesistente):
            Gestore_campo.cerca_campo("ronaldo")

        shutil.rmtree(PATH_DATI, ignore_errors=True)

    def test_elimina_campo(self):
        Campo.crea_campo("messi", 22, 50, "calcio")
        Gestore_campo.cerca_campo("messi").elimina_campo()
        numero_campi = len(Gestore_campo.get_campi())
        self.assertEqual(numero_campi, 0)

        shutil.rmtree(PATH_DATI, ignore_errors=True)

