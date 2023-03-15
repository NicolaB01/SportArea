import shutil
import unittest

from Attivita.Cliente import Cliente
from Gestore.Gestore_cliente import Gestore_cliente
from Path.Path_database import PATH_DATI
from Utils.Eccezioni import ExceptionEmailSconosciuta, ExceptionPassword, ExceptionEmailUtilizzata, \
    ExceptionSaldoInsufficente


class Test_cliente(unittest.TestCase):
    def test_registra_cliente(self):
        Cliente.crea_cliente("nicola", "biagioli", "BBBBBBBBB", "nico@", "29/10/2001", 3334445556, "pwd123")
        self.assertEqual(Gestore_cliente.cerca_account("nico@").get_nome(), "nicola")
        self.assertEqual(Gestore_cliente.cerca_account("nico@").get_saldo(), 0)

        with self.assertRaises(ExceptionEmailUtilizzata):
            Cliente.crea_cliente("tommaso", "rossi", "MMMMMMMM", "nico@", "30/10/2008", 545654654, "123pwd")

        shutil.rmtree(PATH_DATI, ignore_errors=True)

    def test_login_account(self):
        Cliente.crea_cliente("nicola", "biagioli", "BBBBBBBBB", "nico@", "29/10/2001", 3334445556, "pwd123")
        Gestore_cliente.login_account("nico@", "pwd123")
        self.assertEqual(Gestore_cliente.get_account_connesso().get_nome(), "nicola")
        self.assertEqual(Gestore_cliente.get_account_connesso().get_CF(), "BBBBBBBBB")

        with self.assertRaises(ExceptionPassword):
            Gestore_cliente.login_account("nico@", "123")

        with self.assertRaises(ExceptionEmailSconosciuta):
            Gestore_cliente.login_account("test@", "pwd123")

        shutil.rmtree(PATH_DATI, ignore_errors=True)

    def test_cerca_account(self):
        Cliente.crea_cliente("nicola", "biagioli", "BBBBBBBBB", "nico@", "29/10/2001", 3334445556, "pwd123")
        self.assertEqual(Gestore_cliente.cerca_account("nico@").get_nome(), "nicola")

        with self.assertRaises(ExceptionEmailSconosciuta):
            Gestore_cliente.cerca_account("test@")

        shutil.rmtree(PATH_DATI, ignore_errors=True)

    def test_modifica_account(self):
        Cliente.crea_cliente("nicola", "biagioli", "BBBBBBBBB", "nico@", "29/10/2001", 3334445556, "pwd123")
        Gestore_cliente.login_account("nico@", "pwd123")
        Cliente.modifica_account("tommaso", "rossi", "BBBBBBBBB", 3334445556, "pwd123", "10/12/2000")
        self.assertEqual(Gestore_cliente.cerca_account("nico@").get_nome(), "tommaso")
        self.assertEqual(Gestore_cliente.cerca_account("nico@").get_saldo(), 0)
        shutil.rmtree(PATH_DATI, ignore_errors=True)

    def test_preleva(self):
        Cliente.crea_cliente("nicola", "biagioli", "BBBBBBBBB", "nico@", "29/10/2001", 3334445556, "pwd123")
        Gestore_cliente.login_account("nico@", "pwd123")
        cliente = Gestore_cliente.cerca_account("nico@")
        cliente.deposito(2000)
        cliente.preleva(1200)
        self.assertEqual(Gestore_cliente.cerca_account("nico@").get_saldo(), 800)

        with self.assertRaises(ExceptionSaldoInsufficente):
            Gestore_cliente.cerca_account("nico@").preleva(1000)

        shutil.rmtree(PATH_DATI, ignore_errors=True)

    def test_deposita(self):
        Cliente.crea_cliente("nicola", "biagioli", "BBBBBBBBB", "nico@", "29/10/2001", 3334445556, "pwd123")
        Gestore_cliente.login_account("nico@", "pwd123")
        cliente = Gestore_cliente.cerca_account("nico@")
        cliente.deposito(2000)
        self.assertEqual(Gestore_cliente.cerca_account("nico@").get_saldo(), 2000)
        shutil.rmtree(PATH_DATI, ignore_errors=True)

    def test_eta_cliente(self):
        Cliente.crea_cliente("nicola", "biagioli", "BBBBBBBBB", "nico@", "29/10/2001", 3334445556, "pwd123")
        self.assertEqual(Gestore_cliente.cerca_account("nico@").eta(), 21)
        shutil.rmtree(PATH_DATI, ignore_errors=True)
