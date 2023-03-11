class ExceptionPassword(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class ExceptionTentativi(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class ExceptionCodiceRecupero(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class ExceptionEmailSconosciuta(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class ExceptionNomeFormat(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class ExceptionCognomeFormat(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class ExceptionCFFormat(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class ExceptionDataNascitaFormat(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class ExceptionTelefonoFormat(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class ExceptionEmailFormat(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class ExceptionAmicizia(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class ExceptionSaldoInsufficente(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class ExceptionDataPassata(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class ExceptionGiornoFestivo(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class ExceptionOra(Exception):
    def __init__(self):
        super().__init__()


class ExceptionPrenotazioneInesistente(Exception):
    def __init__(self):
        super().__init__()


class ExceptionSaldoInsufficente(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class ExceptionPreotazioneNonModificabile(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class ExceptionCampoInesistente(Exception):
    def __init__(self):
        super().__init__()


class ExceptionAnnoNonPresente(Exception):
    def __init__(self):
        super().__init__()


class ExceptionEmailUtilizzata(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class ExceptionNomeCampoUtilizzato(Exception):
    def __init__(self, msg):
        super().__init__(msg)



