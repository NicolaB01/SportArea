import shutil
import unittest
import datetime

from Attivita.Campo import Campo
from Attivita.Cliente import Cliente
from Attivita.Prenotazione import Prenotazione
from Attivita.Ricevuta import Ricevuta
from Gestore.Gestore_campo import Gestore_campo
from Gestore.Gestore_cliente import Gestore_cliente
from Gestore.Gestore_prenotazione import Gestore_prenotazione
from Gestore.Gestore_statistiche import Gestore_statistiche
from Path.Path_database import PATH_DATI


class Test_statistiche(unittest.TestCase):
    def test_statistiche_fatturato(self):
        Campo.crea_campo("messi", 22, 50, "calcio")
        campo = Gestore_campo.cerca_campo("messi")
        Cliente.crea_cliente("nicola", "biagioli", "BBBBBBBBB", "nico@", "29/10/2001", 3334445556, "pwd123")
        Gestore_cliente.login_account("nico@", "pwd123")
        Prenotazione.crea_prenotazione(campo, datetime.datetime(2023, 4, 15, 18, 00), None)
        prenotazione_1 = Gestore_prenotazione.cerca_prenotazione(campo, datetime.datetime(2023, 4, 15, 18, 00))

        Ricevuta.crea_ricevuta(datetime.datetime(2023, 2, 12, 18, 30), 100, prenotazione_1)
        Ricevuta.crea_ricevuta(datetime.datetime(2023, 2, 12, 18, 30), 60, prenotazione_1)

        Prenotazione.crea_prenotazione(campo, datetime.datetime(2023, 10, 15, 18, 00), None)
        prenotazione_2 = Gestore_prenotazione.cerca_prenotazione(campo, datetime.datetime(2023, 10, 15, 18, 00))

        Ricevuta.crea_ricevuta(datetime.datetime(2023, 3, 12, 19, 30), 200, prenotazione_2)

        self.assertEqual(Gestore_statistiche.stat_bilancio(), {2023: {'Apr': 160,
                                                                        'Oct': 200,
                                                                        'Aug': 0,
                                                                        'Dec': 0,
                                                                        'Feb': 0,
                                                                        'Jan': 0,
                                                                        'Jul': 0,
                                                                        'Jun': 0,
                                                                        'Mar': 0,
                                                                        'May': 0,
                                                                        'Nov': 0,
                                                                        'Sep': 0}})

        self.assertEqual(Gestore_statistiche.guadagno_annuale(2023), 360)
        self.assertEqual(Gestore_statistiche.guadagno_medio_annuale(2023), 30)
        shutil.rmtree(PATH_DATI, ignore_errors=True)

    def test_statistiche_eta(self):
        Cliente.crea_cliente("nicola", "biagioli", "BBBBBBBBB", "nico@", "29/10/2001", 3334445556, "pwd123")
        Cliente.crea_cliente("tommaso", "rossi", "MMMMMMMM", "test@", "19/3/1998", 55566667778, "123pwd")

        self.assertEqual(Gestore_statistiche.get_statistiche_eta(), [21, 24])
        self.assertEqual(Gestore_statistiche.eta_media(), 22.5)
        shutil.rmtree(PATH_DATI, ignore_errors=True)

    def test_statistiche_attivita(self):
        Campo.crea_campo("messi", 22, 50, "calcio")
        campo_1 = Gestore_campo.cerca_campo("messi")
        Cliente.crea_cliente("nicola", "biagioli", "BBBBBBBBB", "nico@", "29/10/2001", 3334445556, "pwd123")
        Gestore_cliente.login_account("nico@", "pwd123")
        Prenotazione.crea_prenotazione(campo_1, datetime.datetime(2023, 4, 15, 18, 00), None)
        prenotazione_1 = Gestore_prenotazione.cerca_prenotazione(campo_1, datetime.datetime(2023, 4, 15, 18, 00))

        Ricevuta.crea_ricevuta(datetime.datetime(2023, 2, 12, 18, 30), 100, prenotazione_1)
        Ricevuta.crea_ricevuta(datetime.datetime(2023, 2, 12, 18, 30), 60, prenotazione_1)

        Campo.crea_campo("ronaldo", 2, 40, "padel")
        campo_2 = Gestore_campo.cerca_campo("ronaldo")
        Prenotazione.crea_prenotazione(campo_2, datetime.datetime(2023, 10, 15, 18, 00), None)
        prenotazione_2 = Gestore_prenotazione.cerca_prenotazione(campo_2, datetime.datetime(2023, 10, 15, 18, 00))

        Ricevuta.crea_ricevuta(datetime.datetime(2023, 3, 12, 19, 30), 200, prenotazione_2)
        self.assertEqual(Gestore_statistiche.stat_attivita(), {2023: {'calcio': 2, 'padel': 1}})
        self.assertEqual(Gestore_statistiche.prenotazioni_totali(), 3)
        self.assertEqual(Gestore_statistiche.prenotazioni_annuali(2023), 3)
        shutil.rmtree(PATH_DATI, ignore_errors=True)

    def test_statistiche_iscrizioni(self):
        Cliente.crea_cliente("nicola", "biagioli", "BBBBBBBBB", "nico@", "29/10/2001", 3334445556, "pwd123")
        Cliente.crea_cliente("tommaso", "rossi", "MMMMMMMM", "test@", "19/3/1998", 55566667778, "123pwd")

        self.assertEqual(Gestore_statistiche.stat_iscrizioni(), {2023: {'Apr': 0,
                                                                        'Oct': 0,
                                                                        'Aug': 0,
                                                                        'Dec': 0,
                                                                        'Feb': 0,
                                                                        'Jan': 0,
                                                                        'Jul': 0,
                                                                        'Jun': 0,
                                                                        'Mar': 2,
                                                                        'May': 0,
                                                                        'Nov': 0,
                                                                        'Sep': 0}})
        self.assertEqual(Gestore_statistiche.iscrizioni_annuali(2023), 2)
        self.assertEqual(Gestore_statistiche.iscrizioni_medie_annuali(2023), 2/12)
        shutil.rmtree(PATH_DATI, ignore_errors=True)
