from enum import Enum

class Socket(Enum):
    """ Slayone Server Socket. """

    FS = ("54.37.204.175", 62202, 1)
    EU = ("54.37.204.175", 62203, 0)
    NA = ("51.79.86.227", 62203, 0)
    ASIA = ("51.79.251.73", 62203, 0)

    @property
    def ip_addr(self) -> str:
        return self.value[0]

    @property
    def port(self) -> str:
        return self.value[1]
    
    @property
    def type(self) -> str:
        value = self.value[2]

        if value == 0: return "Gaming"
        elif value == 1: return "Friends"

    def __str__(self) -> str:
        if self.name == "FS": return "Friends Server"
        return self.name