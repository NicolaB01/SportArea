import calendar

from Utils.Eccezioni import ExceptionAnnoNonPresente, ExceptionCampoInesistente
from Gestore.Gestore_campo import Gestore_campo
from Gestore.Gestore_cliente import Gestore_cliente
from Gestore.Gestore_ricevuta import Gestore_ricevuta


class Gestore_statistiche:
    NUMERO_MESI = 12

    #Questo metodo ridà il fatturato mensile di ogni anno di attività
    @classmethod
    def get_statistiche_fatturato(cls):
        ricevute = Gestore_ricevuta.get_ricevute()
        entrate_annuali = {}

        mesi = []
        for numero_mese in range(1, 13):
            mesi.append(calendar.month_abbr[numero_mese])

        for ricevuta in ricevute:
            entrate_mensili = {}
            anno_ricevuta = ricevuta.prenotazione.data_attivita.year
            mese_ricevuta = ricevuta.prenotazione.data_attivita.month

            for mese in mesi:
                entrate_mensili.setdefault(mese, 0)
                entrate_annuali.setdefault(anno_ricevuta, entrate_mensili)

            entrate_annuali[anno_ricevuta][calendar.month_abbr[mese_ricevuta]] += ricevuta.prezzo

        return entrate_annuali

    #Questo metodo ridà il fatturato dell'anno passato come parametro
    @classmethod
    def guadagno_annuale(cls, anno):
        entrate_annuali = cls.get_statistiche_fatturato()
        ricavo = 0
        if anno in entrate_annuali.keys():
            for incassi_mensili in entrate_annuali[anno].values():
                ricavo += incassi_mensili
            return ricavo
        else:
            raise ExceptionAnnoNonPresente

    #Questo metodo ridà il fatturato medio dell'anno passato come parametro
    @classmethod
    def guadagno_medio_annuale(cls, anno):
        ricavo = cls.guadagno_annuale(anno)
        return ricavo/cls.NUMERO_MESI

    #Questo metodo ridà la lista delle età di tutti i clienti salvati
    @classmethod
    def get_statistiche_eta(cls):
        clienti = Gestore_cliente.get_clienti()
        eta_clienti = []
        for cliente in clienti:
            eta_clienti.append(cliente.eta())

        return eta_clienti

    #Questo metodo ridà l'età media di tutti i clienti salvati
    @classmethod
    def eta_media(cls):
        eta_clienti = cls.get_statistiche_eta()
        eta_totale = 0
        for eta in eta_clienti:
            eta_totale += eta
        numero_clienti = len(Gestore_cliente.get_clienti())
        if numero_clienti != 0:
            return eta_totale/numero_clienti
        return numero_clienti

    #Questo metodo ridà il numero di prenotazioni per attività, divise in anni
    @classmethod
    def get_statistiche_attivita(cls):
        ricevute = Gestore_ricevuta.get_ricevute()
        attivita = {}

        for ricevuta in ricevute:
            anno_ricevute = int(ricevuta.get_prenotazione().get_data_attivita().year)
            attivita_prenotazione = {}
            try:
                campo = Gestore_campo.cerca_campo(ricevuta.get_prenotazione().get_nome_campo())

                attivita.setdefault(anno_ricevute, attivita_prenotazione)
                if campo.get_attivita() in attivita[anno_ricevute].keys():
                    attivita[anno_ricevute][campo.attivita] += 1

                attivita[anno_ricevute].setdefault(campo.attivita, 1)
            except ExceptionCampoInesistente:
                pass

        return attivita

    #Questo metodo ridà il numero totale delle prenotazioni effettuate sull'applicazione
    @classmethod
    def prenotazioni_totali(cls):
        return len(Gestore_ricevuta.get_ricevute())

    #Questo metodo ridà il numero totale delle prenotazioni nell'anno passato come parametro
    @classmethod
    def prenotazioni_annuali(cls, anno):
        prenotazioni = cls.get_statistiche_attivita()
        prenotazioni_annuali = 0
        for prenotazioni_mensili in prenotazioni[anno].values():
            prenotazioni_annuali += prenotazioni_mensili

        return prenotazioni_annuali

    #Questo metodo ridà le iscrizioni mensile di ogni anno di attività
    @classmethod
    def get_statistiche_iscrizioni(cls):
        clienti = Gestore_cliente.get_clienti()
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

    #Questo metodo il numero d'iscritti all'applicazione nell'anno passato come parametro
    @classmethod
    def iscrizioni_annuali(cls, anno):
        anno = int(anno)
        iscrizioni_annuali = cls.get_statistiche_iscrizioni()
        iscritti = 0

        if anno in iscrizioni_annuali.keys():
            for iscrizioni_mensili in iscrizioni_annuali[anno].values():
                iscritti += iscrizioni_mensili
            return iscritti
        else:
            raise ExceptionAnnoNonPresente

    #Questo metodo il numero medio d'iscritti all'applicazione nell'anno passato come parametro
    @classmethod
    def iscrizioni_medie_annuali(cls, anno):
        iscritti = cls.iscrizioni_annuali(anno)
        return iscritti / cls.NUMERO_MESI
