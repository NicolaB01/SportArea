import random
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from Attività.Cliente import Cliente
from Gestore.Eccezioni import ExceptionNomeFormat, ExceptionCognomeFormat, ExceptionCFFormat, ExceptionEmailFormat, \
    ExceptionDataNascitaFormat, ExceptionTelefonoFormat, ExceptionPassword, ExceptionCodiceRecupero, \
    ExceptionEmailSconosciuta, ExceptionEmailUtilizzata


class Gestore_cliente:
    @classmethod
    def registra_cliente(cls, nome, cognome, CF, email, data_nascita, telefono, pwd):
        cls.check_parametri(nome, cognome, CF, email, data_nascita, telefono, pwd)

        try:
            Cliente.cerca_account(email)
            raise ExceptionEmailUtilizzata("Email già in uso")
        except ExceptionEmailSconosciuta:
            clienti = Cliente.get_clienti()
            nuovo_cliente = Cliente(nome, cognome, CF, email, data_nascita, telefono, pwd)
            clienti.append(nuovo_cliente)
            Cliente.set_clienti(clienti)

    @classmethod
    def check_parametri(cls, nome, cognome, CF, email, data_nascita, telefono, pwd):
        cls.check_nome(nome)
        cls.check_congome(cognome)
        cls.check_CF(CF)
        cls.check_email(email)
        cls.check_data_nascita(data_nascita)
        cls.check_teleono(telefono)
        cls.check_pwd(pwd)

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

    @classmethod
    def invia_email_recupero_pwd(cls, email):
        cls.codice_di_verifica = " ".join([str(random.randint(0, 999)).zfill(3) for _ in range(2)])

        mittente = "nbiagioli01@gmail.com"
        oggetto = f"Inserisci questo codice: [{Cliente.codice_di_verifica}] per poter reimpostare la password"

        msg = MIMEMultipart()
        msg['From'] = mittente
        msg['To'] = email
        msg['Subject'] = "Recupero password"
        msg.attach(MIMEText(oggetto))

        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(mittente, "nxnbnjutflbvvugv")
            smtp.send_message(msg)

    @classmethod
    def verifica_codice_recupero_password(cls, email, codice_da_verificare, nuova_pwd):
        if cls.codice_di_verifica != codice_da_verificare:
            raise ExceptionCodiceRecupero("Il codice di recupero non coincide")

        cliente = cls.cerca_account(email)
        cliente.pwd = nuova_pwd

        cliente.salva_modifiche_account()