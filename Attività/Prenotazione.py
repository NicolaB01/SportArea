import datetime
import os.path
import pickle
from Attività.Cliente import Cliente
from Campo import Campo


class Prenotazione:
    FASCE_ORARIE = list(range(8, 23))

    #data_attività oggetto del tipo datetime(anno, mese, gionro, ora)
    def __init__(self, cliente, data_attività, campo, partecipanti):
        self.cliente = cliente
        self.data_attività = data_attività
        self.campo = campo
        self.partecipanti = partecipanti
        self.modificabile = True

    def __eq__(self, other):
        return isinstance(other,Prenotazione) and self.cliente == other.cliente and self.data_prenotazione == other.data_prenotazione and self.campo == other.campo and self.partecipanti == other.partecipanti

    #controlla che nel campo scelto non vi siano già altre prenotazioni per quella stessa fascia oraria poi salva la nuova prenotazione e la aggiunge alle prenotazioni del cliente
    @classmethod
    def prenota_campo(cls, nome_campo, data_attività, partecipanti):
        campo = Campo.cerca_campo(nome_campo)
        prenotazioni = []
        if os.path.getsize(campo.path_prenotazioni) != 0:
            if campo.controlla_disponibilità(data_attività):
                with open(campo.path_prenotazioni,"rb+") as f:
                    prenotazioni = pickle.load(f)
                    prenotazioni.append(Prenotazione(Cliente.get_account_connesso(), data_attività, nome_campo, partecipanti))
                    pickle.dump(prenotazioni,f,pickle.HIGHEST_PROTOCOL)
        else:
            with open(campo.path_prenotazioni, "wb") as f:
                prenotazioni.append(Prenotazione(Cliente.get_account_connesso(), data_attività, nome_campo, partecipanti))
                pickle.dump(prenotazioni, f, pickle.HIGHEST_PROTOCOL)

    def modifica_prenotazione(self):
        pass

    #TODO da fare mi raddopia le prenotazioni invece di toglierle
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