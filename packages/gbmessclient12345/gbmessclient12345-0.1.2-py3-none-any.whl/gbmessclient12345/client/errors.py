"""Модуль с общими классами клиентских исключений"""


class ClientDBError(Exception):
    def __init__(self, *args: object, msg="") -> None:
        super().__init__(*args)
        self._msg = msg

    def __str__(self):
        if self._msg:
            return f"DB error: {self._msg}"

        return f"DB error"


class ClientNoConnectionError(Exception):
    def __str__(self):
        return f"Отсутствует подключение к серверу"
