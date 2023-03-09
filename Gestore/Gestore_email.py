import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Gestore_email:
    codice_di_verifica = None
    mittente = "nbiagioli01@gmail.com"

    @classmethod
    def invia_mail(cls, email_destinatario, oggetto, soggetto):
        msg = MIMEMultipart()
        msg['From'] = cls.mittente
        msg['To'] = email_destinatario
        msg['Subject'] = soggetto
        msg.attach(MIMEText(oggetto))

        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(cls.mittente, "nxnbnjutflbvvugv")
            try:
                smtp.send_message(msg)
            except smtplib.SMTPRecipientsRefused:
                pass

    @classmethod
    def invia_email_prenotazione(cls, destinatario, prenotazione, attività):
        soggetto = "Conferma prenotazione"
        oggetto = f"La tua prenotazione è stata effettuata correttamente.\n\n" \
                  f"Attività: {attività}\n" \
                  f"Nome campo: {prenotazione.get_nome_campo()}\n" \
                  f"Data: {prenotazione.get_data_attività().strftime('%d/%m/%Y')}\n" \
                  f"Ora: {prenotazione.get_data_attività().strftime('%H:%M')}\n" \

        cls.invia_mail(destinatario.get_email(), oggetto, soggetto)

    @classmethod
    def invia_email_richiesta_amicizia(cls, destinatario):
        soggetto = "Richiesta amicizia"
        oggetto = f"{destinatario.get_nome()} {destinatario.get_cognome()} vuole stringere amicizia con te."

        cls.invia_mail(destinatario.get_email(), oggetto, soggetto)

    @classmethod
    def invia_email_recupero_pwd(cls, email_destinatario):
        cls.codice_di_verifica = " ".join([str(random.randint(0, 999)).zfill(3) for _ in range(2)])

        soggetto = "Recupero password"
        oggetto = f"Inserisci questo codice: [{cls.codice_di_verifica}] per poter reimpostare la password"

        cls.invia_mail(email_destinatario, oggetto, soggetto)

    @classmethod
    def invia_email_modifica_account(cls, email_destinatario):
        soggetto = "Modifica account"
        oggetto = "Il tuo profilo è stato modificato correttamente"

        cls.invia_mail(email_destinatario, oggetto, soggetto)

    @classmethod
    def invia_email_crea_account(cls, destinatario):
        soggetto = "Registraziona effettuata"
        oggetto = f"Ciao {destinatario.get_nome()},\n\n" \
                  f"Ti diamo il benvenuto in SportArea!"

        cls.invia_mail(destinatario.get_email(), oggetto, soggetto)

    @classmethod
    def invia_email_ricarica_portafoglio(cls, email_destinatario, importo):
        soggetto = "Ricarica effettuata"
        oggetto = f"Gentile Cliente,\n" \
                  f"la ricarica del credito è andata a buon fine, per un importo di €{importo}."

        cls.invia_mail(email_destinatario, oggetto, soggetto)
