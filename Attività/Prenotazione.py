from Attività.Campo import Campo


class Prenotazione:
    def __init__(self, cliente, data_prenotazione, campo, partecipanti):
        self.cliente = cliente
        self.data_prenotazione = data_prenotazione
        self.campo = campo
        self.partecipanti = partecipanti

    @classmethod
    def prenota_campo(cls, cliente, nome_campo, ora_inizio, ora_fine, giorno, mese, anno):
        if Campo.cerca_campo(nome_campo).controlla_disponibilità(ora_inizio, ora_fine, giorno, mese, anno):
            with open(Campo.cerca_campo(nome_campo).path_prenotazioni, "a") as f:
                f.write(f"{ora_inizio}-{ora_fine} {giorno}/{mese}/{anno}\n")
            return Prenotazione(cliente, f"{ora_inizio}-{ora_fine} {giorno}/{mese}/{anno}", nome_campo, None)


Prenotazione.prenota_campo("nicola", "san siro", 18,20,27,12,2022)