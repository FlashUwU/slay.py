import json
from concurrent.futures import ThreadPoolExecutor
from typing import Type, Callable

from ..utils.types import original


DELIMITER1 = "$"
DELIMITER2 = "%split%"

class BasicObject():
    client = None; executor = None; ipackets = {}

    def __init__(self, init_ipackets: bool = True):
        if not init_ipackets: return

        self.ipackets: dict[str, tuple[Callable | list[Callable], tuple[str, int]]] = {
            "i_d": ("id", (1,)), # id
            "svrMsg": ("server_message", (0, 2, 0)), # type, duration, content
            "logged": ("logged", ((10, Player), 1)) # player data, ranked search number
        }
    
    def setup(self, client, thread_pool_executor: bool = True):
        self.client = client
        self.executor =  ThreadPoolExecutor(max_workers=1) if thread_pool_executor else None

        return self
    
    def shutdown(self):
        if self.executor:
            self.executor.shutdown(wait=True)
    
    def process_message(self, message: str):
        if self.executor: self.executor.submit(self._process_message, message)
        else: self._process_message(message)

    def _process_message(self, message: str):
        ipacket_array = message.split(DELIMITER1)
        event_name, ipacket_ref = x if (x := self.ipackets.get(ipacket_array[0])) else (None, None)

        if not ipacket_ref or not event_name: return

        is_list_data = False
        if isinstance(x:=ipacket_ref[0], int) and x > 99:
            x -= 100
            repeated_times = (len(ipacket_array)-1)//x
            ipacket_ref = ipacket_ref[1:]
            is_list_data = True

        args_arr = []
        while repeated_times:
            args = []; index = 0

            for pattern in ipacket_ref:
                index += 1; need_assign = False

                if isinstance(pattern, type):
                    obj: type = pattern()

                    for attr, vtype in obj.__dict__.items():
                        obj.__dict__[attr] = vtype(ipacket_array[index])
                        index += 1
                    
                    args.append(obj)
                    index -= 1; continue

                try: vtype = pattern[0]
                except: vtype = pattern

                if vtype > 9:
                    need_assign = True
                    vtype = vtype - 10

                if vtype == 0: vtype = original
                elif vtype == 1: vtype = int
                elif vtype == 2: vtype = float
                elif vtype == 3: vtype = json.loads

                if isinstance(pattern, int):
                    args.append(vtype(ipacket_array[index])); continue

                if len(pattern) == 3:
                    index += pattern[2]

                if isinstance(pattern[1], type):
                    obj: type = pattern[1]()

                    for attr, vtype2 in obj.__dict__.items():
                        value = ipacket_array[index]

                        obj.__dict__[attr] = vtype2(value)

                        index += 1
                    
                    obj = vtype(obj)

                    if need_assign: setattr(self.client, obj.__class__.__name__.lower(), obj)
                    else: args.append(obj)

                    index -= 1; continue
                
                if isinstance(pattern, tuple):
                    value = ipacket_array[index]

                    if need_assign: setattr(self.client, pattern[1], vtype(value))

                    continue
            
            args_arr.append(args)
            repeated_times -= 1

        if is_list_data:
            self.client.trigger_event(event_name, *args_arr)
        else:
            self.client.trigger_event(event_name, *args_arr[0])

    def __add__(self, object: Type["BasicObject"]):
        if not isinstance(object, BasicObject):
            raise TypeError

        self.ipackets.update(object.ipackets)

        object.shutdown()

        return self

class Player:
    def __init__(self):
        self.name: str = original
        self.skin_id: int = int
        self._abilities: list[dict[str, int | list[int]]] = json.loads
        self.golds: int = int
        self.gems: int = int
        self.xp: int = int
        self.is_mod: bool = bool
        self.is_mod2: bool = bool
        self.is_admin: bool = bool
        self.name_color_id: int = int
        self._unlocked_skins: str = original
        self.clan_tag: str = original
        self.clan_role: int = int
        self._chests: str = original
        self.db_id: int = int
        self._unlocked_colours: str = original
        self.unlocked_emote_ids: list[int] = json.loads
        self._kills_of_weapons: list[int] = json.loads