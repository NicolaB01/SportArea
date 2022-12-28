import os.path
import pickle
import shutil


class Campo:
    def __init__(self, nome, numero_max_partecipanti, prezzo, attività):
        self.nome = nome
        self.numero_max_partecipanti = numero_max_partecipanti
        self.prezzo = prezzo
        self.attività = attività
        self.path_prenotazioni = f"../DataBase/Campi/Prenotazioni_campo_{self.nome}.txt"
        open(self.path_prenotazioni, "x")

    @classmethod
    def crea_campo(cls, nome, numero_max_partecipanti, prezzo, attività):
        gia_presente = False
        with open("/Users/nicola/PycharmProjects/ProgettoIDS/DataBase/Campi/InfoCampi", "rb+") as f:
            while True:
                try:
                    if pickle.load(f).nome == nome:
                        gia_presente = True
                        print("Gia presente")
                except (EOFError, pickle.UnpicklingError):
                    break
            if not gia_presente:
                pickle.dump(Campo(nome, numero_max_partecipanti, prezzo, attività), f, pickle.HIGHEST_PROTOCOL)

    def modifica_campo(self, nuovo_numero_max_partecipanti, nuovo_prezzo, nuova_attività):
        with open(os.path.join("DataBase", "Campi","InfoCampi"), "rb+") as f:
            with open(os.path.join("DataBase", "temp"), "wb") as temp:

                while True:
                    try:
                        campo = pickle.load(f)
                        if campo.nome == self.nome:
                            self.numero_max_partecipanti = nuovo_numero_max_partecipanti
                            self.prezzo = nuovo_prezzo
                            self.attività = nuova_attività

                            pickle.dump(self, temp, pickle.HIGHEST_PROTOCOL)
                        else:
                            pickle.dump(campo, temp, pickle.HIGHEST_PROTOCOL)

                    except (EOFError, pickle.UnpicklingError):
                        break

            shutil.copy("DataBase/temp", "DataBase/Campi/InfoCampi")
            os.remove(os.path.join("DataBase", "temp"))

    @classmethod
    def elimina_campo(cls, nome):
        pass

    @classmethod
    def cerca_campo(cls, nome):
        with open("/Users/nicola/PycharmProjects/ProgettoIDS/DataBase/Campi/InfoCampi", "rb") as f:
            while True:
                try:
                    campo = pickle.load(f)
                    if campo.nome == nome:
                            return campo
                except (EOFError, pickle.UnpicklingError):
                    break

    def controlla_disponibilità(self, ora_prenotazione_inizio, ora_prenotazione_fine, giorno_prenotazione, mese_prenotazione, anno_prenotazione):
        with open(self.path_prenotazioni, "r") as f:
            for riga in f:
                ora_inizio, ora_fine, giorno, mese, anno = riga.split(",")
                if giorno_prenotazione == int(giorno) and mese_prenotazione == int(mese) and anno_prenotazione == int(anno):
                    if ora_prenotazione_inizio >= int(ora_inizio) and ora_prenotazione_inizio < int(ora_fine) or ora_prenotazione_fine > int(ora_inizio) and ora_prenotazione_fine <= int(ora_fine):
                        return False
            return True

    def __str__(self):
        return f"nome: {self.nome}\nnumero max partecipanti: {self.numero_max_partecipanti}\n" \
               f"prezzo: {self.prezzo}\nattività: {self.attività}\n"

