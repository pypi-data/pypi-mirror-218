# sockets.py

import warnings
import datetime as dt
import socket
import threading
from typing import (
    Optional, Union, Tuple, Dict, Any
)


from represent import represent

from sockets_communication.service import ServiceInterface
from sockets_communication.communication import Communication

__all__ = [
    "SocketServer",
    "ClientsCollection"

]

Socket = socket.socket
Host = str
Port = Union[str, int]
Address = Tuple[Host, Port]
Number = Union[int, float]

@represent
class ClientsCollection:
    """A data class to contain clients within the server data."""

    __slots__ = "clients",

    def __init__(self, clients: Optional[dict] = None) -> None:
        """
        Defines the base data class to contain the clients.

        :param clients: The base dictionary to contain the clients' data.
        """

        if clients is None:
            clients = {}
        # end if

        self.clients = clients
    # end __init__

    # defines a method to set a client
    def set_client(
            self, address: Address, connection: Optional[Socket] = None
    ) -> None:
        """
        Sets or updates clients data in the clients' container .

        :param address: The ip address and port used for the sockets' connection.
        :param connection: The sockets object used for the connection.
        """

        self.clients[address] = connection
    # end add_client

    def get_client(self, address: Address) -> dict:
        """
        Returns the client object inside the data class.

        :param address: The tuple of the ip address and the port of the connection

        :return: The object that represents the client in the dataset.
        """

        return self.clients[address]
    # end get_client

    def pop_client(self, address: Address) -> dict:
        """
        Pops out and returns the client object from the data  class.

        :param address: The tuple of the ip address and the port of the connection

        :return: The object that represents the client in the dataset.
        """

        return self.clients.pop(address)
    # end pop_client

    def remove_client(self, address: Address) -> None:
        """
        Removes the client object from the data class.

        :param address: The tuple of the ip address and the port of the connection
        """

        self.pop_client(address)
    # end remove_client
# end ClientsCollection

