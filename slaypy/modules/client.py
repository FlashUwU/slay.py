import asyncio, threading
from typing import Literal, Iterable

from ..core.ws import Connection
from ..core.enums import Socket
from ..utils.network import find_nearest_socket
from ..utils.types import AsyncFunc

from ..objects.basic import Player
from .basic import BasicOperator
from .settings import Settings

class Client:
    def __init__(
            self, name: str = "client",
            
            gaming_server: Literal["EU", "NA", "ASIA", "auto"] = None,
            friends_server: bool = False,
            event_registration_mode: int = 3,

            settings: Settings = Settings()
        ):

        self.name = name
        self.gaming_server= gaming_server
        self.friends_server = friends_server
        self.event_registration_mode = event_registration_mode

        self.events = Events()
        self.async_loop = asyncio.new_event_loop()

        self.player: Player = None

        # try to create connection

        if gaming_server.lower() == "auto":
            gs_socket = find_nearest_socket(type="Gaming")

            if gs_socket:
                self.gs_conn = Connection.from_client(self, gs_socket, settings)
            else:
                raise TimeoutError("Error occurs while finding the nearest server socket.")

        elif gaming_server:
            self.gs_conn = Connection.from_client(self, Socket[gaming_server.upper], settings)

        else: self.gs_conn = None
        
        # setup operators

        self.basic = BasicOperator(self.gs_conn.send_message) if "basic" in settings.operators else None

        # try to registry connection event function
        
        self.registry_event("_close", self.close)

    def event(self, name: str): # use for registrying event

        def decorator(async_func: AsyncFunc):
            if not asyncio.iscoroutinefunction(async_func):
                raise TypeError("Event function must be asynchronous function.")
            
            self.registry_event(name, async_func)

            return async_func
        
        return decorator

    def registry_event(self, event_name: str, async_func: AsyncFunc):
        match self.event_registration_mode:
            case 1: _registry_event1(self, event_name, async_func)
            case 2: _registry_event2(self, event_name, async_func)
            case 3: _registry_event3(self, event_name, async_func)

    def unregistry_event(self, event_name: str, async_func: AsyncFunc):
        match self.event_registration_mode:
            case 1: _unregistry_event1(self, event_name, async_func)
            case 2: _unregistry_event2(self, event_name, async_func)
            case 3: _unregistry_event3(self, event_name, async_func)

    def trigger_event(self, event_name: str, *args, **kwargs):
        try:
            efuncs: Iterable[AsyncFunc] = getattr(self.events, event_name)

            for efunc in efuncs:
                try: self.async_loop.call_soon_threadsafe(self.async_loop.create_task, efunc(*args, **kwargs))
                except: continue

        except AttributeError: pass

        except Exception as e: print(e)

    def run(self): # start all necessary loops
        threading.Thread(target=self.async_loop.run_forever).start()
        if self.gs_conn: self.gs_conn.connect()

    def stop(self): # stop all running loops
        if self.gs_conn:
            self.gs_conn.disconnect()
            self.gs_conn.object.shutdown()
        self.async_loop.call_soon_threadsafe(self.async_loop.stop)

    async def close(self): # close all running loops
        if self.gs_conn:
            self.gs_conn.disconnect()
            self.gs_conn.object.shutdown()
        self.async_loop.call_soon_threadsafe(self.async_loop.stop)

class Events: # use for saving event registration data
    pass

def _registry_event1(client: Client, event_name: str, async_func: AsyncFunc):
     setattr(client.events, event_name, (async_func,))

def _registry_event2(client: Client, event_name: str, async_func: AsyncFunc):
    try:
        efuncs_set: set[AsyncFunc] = getattr(client.events, event_name)
        efuncs_set.add(async_func)

    except AttributeError:
        aset = set(); aset.add(async_func)
        setattr(client.events, event_name, aset)

def _registry_event3(client: Client, event_name: str, async_func: AsyncFunc):
    try:
        efuncs_arr: list[AsyncFunc] = getattr(client.events, event_name)
        efuncs_arr.append(async_func)

    except AttributeError:
        setattr(client.events, event_name, [async_func])

def _unregistry_event1(client: Client, event_name: str, async_func: AsyncFunc):
    efuncs_set: set[AsyncFunc] = getattr(client.events, event_name)
    efuncs_set.remove(async_func)

def _unregistry_event2(client: Client, event_name: str, async_func: AsyncFunc):
    efuncs_set: set[AsyncFunc] = getattr(client.events, event_name)
    efuncs_set.remove(async_func)

def _unregistry_event3(client: Client, event_name: str, async_func: AsyncFunc):
    efuncs_arr: list[AsyncFunc] = getattr(client.events, event_name)
    efuncs_arr.remove(async_func)