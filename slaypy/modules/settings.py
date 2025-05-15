from typing import Literal, Iterable

class Settings:

    class GamingServer:
        def __init__(self, socket: str):
            self.socket = socket

    def __init__(
            self,

            objects: Iterable[Literal["basic", "lobby"]] = ["basic"],
            operators: Iterable[Literal["basic"]] = ["basic"],

            disable_events: Iterable[str] = []
        ):

        self.objects = objects
        self.operators = operators
        
        self.disable_events = disable_events