# communication.py

from abc import ABCMeta
import socket

__all__ = [
    "Components",
    "Communication"
]

Socket = socket.socket

class Components(metaclass=ABCMeta):
    """Defines the basic parameters for the communication."""

    HEADER = 64

    ENCODING = 'utf-8'

    __slots__ = ()

    @property
    def encoding(self) -> str:
        """
        Returns the encoding string.

        :return: The encoding string.
        """

        return self.ENCODING
    # end encoding

    @property
    def header(self) -> int:
        """
        Returns the header number.

        :return: The header-number.
        """

        return self.HEADER
    # end header

    @encoding.setter
    def encoding(self, value: str) -> None:
        """
        Sets the encoding value.

        :param value: The encoding value
        """

        try:
            if not isinstance(value, str):
                raise LookupError
            # end if

            "".encode(value)

        except LookupError:
            raise LookupError(f"Unknown encoding: {value}")
        # end try

        Components.ENCODING = value
    # end encoding

    @header.setter
    def header(self, value: int) -> None:
        """
        Sets the header value.

        :param value: The header value
        """

        if not (isinstance(value, str) and value % 2 == 0):
            raise ValueError(f"Invalid header: {value}")
        # end if

        Components.HEADER = value
    # end header
# end Components

class Communication(Components, metaclass=ABCMeta):
    """Defines the base methods for the server and clients communication."""

    SIZE = 1024

    __slots__ = ()

    def send(self, message: bytes, connection: Socket) -> None:
        """
        Sends a message to the client or server by its connection.

        :param message: The message to send to the client.
        :param connection: The sockets' connection object.
        """

        message_len = len(message)

        connection.send(
            (
                str(message_len) + " " *
                (self.HEADER - len(str(message_len)))
            ).encode(self.ENCODING)
        )

        iterations = (
            message_len // self.SIZE + 1 + message_len % self.SIZE
        )

        for i in range(0, iterations, self.SIZE):
            if len(message[i:]) >= self.SIZE:
                connection.send(message[i:self.SIZE])

            else:
                connection.send(message[i:])
            # end if
        # end for
    # end send

    def receive(self, connection: Socket) -> bytes:
        """
        Receive a message from the client or server by its connection.

        :param connection: The sockets' connection object.

        :return: The received message from the server.
        """

        message_len = (
            int(
                connection.recv(self.HEADER).
                decode(self.ENCODING).
                replace(" ", "")
            )
        )

        message = b''

        iterations = (
            message_len // self.SIZE + 1 + message_len % self.SIZE
        )

        for i in range(0, iterations, self.SIZE):
            if (i < iterations - 1) or (message_len % self.SIZE == 0):
                message += connection.recv(self.SIZE)

            else:
                message += connection.recv(message_len % self.SIZE)
            # end if
        # end for

        return message
    # end receive
# end Communication