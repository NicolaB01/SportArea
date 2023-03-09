import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from Utils.Eccezioni import ExceptionCodiceRecupero
from Gestore.Gestore_cliente import Gestore_cliente

#TODO fare una classe per la gestione delle email che puù essere tranquillamente questa
class Gestore_email:
    def __int__(self):
        self.codice_di_verifica

    @classmethod
    def invia_email_prenotazione(cls, email_destinatario):
        pass

    @classmethod
    def invia_email_richiesta_amicizia(cls, email_destinatario):
        pass

    @classmethod
    def invia_email_recupero_pwd(cls, email_destinatario):
        cls.codice_di_verifica = " ".join([str(random.randint(0, 999)).zfill(3) for _ in range(2)])

        mittente = "nbiagioli01@gmail.com"
        oggetto = f"Inserisci questo codice: [{cls.codice_di_verifica}] per poter reimpostare la password"

        msg = MIMEMultipart()
        msg['From'] = mittente
        msg['To'] = email_destinatario
        msg['Subject'] = "Recupero password"
        msg.attach(MIMEText(oggetto))

        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(mittente, "nxnbnjutflbvvugv")
            smtp.send_message(msg)

    @classmethod
    def invia_email_modifica_account(cls, email_destinatario):
        pass

    @classmethod
    def invia_email_crea_account(cls, email_destinatario):
        pass

    @classmethod
    def invia_email_ricarica_portafoglio(cls, email_destinatario):
        pass


    #TODO questa la inserirei nella classe gestore cliente
    @classmethod
    def verifica_codice_recupero_password(cls, email, codice_da_verificare, nuova_pwd, conferma_nuova_pwd):
        if cls.codice_di_verifica != codice_da_verificare:
            raise ExceptionCodiceRecupero("Il codice di recupero non coincide")

        Gestore_cliente.check_pwd(nuova_pwd, conferma_nuova_pwd)

        cliente = Gestore_cliente.cerca_account(email)
        cliente.pwd = nuova_pwd

        cliente.salva_modifiche_account()