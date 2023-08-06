# bluetooth.py

import socket

__all__ = [
    "bluetooth_socket"
]

def bluetooth_socket() -> socket.socket:
    """
    Sends a request through the bluetooth sockets.

    :return: The client object..
    """

    return socket.socket(
        socket.AF_BLUETOOTH, socket.SOCK_STREAM,
        socket.BTPROTO_RFCOMM
    )
# end bluetooth_socket