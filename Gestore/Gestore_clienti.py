import re
import datetime

from Gestore.Eccezioni import *


class Gestore_clienti:
    def __init__(self):
        pass

    def check_nome(self, nome):
        if len(nome) < 3:
            raise ExceptionNomeFormat("Il nome è troppo corto")

    def check_congome(self, cognome):
        if len(cognome) < 3:
            raise ExceptionCognomeFormat("Il cognome è troppo corto")

    def check_CF(self, CF):
        if len(CF) != 16 or not CF.isalnum():
            raise ExceptionCFFormat("Codice fiscale errato")

    def check_email(self, email):
        if "@" not in email:
            raise ExceptionEmailFormat("L'email non presenta la @")

    def check_data_nascita(self, data_nascita):
        try:
            if re.match(re.compile("[0-9]{2}/[0-9]{2}/[0-9]{4}"), data_nascita) is None:
                raise ExceptionDataNascitaFormat("La data non rispetta il formato dd/mm/YYYY")

            day, month, year = data_nascita.split('/')
            datetime.datetime(int(year), int(month), int(day))
        except ValueError:
            raise ExceptionDataNascitaFormat("La data non rispetta il formato dd/mm/YYYY")

    def check_teleono(self, telefono):
        if len(telefono) != 10 or not telefono.isnumeric():
            raise ExceptionTelefonoFormat("Il numero di telefono non presenta 10 carattero o non sono solo numeri")

    def check_pwd(self, pwd):
        if re.search(re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$"), pwd) is None:
            raise ExceptionPassword("La password deve essere di almeno 8 caratteri, maiuscole, minuscole, numeri e caratteri speciali")

    def check_pwd(self, pwd, conferma_password):
        if pwd != conferma_password:
            raise ExceptionPassword("Le password non coincidono")

        if re.search(re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$"), pwd) is None:
            raise ExceptionPassword("La password deve essere di almeno 8 caratteri, maiuscole, minuscole, numeri e caratteri speciali")