class SocketServer(Communication, ServiceInterface):
    """The server object to control the communication ith multiple clients."""

    __slots__ = (
        "connection", "host", "port", "_serving_process",
        "_running_parameters", "_connected", "_serving", "clients"
    )

    def __init__(
            self,
            connection: Optional[Socket] = None, *,
            host: Optional[Host] = None,
            port: Optional[Port] = None
    ) -> None:
        """
        Defines the server datasets for clients and client commands.

        :param connection: The connection socket.
        :param host: The ip address of the server.
        :param port: The port for the server connection.
        """

        ServiceInterface.__init__(self)

        self.connection: Optional[socket.socket] = connection

        self.host: Optional[str] = host
        self.port: Optional[int] = port

        self._serving_process: Optional[threading.Thread] = None

        self._running_parameters: Optional[Dict[str, Any]] = None

        self._connected = False
        self._serving = False

        self.clients = ClientsCollection()
    # end __init__

    def __getstate__(self) -> Dict[str, Any]:
        """
        Gets the state of the object.

        :return: The state of the object.
        """

        data = super().__getstate__()

        data["_running_parameters"] = None

        return data
    # end __getstate__

    @property
    def connected(self) -> bool:
        """
        Checks if the service was built.

        :return: The value for the service being built.
        """

        return self._connected
    # end connected

    @property
    def created(self) -> bool:
        """
        Checks if the service was created.

        :return: The value for the service being created.
        """

        return isinstance(self._serving_process, threading.Thread)
    # end created

    @property
    def serving(self) -> bool:
        """
        Checks if the service is currently serving.

        :return: The boolean value.
        """

        return self._serving
    # end serving

    def validate_connection(self) -> None:
        """Validates the connection object."""

        if not isinstance(self.connection, socket.socket):
            raise ValueError(
                f"Connection object must be {socket.socket}, "
                f"not: {self.connection}."
            )
        # end if
    # end validate_connection

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

        self.connection.bind((host, port))

        self._connected = True
    # end connect

    def respond(self, address: Address, connection: Socket) -> None:
        """
        Sets or updates clients data in the clients' container .

        :param address: The ip address and port used for the sockets' connection.
        :param connection: The sockets object used for the connection.
        """
    # end respond

    def handle(self) -> None:
        """Sends a message to the client by its connection."""

        self.validate_connection()

        connection, address = self.connection.accept()

        self.clients.set_client(address=address, connection=connection)

        self.respond(address=address, connection=connection)

        self.clients.pop_client(address=address)
    # end handle

    def listen(self) -> None:
        """Runs the threads to serving_loop to clients with requests."""

        self.validate_connection()

        self._serving = True

        self.connection.listen()

        while self.serving:
            threading.Thread(target=self.handle).start()
        # end while
    # end listen

    def create(
            self,
            connection: Optional[Socket] = None,
            host: Optional[Host] = None,
            port: Optional[Port] = None,
            daemon: Optional[bool] = True
    ) -> None:
        """
        Creates the process to run the api service.

        :param connection: The connection socket.
        :param host: The host of the server.
        :param port: The port of the server.
        :param daemon: The value to set the process as daemon.
        """

        if not self.connected:
            self.connect(connection=connection, host=host, port=port)
        # end if

        self._serving_process = threading.Thread(
            target=self.listen, daemon=daemon
        )
    # end create

    def start_serving(
            self,
            connection: Optional[Socket] = None,
            host: Optional[Host] = None,
            port: Optional[Port] = None,
            daemon: Optional[bool] = True,
    ) -> None:
        """
        Starts serving to clients.

        :param connection: The connection socket.
        :param host: The host of the server.
        :param port: The port of the server.
        :param daemon: The value to set the process as daemon.
        """

        if self.serving:
            warnings.warn(f"Listening process of {self} is already running.")

            return
        # end if

        if not self.created:
            self.create(
                connection=connection, host=host,
                port=port, daemon=daemon
            )
        # end if

        self._serving_process.start()
    # end start_serving

    def run(
            self,
            connection: Optional[Socket] = None,
            host: Optional[Host] = None,
            port: Optional[Port] = None,
            listen: Optional[bool] = True,
            daemon: Optional[bool] = True,
            update: Optional[bool] = False,
            block: Optional[bool] = False,
            refresh: Optional[Union[Number, dt.timedelta]] = None,
            wait: Optional[Union[Number, dt.timedelta, dt.datetime]] = None,
            timeout: Optional[Union[Number, dt.timedelta, dt.datetime]] = None
    ) -> None:
        """
        Runs the api service.

        :param connection: The connection socket.
        :param host: The host of the server.
        :param port: The port of the server.
        :param listen: The value to start serving_loop.
        :param update: The value to update the service.
        :param daemon: The value to set the process as daemon.
        :param block: The value to block the execution and wain for the service.
        :param wait: The waiting time.
        :param refresh: The value to refresh the service.
        :param timeout: The start_timeout for the process.
        """

        self._running_parameters = dict(
            update=update, refresh=refresh,
            connection=connection, host=host,
            port=port, daemon=daemon, listen=listen,
            timeout=timeout, wait=wait, block=block
        )

        if listen:
            self.start_serving(
                connection=connection, host=host,
                port=port, daemon=daemon
            )
        # end if

        ServiceInterface.run(
            self, update=update, refresh=refresh,
            block=block, wait=wait, timeout=timeout
        )
    # end run

    def rerun(
            self,
            connection: Optional[Socket] = None,
            host: Optional[Host] = None,
            port: Optional[Port] = None,
            listen: Optional[bool] = True,
            daemon: Optional[bool] = True,
            update: Optional[bool] = False,
            block: Optional[bool] = False,
            refresh: Optional[Union[Number, dt.timedelta]] = None,
            wait: Optional[Union[Number, dt.timedelta, dt.datetime]] = None,
            timeout: Optional[Union[Number, dt.timedelta, dt.datetime]] = None
    ) -> None:
        """
        Runs the api service.

        :param connection: The connection socket.
        :param host: The host of the server.
        :param port: The port of the server.
        :param listen: The value to start serving_loop.
        :param update: The value to update the service.
        :param daemon: The value to set the process as daemon.
        :param block: The value to block the execution and wain for the service.
        :param wait: The waiting time.
        :param refresh: The value to refresh the service.
        :param timeout: The start_timeout for the process.
        """

        self.terminate()

        parameters = dict(
            update=update, refresh=refresh,
            connection=connection, host=host,
            port=port, daemon=daemon, listen=listen,
            timeout=timeout, wait=wait, block=block
        )

        parameters = {
            key: value for key, value in parameters.items()
            if value is not None
        }

        self._running_parameters.update(parameters)

        self.run(**self._running_parameters)
    # end rerun

    def stop_serving(self) -> None:
        """Stops the serving process."""

        if self.serving:
            self._serving = False
        # end if

        if self.created and self._serving_process.is_alive():
            self._serving_process = None
        # end if
    # end stop_serving

    def terminate(self) -> None:
        """Pauses the process of service."""

        super().terminate()

        self.stop_serving()
    # end terminate

    def send_message_to_client(self, message: bytes, connection: Socket) -> None:
        """
        Sends a message to the client by its connection.

        :param message: The message to send to the client.
        :param connection: The sockets' connection object.
        """

        return self.send(connection=connection, message=message)
    # end send_message_to_client

    # defines a method to receive a message form hte server
    def receive_message_from_client(self, connection: Socket) -> bytes:
        """
        Receive a message from the client by its connection.

        :param connection: The sockets' connection object.

        :return: The returned data.
        """

        return self.receive(connection=connection)
    # end receive_message_from_client

    def disconnect_client(self, connection: Socket) -> None:
        """
        Disconnects the client from the server through the connection.

        :param connection: The sockets' connection object.
        """

        return self.brute_disconnect_client(connection)
    # end disconnect_client

    # defines a method to receive a message form hte server
    @staticmethod
    def brute_disconnect_client(connection: Socket) -> None:
        """
        Disconnects the client from the server through the connection.

        :param connection: The sockets' connection object.
        """

        return connection.close()
    # end brute_disconnect_client

    def get_client(self, address: Address) -> dict:
        """
        Returns the client object inside the data class.

        :param address: The tuple of the ip address and the port of the connection

        :return: The object that represents the client in the dataset.
        """

        return self.clients.get_client(address)
    # end get_client

    def pop_client(self, address: Address) -> dict:
        """
        Pops out and returns the client object from the data  class.

        :param address: The tuple of the ip address and the port of the connection

        :return: The object that represents the client in the dataset.
        """

        return self.clients.pop_client(address)
    # end pop_client

    def remove_client(self, address: Address) -> None:
        """
        Removes the client object from the data class.

        :param address: The tuple of the ip address and the port of the connection
        """

        self.clients.remove_client(address)
    # end remove_client
# end SocketServer