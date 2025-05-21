# will be like plugins that be able to add or remove on Client class
from typing import Callable

class BasicOperator:
    def __init__(self, send_message: Callable[[str], None]):
        self._send_messsage = send_message

        self._opackets = {}
    
    def login(self, username: str, password: str): pass

    def __getattribute__(self, name):
        if name[0] == "_":
            return super().__getattribute__(name)

        def operation(*args):
            self._send_messsage(f"{self._opackets.get(name, name)}$"+"$".join(map(str, args)))

        return operation