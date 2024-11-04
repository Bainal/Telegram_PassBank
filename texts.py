TEXTS = {"menu": "Это меню", "check": "Вы нажали на кнопку", "ik_check": "Проверка"}


def get_text(key: str) -> str:
    return TEXTS.get(key, key)
