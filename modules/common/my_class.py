from datetime import datetime


class Users(object):
    def __init__(self, id: int, telegram_id: int, masterkey_lifetime: datetime):
        self.id = id
        self.telegram_id = telegram_id
        self.masterkey_lifetime = masterkey_lifetime
