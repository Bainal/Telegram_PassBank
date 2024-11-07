from datetime import datetime


class Users(object):
    def __init__(self, id: int, telegram_id: int, masterkey_lifetime: datetime):
        self.id: int = id
        self.telegram_id: int = telegram_id
        self.masterkey_lifetime: datetime = masterkey_lifetime
