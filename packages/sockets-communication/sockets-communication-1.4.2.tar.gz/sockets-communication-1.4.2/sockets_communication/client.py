# client.py

import socket
from typing import Optional, Union, Any, Dict

from requests.models import PreparedRequest

from represent import represent

from sockets_communication.bluetooth import bluetooth_socket
from sockets_communication.process import decode
from sockets_communication.communication import Communication

__all__ = [
    "SocketClient",
    "socket_request",
    "bluetooth_socket_request"
]

Socket = socket.socket
Host = str
Port = Union[str, int]

@represent
class SocketClient(Communication):
    """Creates the client to communicate with the server."""

    __slots__ = "connection", "host", "port"

    def __init__(
            self,
            connection: Optional[Socket] = None, *,
            host: Optional[Host] = None,
            port: Optional[Port] = None
    ) -> None:
        """
        Defines the server address and creates the client object.

        :param connection: The connection socket.
        :param host: The ip address of the server.
        :param port: The port for the server connection.
        """

        self.connection: Optional[Socket] = connection

        self.host: Optional[str] = host
        self.port: Optional[int] = port
    # end __init__

    def validate_connection(self) -> None:
        """Validates the connection object."""

        if not isinstance(self.connection, socket.socket):
            raise ValueError(
                f"Connection object must be {socket.socket}, "
                f"not: {self.connection}."
            )
        # end if
    # end validate_connection

    def send(self, message: bytes, connection: Optional[Socket] = None) -> None:
        """
        Sends a message to the client or server by its connection.

        :param message: The message to send to the client.
        :param connection: The sockets' connection object.
        """

        if connection is None:
            self.validate_connection()

            connection = self.connection
        # end if

        super().send(message=message, connection=connection)
    # end send

    def receive(self, connection: Optional[Socket] = None) -> bytes:
        """
        Receive a message from the client or server by its connection.

        :param connection: The sockets' connection object.

        :return: The received message from the server.
        """

        if connection is None:
            self.validate_connection()

            connection = self.connection
        # end if

        return super().receive(connection=connection)
    # end receive

    def connect(
            self,
            connection: Optional[Socket] = None, *,
            host: Optional[Host] = None,
            port: Optional[Port] = None
    ) -> None:
        """
        Creates the sockets' connection for the client object with the server.

        :param connection: The connection socket.
        :param host: The ip address of the server.
        :param port: The port for the server connection.
        """

        if connection is not None:
            self.connection = connection
        # end if

        if host is not None:
            self.host = host
        # end if

        if port is not None:
            self.port = port
        # end if

        self.validate_connection()

        self.connection.connect((self.host, self.port))
    # end connect

    def send_message_to_server(self, message: bytes) -> None:
        """
        Sends a message to the server through the sockets' connection.

        :param message: The message to send to the server.
        """

        return self.send(connection=self.connection, message=message)
    # end send_message_to_server

    # defines a method to receive a message form hte server
    def receive_message_from_server(self) -> bytes:
        """
        Gets the received message from the server.

        :return: The received response from the server.
        """

        return self.receive(connection=self.connection)
    # end receive_message_from_server
# end SocketClient

def socket_request(
        connection: Optional[Socket], *,
        host: Host,
        port: Port,
        endpoint: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None
) -> Any:
    """
    Sends a request through the bluetooth sockets.

    :param connection: The connection object.
    :param host: The request host.
    :param endpoint: The path to the endpoint.
    :param port: The sending port.
    :param parameters: The request parameters.

    :return: The returned value.
    """

    client = SocketClient()

    client.connect(connection=connection, host=host, port=port)

    req = PreparedRequest()
    # noinspection HttpUrlsUsage
    req.prepare_url(
        f"http://{host}:{port}/{endpoint or ''}",
        parameters or {}
    )

    client.send(message=req.url.encode())
    content = client.receive()

    client.connection.close()

    return decode(content.decode())
# end socket_request

def bluetooth_socket_request(
        host: Host,
        port: Port,
        endpoint: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None
) -> Any:
    """
    Sends a request through the bluetooth sockets.

    :param host: The request host.
    :param endpoint: The path to the endpoint.
    :param port: The sending port.
    :param parameters: The request parameters.

    :return: The returned value.
    """

    return socket_request(
        connection=bluetooth_socket(), host=host,
        port=port, endpoint=endpoint, parameters=parameters
    )
# end bluetooth_socket_request