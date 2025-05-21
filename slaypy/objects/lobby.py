from ..objects.basic import BasicObject
from ..utils.types import original

class Lobby(BasicObject):
    def __init__(self):
        self.ipackets = {
            "gL": ("rooms_list", (109, RoomInfo))
        }

class RoomInfo():
    def __init__(self):
        self.id: int = int
        self.name: str = original
        self.players_amount: int = int
        self.max_players_limit: int = int
        self.mode_id: int = int
        self.map_height: int = int
        self.map_witdh: int = int
        self.tag: str = original
        self.map_thumbnail_data: str = original