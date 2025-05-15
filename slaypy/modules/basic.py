# will be like plugins that be able to add or remove on Client class
from typing import Callable

class BasicOperator:
    def __init__(self, send_message: Callable[[str], None]):
        self.__send_messsage = send_message

        self.__opackets = {}
    
    def login(self, username: str, password: str): pass

    def __getattribute__(self, name):
        if name[0] == "_":
            return super().__getattribute__(name)

        def operation(*args):
            self.__send_messsage(f"{self.__opackets.get(name, name)}$"+"$".join(map(str, args)))

        return operation