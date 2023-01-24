import calendar

from Attività.Campo import Campo
from Attività.Cliente import Cliente
from Attività.Ricevuta import Ricevuta
from Gestore.Eccezioni import ExceptionAnnoNonPresente


class Statistiche:
    NUMERO_MESI = 12

    @classmethod
    def stat_bilancio(cls):
        ricevute = Ricevuta.get_ricevute()
        entrate_annuali = {}

        mesi = []
        for numero_mese in range(1, 13):
            mesi.append(calendar.month_abbr[numero_mese])

        for ricevuta in ricevute:
            entrate_mensili = {}
            anno_ricevuta = ricevuta.prenotazione.data_attività.year
            mese_ricevuta = ricevuta.prenotazione.data_attività.month

            for mese in mesi:
                entrate_mensili.setdefault(mese, 0)
                entrate_annuali.setdefault(anno_ricevuta, entrate_mensili)

            entrate_annuali[anno_ricevuta][calendar.month_abbr[mese_ricevuta]] += ricevuta.prezzo

        return entrate_annuali

    @classmethod
    def guadagno_annuale(cls, anno):
        entrate_annuali = cls.stat_bilancio()
        ricavo = 0
        if anno in entrate_annuali.keys():
            for incassi_mensili in entrate_annuali[anno]:
                ricavo += incassi_mensili
            return ricavo
        else:
            raise ExceptionAnnoNonPresente

    @classmethod
    def guadagno_medio_annuale(cls, anno):
        ricavo = cls.guadagno_annuale(anno)
        return ricavo/cls.NUMERO_MESI

    @classmethod
    def stat_anagrafiche(cls):
        clienti = Cliente.get_clienti()
        età_clienti = []
        for cliente in clienti:
            età_clienti.append(cliente.età())

        return età_clienti

    @classmethod
    def età_media(cls):
        età_clienti = cls.stat_anagrafiche()
        età_totale = [x for x in età_clienti]
        numero_clienti = len(Cliente.get_clienti())
        return età_totale/numero_clienti

    @classmethod
    def stat_attività(cls):
        ricevute = Ricevuta.get_ricevute()
        attività = {}
        for ricevuta in ricevute:
            campo = Campo.cerca_campo(ricevuta.prenotazione.nome_campo)
            if campo.attività not in attività:
                attività.setdefault(campo.attività, 1)
            else:
                attività[campo.attività] += 1

        return attività

    @classmethod
    def stat_iscrizioni(cls):
        clienti = Cliente.get_clienti()
        iscrizioni_annuali = {}
        mesi = []
        for numero_mese in range(1, 13):
            mesi.append(calendar.month_abbr[numero_mese])

        for cliente in clienti:
            iscrizioni_mensili = {}
            anno_iscrizione = cliente.data_iscrizione.year
            mese_iscrizione = cliente.data_iscrizione.month

            for mese in mesi:
                iscrizioni_mensili.setdefault(mese, 0)
                iscrizioni_annuali.setdefault(anno_iscrizione, iscrizioni_mensili)

            iscrizioni_annuali[anno_iscrizione][calendar.month_abbr[mese_iscrizione]] += 1

        return iscrizioni_annuali

    @classmethod
    def iscrizioni_annuali(cls, anno):
        iscrizioni_annuali = cls.stat_bilancio()
        iscritti = 0
        if anno in iscrizioni_annuali.keys():
            for iscrizioni_mensili in iscrizioni_annuali[anno]:
                iscritti += iscrizioni_mensili
            return iscritti
        else:
            raise ExceptionAnnoNonPresente

    @classmethod
    def iscrizioni_medie_annuali(cls, anno):
        iscritti = cls.iscrizioni_annuali(anno)
        return iscritti / cls.NUMERO_MESI



