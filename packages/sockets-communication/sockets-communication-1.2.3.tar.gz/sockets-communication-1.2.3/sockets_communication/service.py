# service.py

import threading
import warnings
import time
import datetime as dt
from typing import Optional, Union

from represent import represent

Number = Union[int, float]
Host = str
Port = Union[str, int]

__all__ = [
    "ServiceInterface"
]

@represent
class ServiceInterface:
    """The server object to control the communication ith multiple clients."""

    SLEEP = 0.01

    def __init__(self) -> None:
        """Defines the server datasets for clients and client commands."""

        self._timeout_process: Optional[threading.Thread] = None
        self._updating_process: Optional[threading.Thread] = None
        self._refreshing_process: Optional[threading.Thread] = None

        self._blocking = False
        self._updating = False
        self._refreshing = False
    # end __init__

    @property
    def updating(self) -> bool:
        """
        Returns the value of the updating process.

        :return: The updating value.
        """

        return self._updating
    # end updating

    @property
    def blocking(self) -> bool:
        """
        Returns the value of te execution being blocking by the service loop.

        :return: The blocking value.
        """

        return self._blocking
    # end blocking

    @property
    def refreshing(self) -> bool:
        """
        Returns the value of te execution being refreshing by the service loop.

        :return: The refreshing value.
        """

        return self._refreshing
    # end refreshing

    def update(self) -> None:
        """Updates the options according to the screeners."""
    # end update

    def refresh(self) -> None:
        """Updates the options according to the screeners."""
    # end update

    def refreshing_loop(self, refresh: Union[Number, dt.timedelta]) -> None:
        """
        Updates the options according to the screeners.

        :param refresh: The value to refresh the service.
        """

        self._refreshing = True

        if isinstance(refresh, dt.timedelta):
            refresh = refresh.total_seconds()
        # end if

        start = time.time()

        while self.updating:
            current = time.time()

            if (current - start) >= refresh:
                start = current

                self.refresh()
            # end if

            time.sleep(self.SLEEP)
        # end while
    # end update_loop

    def updating_loop(self) -> None:
        """Updates the options according to the screeners."""

        self._updating = True

        while self.updating:
            self.update()

            time.sleep(self.SLEEP)
        # end while
    # end updating_loop

    def blocking_loop(self) -> None:
        """Updates the options according to the screeners."""

        self._blocking = True

        while self.blocking:
            time.sleep(self.SLEEP)
        # end while
    # end blocking_loop

    def start_updating(self) -> None:
        """Starts the updating process."""

        if self.updating:
            warnings.warn(f"Updating process of {self} is already running.")

            return
        # end if

        self._updating_process = threading.Thread(
            target=self.updating_loop
        )

        self._updating_process.start()
    # end start_updating

    def start_refreshing(self, refresh: Union[Number, dt.timedelta]) -> None:
        """
        Starts the refreshing process.

        :param refresh: The value to refresh the service.
        """

        if self.refreshing:
            warnings.warn(f"Refreshing process of {self} is already running.")

            return
        # end if

        self._refreshing_process = threading.Thread(
            target=lambda: self.refreshing_loop(refresh)
        )

        self._refreshing_process.start()
    # end start_refreshing

    def start_blocking(self) -> None:
        """Starts the blocking process."""

        if self.blocking:
            warnings.warn(f"Blocking process of {self} is already running.")

            return
        # end if

        self.blocking_loop()
    # end start_blocking

    @staticmethod
    def start_waiting(
            wait: Union[Number, dt.timedelta, dt.datetime]
    ) -> None:
        """
        Runs a waiting for the process.

        :param wait: The duration of the start_timeout.

        :return: The start_timeout process.
        """

        if isinstance(wait, dt.datetime):
            wait = wait - dt.datetime.now()
        # end if

        if isinstance(wait, dt.timedelta):
            wait = wait.total_seconds()
        # end if

        if isinstance(wait, (int, float)):
            time.sleep(wait)
        # end if
    # end start_waiting

    def run(
            self,
            update: Optional[bool] = True,
            block: Optional[bool] = False,
            refresh: Optional[Union[Number, dt.timedelta]] = None,
            wait: Optional[Union[Number, dt.timedelta, dt.datetime]] = None,
            timeout: Optional[Union[Number, dt.timedelta, dt.datetime]] = None,
    ) -> None:
        """
        Runs the api service.

        :param update: The value to update the service.
        :param block: The value to block the execution and wain for the service.
        :param refresh: The value to refresh the service.
        :param wait: The waiting time.
        :param timeout: The start_timeout for the process.
        """

        if update:
            self.start_updating()
        # end if

        if refresh:
            self.start_refreshing(refresh)
        # end if

        if timeout:
            self.start_timeout(timeout)
        # end if

        if wait:
            self.start_waiting(wait)
        # end if

        if block:
            self.start_blocking()
        # end if
    # end run

    def start_timeout(
            self,
            duration: Union[Number, dt.timedelta, dt.datetime]
    ) -> None:
        """
        Waits to terminate the process.

        :param duration: The amount of seconds to wait before termination.
        """

        if isinstance(duration, dt.datetime):
            duration = duration - dt.datetime.now()
        # end if

        if isinstance(duration, dt.timedelta):
            duration = duration.total_seconds()
        # end if

        self._timeout_process = threading.Thread(
            target=lambda: (time.sleep(duration), self.terminate())
        )

        self._timeout_process.start()
    # end start_timeout

    def stop_blocking(self) -> None:
        """Stops the blocking process."""

        self._blocking = False
    # end stop_blocking

    def stop_updating(self) -> None:
        """Stops the updating process."""

        if self.updating:
            self._updating = False
        # end if

        if (
            isinstance(self._updating_process, threading.Thread) and
            self._updating_process.is_alive()
        ):
            self._updating_process = None
        # end if
    # end stop_updating

    def stop_refreshing(self) -> None:
        """Stops the refreshing process."""

        if self.refreshing:
            self._refreshing = False
        # end if

        if (
            isinstance(self._refreshing_process, threading.Thread) and
            self._refreshing_process.is_alive()
        ):
            self._refreshing_process = None
        # end if
    # end stop_refreshing

    def terminate(self) -> None:
        """Pauses the process of service."""

        self.stop_blocking()
        self.stop_updating()
        self.stop_refreshing()
    # end terminate
# end ServiceInterface