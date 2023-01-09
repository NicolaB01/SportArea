import datetime
import os.path
import pickle
from Attività.Cliente import Cliente
from Campo import Campo


class Prenotazione:
    FASCE_ORARIE = list(range(8, 23))

    def __init__(self, cliente, data_attività, campo, partecipanti):
        self.cliente = cliente
        self.data_attività = data_attività
        self.campo = campo
        self.partecipanti = partecipanti
        self.modificabile = True

    def __str__(self):
        return f"""
            cliente         :{self.cliente}
            data attività   :{self.data_attività}
            campo           :{self.campo}
            partecipanti    :{self.partecipanti}
            """

    def __eq__(self, other):
        return isinstance(other,
                          Prenotazione) and self.cliente == other.cliente and self.data_prenotazione == other.data_prenotazione and self.campo == other.campo and self.partecipanti == other.partecipanti

    @classmethod
    def prenota_campo(cls, nome_campo, data_attività, partecipanti):
        campo = Campo.cerca_campo(nome_campo)
        prenotazioni = []
        if os.path.getsize(campo.path_prenotazioni) != 0:
            with open(campo.path_prenotazioni, "rb") as f:
                prenotazioni = pickle.load(f)
                prenotazioni.append(Prenotazione(Cliente.get_account_connesso(), data_attività, nome_campo, partecipanti))

            with open(campo.path_prenotazioni, "wb") as f:
                pickle.dump(prenotazioni, f, pickle.HIGHEST_PROTOCOL)
        else:
            with open(campo.path_prenotazioni, "wb") as f:
                prenotazioni.append(Prenotazione(Cliente.get_account_connesso(), data_attività, nome_campo, partecipanti))

                pickle.dump(prenotazioni, f, pickle.HIGHEST_PROTOCOL)

    #ridà una lista di prenotaioni
    @classmethod
    def filtra_prenotazione(cls, attività, giorno, mese, anno, ora_inizio):
        campi_idonei = []
        with open(Campo.PATH_INFOCAMPI, "rb") as f:
            campi = pickle.load(f)
            for campo in campi:
                if campo.attività == attività:
                    campi_idonei.append(campo)

        prenotazioni_disponibili = {}
        for campo in campi_idonei:
            lista_ore = list(range(ora_inizio, 22))
            with open(campo.path_prenotazioni, "rb") as f:
                prenotazioni_effetuate = pickle.load(f)
                for prenotazione in prenotazioni_effetuate:
                    anno_prenotazione, mese_prenotazione, giorno_prenotazione, ora_prenotazione = prenotazione.spliy("/")

                    if anno_prenotazione == anno and mese_prenotazione == mese and giorno_prenotazione == giorno:
                        if ora_prenotazione >= ora_inizio:
                            lista_ore.remove(ora_prenotazione)

                prenotazioni_disponibili[campo] = lista_ore

        return prenotazioni_disponibili






    def aggiugni_partecipante(self):
        pass

    # TODO da fare mi raddopia le prenotazioni invece di toglierle
    def elimina_prenotazione(self):
        with open(Campo.PATH_INFOCAMPI, "rb") as f:
            campi = pickle.load(f)
            for i in range(len(campi)):
                campo = Campo.cerca_campo(campi[i].nome)
                if os.path.getsize(campo.path_prenotazioni) != 0:
                    with open(campo.path_prenotazioni, "rb+") as f:
                        prenotazioni = pickle.load(f)
                        for j in range(len(prenotazioni)):
                            if prenotazioni[j] == self:
                                prenotazioni.remove(self)
                                print(prenotazioni)
                        pickle.dump(prenotazioni, f, pickle.HIGHEST_PROTOCOL)

    @classmethod
    def get_prenotazioni(cls, nome_campo):
        campo = Campo.cerca_campo(nome_campo)
        if os.path.getsize(campo.path_prenotazioni) != 0:
            with open(campo.path_prenotazioni, "rb+") as f:
                return pickle.load(f)

    @classmethod
    def cerca_prenotazione(cls, cliente):
        with open(Campo.PATH_INFOCAMPI, "rb") as f:
            campi = pickle.load(f)
            for i in range(len(campi)):
                campo = Campo.cerca_campo(campi[i].nome)
                if os.path.getsize(campo.path_prenotazioni) != 0:
                    with open(campo.path_prenotazioni, "rb+") as f:
                        prenotazioni = pickle.load(f)
                        for j in range(len(prenotazioni)):
                            if prenotazioni[i].cliente.nome == cliente:
                                return prenotazioni[i]


