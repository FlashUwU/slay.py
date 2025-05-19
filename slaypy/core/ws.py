from websocket import WebSocketApp
from typing import Type

from .socket import Socket
from ..objects import map as objects_map
from ..objects.basic import BasicObject

sid = 0

class Connection():
    def __init__(self, socket: Socket, trigger_event):
        global sid

        self.sid = sid = sid + 1
        
        self.socket = socket
        self.trigger_event = trigger_event

        self.object: Type[BasicObject] = None

        self.ws = WebSocketApp(
            f"wss://{self.socket.ip_addr}:{self.socket.port}",
            on_open=self.on_connect,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_disconnect
        )

    def send_message(self, message: str):
        self.ws.send(message)

    def connect(self):
        self.ws.run_forever(sslopt={"cert_reqs": 0})
    
    def disconnect(self):
        if self.ws.sock and self.ws.sock.connected:
            self.ws.close()

    def on_connect(self, ws: WebSocketApp):
        print(f"[{self.sid}] Connected to slayone server {self.socket.name if self.socket.name else (self.socket.ip_addr, self.socket.port)}.")

        self.trigger_event("open")

    def on_message(self, ws: WebSocketApp, message: str):
        print(f"[{self.sid}] Received Message: {message}")
        self.object.process_message(message)

        self.trigger_event("message")
    
    def on_error(self, ws: WebSocketApp, err: Exception):
        if not str(err): return

        print(f"[{self.sid}] Error: {err}")

        self.trigger_event("error")
    
    def on_disconnect(self, ws: WebSocketApp, code: int, message: str):
        print(f"[{self.sid}] Disconnected to slayone server {self.socket.name if self.socket.name else (self.socket.ip_addr, self.socket.port)} (code: {code}, message: {message}).")

        self.trigger_event("_close")
        self.trigger_event("close")
    
    @staticmethod
    def from_client(client, socket: Socket, settings): # establish a bridge between basic things and models.
        conn = Connection(socket, client.trigger_event)

        conn.trigger_event = client.trigger_event
        conn.object = BasicObject(init_ipackets=False).setup(client)


        for object_name in settings.objects:
            if "basic":
                conn.object += BasicObject()
                continue

            conn.object += objects_map[object_name]()

        for event_name in settings.disable_events:
            conn.object.ipackets.pop(event_name, None)

        return conn