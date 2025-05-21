from ..modules.basic import BasicOperator

class LobbyOperator(BasicOperator):
    def __init__(self, send_message):
        self._send_messsage = send_message
        self._opackets = {
            "request_rooms_list": "req-games-list"
        }
    
    def request_rooms_list(self): pass