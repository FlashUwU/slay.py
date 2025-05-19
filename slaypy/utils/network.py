from typing import Literal

from ping3 import ping

from ..core.socket import SocketEnum

def find_nearest_socket(type: Literal["Gaming", "Friends"], timeout=4) -> SocketEnum | None:
    nearest_socket = None
    nearest_latency = None

    for socket in SocketEnum:
        if socket.type != type: continue

        latency = ping(socket.ip_addr, timeout)
        if not latency: continue

        if nearest_socket:
            if latency < nearest_latency:
                nearest_socket = socket
                nearest_latency = latency
        else:
            nearest_socket = socket
            nearest_latency = latency

    return nearest_socket