import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Gestore_email:
    codice_di_verifica = None
    #va inserita l'email del centro sportivo da cui partiranno le comunicazioni
    mittente = None
    #va inserita la password per le app della mail selezionata
    password = None

    #Questo metodo permette l'invio di una email con i parametri forniti
    @classmethod
    def invia_email(cls, email_destinatario, oggetto, soggetto):
        msg = MIMEMultipart()
        msg['From'] = cls.mittente
        msg['To'] = email_destinatario
        msg['Subject'] = soggetto
        msg.attach(MIMEText(oggetto))

        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            try:
                if cls.password is not None or cls.mittente is not None:
                    smtp.login(cls.mittente, cls.password)
                    smtp.send_message(msg)
            except smtplib.SMTPRecipientsRefused:
                print("Invio fallito")

    #Questo metodo invia una email relativa alla prenotazione effettuata
    @classmethod
    def invia_email_prenotazione(cls, destinatario, prenotazione, attivita):
        soggetto = "Conferma prenotazione"
        oggetto = f"La tua prenotazione è stata effettuata correttamente.\n\n" \
                  f"Attività: {attivita}\n" \
                  f"Nome campo: {prenotazione.get_nome_campo()}\n" \
                  f"Data: {prenotazione.get_data_attivita().strftime('%d/%m/%Y')}\n" \
                  f"Ora: {prenotazione.get_data_attivita().strftime('%H:%M')}\n"

        cls.invia_email(destinatario.get_email(), oggetto, soggetto)

    #Questo metodo invia una email al cliente che ha ricevuto una richiesta di amicizia
    @classmethod
    def invia_email_richiesta_amicizia(cls, destinatario, mittete):
        soggetto = "Richiesta amicizia"
        oggetto = f"{mittete.get_nome()} {mittete.get_cognome()} vuole stringere amicizia con te."

        cls.invia_email(destinatario.get_email(), oggetto, soggetto)

    #Questo metodo invia una email con il codice di recupero della password
    @classmethod
    def invia_email_recupero_pwd(cls, destinatario):
        cls.codice_di_verifica = " ".join([str(random.randint(0, 999)).zfill(3) for _ in range(2)])

        soggetto = "Recupero password"
        oggetto = f"Inserisci questo codice: [{cls.codice_di_verifica}] per poter reimpostare la password"

        cls.invia_email(destinatario.get_email(), oggetto, soggetto)

    #Questo metodo invia una email relativa alla modifica dell'account
    @classmethod
    def invia_email_modifica_account(cls, destinatario):
        soggetto = "Modifica account"
        oggetto = "Il tuo profilo è stato modificato correttamente"

        cls.invia_email(destinatario.get_email(), oggetto, soggetto)

    #Questo metodo invia una email al cliente appena effettua la registrazione
    @classmethod
    def invia_email_crea_account(cls, destinatario):
        soggetto = "Registraziona effettuata"
        oggetto = f"Ciao {destinatario.get_nome()},\n\n" \
                  f"Ti diamo il benvenuto in SportArea!"

        cls.invia_email(destinatario.get_email(), oggetto, soggetto)

    #Questo metodo invia una email ogni qualvolta si effettui una ricarica del saldo
    @classmethod
    def invia_email_ricarica_portafoglio(cls, destinatario, importo):
        soggetto = "Ricarica effettuata"
        oggetto = f"Gentile Cliente,\n" \
                  f"la ricarica del credito è andata a buon fine, per un importo di €{importo}."

        cls.invia_email(destinatario.get_email(), oggetto, soggetto)
