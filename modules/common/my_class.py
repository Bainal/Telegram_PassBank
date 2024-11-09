from datetime import datetime


class Users(object):
    def __init__(self, id: int, telegram_id: int, masterkey_lifetime: datetime):
        self.id: int = id
        self.telegram_id: int = telegram_id
        self.masterkey_lifetime: datetime = masterkey_lifetime


class Passwords(object):
    def __init__(
        self,
        id: int = None,
        user: int = None,
        service_name: str = None,
        login: str = None,
        password: str = None,
    ):
        self.id: int = id
        self.user: int = user
        self.service_name: str = service_name
        self.login: str = login
        self.password: str = password
