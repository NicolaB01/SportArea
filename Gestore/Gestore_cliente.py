import re

from Attività.Cliente import Cliente
from Gestore.Eccezioni import ExceptionNomeFormat, ExceptionCognomeFormat, ExceptionCFFormat, ExceptionEmailFormat, \
    ExceptionDataNascitaFormat, ExceptionTelefonoFormat, ExceptionPassword, ExceptionCodiceRecupero


class Gestore_cliente:
    @classmethod
    def registra_cliente(cls, nome, cognome, CF, email, data_nascita, telefono, pwd):
        cls.check_nome(nome)
        cls.check_congome(cognome)
        cls.check_CF(CF)
        cls.check_email(email)
        cls.check_data_nascita(data_nascita)
        cls.check_teleono(telefono)
        cls.check_pwd(pwd)
        Cliente.crea(nome, cognome, CF, email, data_nascita, telefono, pwd)

    @classmethod
    def modifica_cliente(cls, nuovo_nome, nuovo_cognome, nuovo_CF, nuovo_telefono, nuova_password, nuova_password_conferma, nuova_data_nascita):
        cls.check_nome(nuovo_nome)
        cls.check_congome(nuovo_cognome)
        cls.check_CF(nuovo_CF)
        cls.check_data_nascita(nuova_data_nascita)
        cls.check_teleono(nuovo_telefono)
        cls.check_pwd(nuova_password, nuova_password_conferma)
        Cliente.modifica_account(nuovo_nome, nuovo_cognome, nuovo_CF, nuovo_telefono, nuova_password, nuova_data_nascita)

    @classmethod
    def check_nome(cls, nome):
        if len(nome) < 3:
            raise ExceptionNomeFormat("Il nome è troppo corto")

    @classmethod
    def check_congome(cls, cognome):
        if len(cognome) < 3:
            raise ExceptionCognomeFormat("Il cognome è troppo corto")

    @classmethod
    def check_CF(cls, CF):
        if len(CF) != 16 or not CF.isalnum():
            raise ExceptionCFFormat("Codice fiscale errato")

    @classmethod
    def check_email(cls, email):
        if "@" not in email:
            raise ExceptionEmailFormat("L'email non presenta la @")

    @classmethod
    def check_data_nascita(cls, data_nascita):
        try:
            if re.match(re.compile("[0-9]{2}/[0-9]{2}/[0-9]{4}"), data_nascita) is None:
                raise ExceptionDataNascitaFormat("La data non rispetta il formato dd/mm/YYYY")

        except ValueError:
            raise ExceptionDataNascitaFormat("La data non rispetta il formato dd/mm/YYYY")

    @classmethod
    def check_teleono(cls, telefono):
        if len(telefono) != 10 or not telefono.isnumeric():
            raise ExceptionTelefonoFormat("Il numero di telefono non presenta 10 carattero o non sono solo numeri")

    @classmethod
    def check_pwd(cls, pwd, conferma_password=None):
        if pwd != conferma_password and conferma_password is not None:
            raise ExceptionPassword("Le password non coincidono")

        if re.search(re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$"),
                     pwd) is None:
            raise ExceptionPassword(
                "La password deve essere di almeno 8 caratteri, maiuscole, minuscole, numeri e caratteri speciali")

