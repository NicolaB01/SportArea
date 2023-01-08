import os.path
import pickle


class Campo:
    PATH_INFOCAMPI = "../DataBase/Campi/InfoCampi.txt"

    def __init__(self, nome, numero_max_partecipanti, prezzo, attività):
        self.nome = nome
        self.numero_max_partecipanti = numero_max_partecipanti
        self.prezzo = prezzo
        self.attività = attività
        self.path_prenotazioni = f"../DataBase/Campi/Prenotazioni_campo_{self.nome}.txt"

    def __str__(self):
        return f"""
        nome: {self.nome}
        numero max partecipanti: {self.numero_max_partecipanti}
        prezzo: {self.prezzo}
        attività: {self.attività}
        """

    def __eq__(self, other):
        return isinstance(other, Campo) and self.nome == other.nome and self.prezzo == other.prezzo and self.numero_max_partecipanti == other.numero_max_partecipanti and self.attività == other.attività

    @classmethod
    def crea_campo(cls, nome, numero_max_partecipanti, prezzo, attività):
        già_presente = False
        campi = []
        campo = Campo.cerca_campo(nome)
        if campo is not None:
            già_presente = True

        with open(Campo.PATH_INFOCAMPI, "wb") as f:
            if not già_presente:
                nuovo_campo = Campo(nome, numero_max_partecipanti, prezzo, attività)
                campi.append(nuovo_campo)
                open(nuovo_campo.path_prenotazioni, "x")
            pickle.dump(campi, f, pickle.HIGHEST_PROTOCOL)

    def modifica_campo(self, nuovo_numero_max_partecipanti, nuovo_prezzo, nuova_attività):
        if os.path.getsize(Campo.PATH_INFOCAMPI) != 0:
            with open(Campo.PATH_INFOCAMPI, "rb") as f:
                campi = pickle.load(f)
                indice = campi.index(self)
                self.numero_max_partecipanti = nuovo_numero_max_partecipanti
                self.prezzo = nuovo_prezzo
                self.attività = nuova_attività
                campi[indice] = self

            with open(Campo.PATH_INFOCAMPI, "wb") as f:
                pickle.dump(campi, f, pickle.HIGHEST_PROTOCOL)

    def elimina_campo(self):
        if os.path.getsize(Campo.PATH_INFOCAMPI) != 0:
            with open(Campo.PATH_INFOCAMPI, "rb") as f:
                campi = pickle.load(f)
                campi.remove(self)
                os.remove(self.path_prenotazioni)
            with open(Campo.PATH_INFOCAMPI, "wb") as f:
                pickle.dump(campi, f, pickle.HIGHEST_PROTOCOL)

    @classmethod
    def cerca_campo(cls, nome):
        if os.path.getsize(Campo.PATH_INFOCAMPI) != 0:
            with open(Campo.PATH_INFOCAMPI, "rb") as f:
                campi = pickle.load(f)
                for i in range(len(campi)):
                    if campi[i].nome == nome:
                        return campi[i]
        return None


    def controlla_disponibilità(self, data_attività):
           prenotazioni = Prenotazione.get_prenotazioni(self)

#Campo.crea_campo("maradona", 20000, 60, "calcio")
Campo.cerca_campo("maradona").controlla_disponibilità("2023/02/12/15")
