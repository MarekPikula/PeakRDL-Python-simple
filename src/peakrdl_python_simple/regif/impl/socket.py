"""Register interface using custom socket protocol over a remote connection."""

__authors__ = ["Marek Pikuła <marek.pikula at embevity.com>"]

from dataclasses import dataclass
from enum import Enum
from multiprocessing.connection import Client, Listener
from pickle import PickleError
from threading import Lock
from typing import Any, Optional, Tuple

try:
    from loguru import logger

    LOGURU_ENABLED = True
except ImportError:
    LOGURU_ENABLED = False  # type: ignore

from ..regif import RegisterInterface

PROTOCOL_VERSION: int = 1
"""Current version of the SocketRegIf protocol.

Used to ensure compatibility between client and server.
"""


@dataclass
class SocketRegIfPacket:
    """Socket register interface packet."""

    class Operation(Enum):
        """Operation to be performed."""

        GET = 0
        SET = 1

    class Status(Enum):
        """Status of the curent packet."""

        REQUEST = 0
        RESPONSE_OK = 1
        RESPONSE_ERROR = 2

    protocol_version: int
    """Protocol version.

    Used to check compatibility between client and server.
    """

    operation: Tuple[Operation, int]
    """Operation in form of (Operation, Operation ID) pair."""

    status: Tuple[Status, Optional[str]]
    """Status of the request in for of (Status, optional status string) pair."""

    reg_address: int
    """Register address to be accessed."""

    value: Optional[int]
    """Register value for the set operation or return value from get operation."""


class SocketRegIfServer:  # pylint: disable=too-few-public-methods
    """Socket register interface server.

    Supposed to be running on the hardware side.
    """

    def __init__(self, regif: RegisterInterface):
        """Initialize the socket regif.

        Arguments:
            regif -- register interface with access to be published via the socket.
        """
        self._regif = regif

    def serve(self, socket_tuple: Tuple[str, int]):
        """Start the socket server.

        Arguments:
            socket_tuple -- host, port number pair.
        """
        with Listener(socket_tuple) as listener:
            if LOGURU_ENABLED:
                logger.info("Listening at {addr[0]}:{addr[1]}.", addr=listener.address)
            while True:
                self._accept_connection(listener)

    def _accept_connection(self, listener: Listener):
        """Accept connection and process requests."""
        with listener.accept() as connection:
            assert (
                listener.last_accepted is not None
            ), "Something's wrong. We have just accepted a connection."
            if LOGURU_ENABLED:
                logger.info(
                    "Connection accepted from {acc[0]}:{acc[1]}.",
                    acc=listener.last_accepted,
                )
            while not connection.closed:
                # Process packets until the connection is closed.
                try:
                    connection.send(self._process_packet(connection.recv()))
                except EOFError:
                    # Raised when connection is closed by the client during `recv()`.
                    connection.close()
                    break
        if LOGURU_ENABLED:
            logger.info("Connection closed.")

    def _process_packet(self, data: SocketRegIfPacket) -> SocketRegIfPacket:
        """Process a packet and return a response.

        If any error occurs during the packet processing, the exception string is passed as an
        response error with the exception message passed as the optional response string.

        Arguments:
            data -- request packet.

        Returns:
            Response packet.
        """
        try:
            if data.protocol_version != PROTOCOL_VERSION:
                raise RuntimeError(
                    f"Unsupported protocol version: {data.protocol_version}."
                )
            if data.status[0] != SocketRegIfPacket.Status.REQUEST:
                raise RuntimeError(
                    f"Server can handle only requests. Got {data.status}."
                )

            if data.operation[0] == SocketRegIfPacket.Operation.GET:
                data.value = self._regif.get(data.reg_address)
                data.status = (SocketRegIfPacket.Status.RESPONSE_OK, None)
            elif data.operation[0] == SocketRegIfPacket.Operation.SET:
                if data.value is None:
                    raise RuntimeError(
                        f"SET request for address 0x{data.reg_address:X} failed. No value provided."
                    )
                self._regif.set(data.reg_address, data.value)
                data.status = (SocketRegIfPacket.Status.RESPONSE_OK, None)
            else:
                raise NotImplementedError(
                    f'Operation "{data.operation}" not supported.'
                )
        except Exception as exc:  # pylint: disable=broad-except
            # Exception occured either during validation of the packet or during register access.
            data.protocol_version = PROTOCOL_VERSION
            data.status = (SocketRegIfPacket.Status.RESPONSE_ERROR, str(exc))
        return data


class SocketRegIfClient(RegisterInterface):
    """Socket register interface client.

    Supposed to be running on the controller side.
    """

    def __init__(
        self,
        socket_tuple: Tuple[str, int],
        data_width: int,
        address_bounds: Optional[range] = None,
        trace: bool = False,
    ):
        """Initialize the socket register interface client.

        Arguments:
            socket_tuple -- server socket tuple in form of (address, port).
            data_width -- width of data in bits, should be divisible by 8.
            address_bounds -- address range, which is allowed by this register
                interface. If not defined, addresses are not validated if they
                are in range.

        Keyword Arguments:
            trace -- activate operation tracing (uses `loguru.trace()` under the hood).
        """
        super().__init__(data_width, address_bounds, trace)

        self._conn = Client(socket_tuple)
        if LOGURU_ENABLED:
            logger.info("Connected to {conn[0]}:{conn[1]}", conn=socket_tuple)

        self._operation_id = 0
        self._operation_lock = Lock()

    @staticmethod
    def _check_response(request: SocketRegIfPacket, response: Any) -> SocketRegIfPacket:
        """Verify whether the response is valid.

        Raises RuntimeError for every invalidity. Returns the validated response.
        """
        if not isinstance(response, SocketRegIfPacket):
            raise RuntimeError(
                "The response is of an unexpected type. "
                f"Requested SocketRegIfPacket, got {type(response)}."
            )

        if response.protocol_version != PROTOCOL_VERSION:
            raise RuntimeError(
                f"Wrong protocol version in response: {response.protocol_version}"
            )

        if request.operation != response.operation:
            raise RuntimeError(
                "Response for wrong operation. "
                f"Requested {request.operation}, got {response.operation}"
            )

        if response.status[0] != SocketRegIfPacket.Status.RESPONSE_OK:
            raise RuntimeError(f"Response error: {response.status}")

        return response

    def _get(self, reg_address: int) -> int:
        """Read register value over the socket.

        Arguments:
            reg_address -- absolute address of register to read.

        Returns:
            Data from the register.
        """
        with self._operation_lock:
            try:
                request = SocketRegIfPacket(
                    PROTOCOL_VERSION,
                    (SocketRegIfPacket.Operation.GET, self._operation_id),
                    (SocketRegIfPacket.Status.REQUEST, None),
                    reg_address,
                    None,
                )
                self._conn.send(request)
                self._operation_id += 1

                response = self._check_response(request, self._conn.recv())
                if response.value is None:
                    raise RuntimeError("Get response doesn't have a value.")
                return response.value
            except PickleError as exc:
                raise RuntimeError(
                    f"Failed to execute socket get command for register 0x{reg_address:X}."
                ) from exc

    def _set(self, reg_address: int, value: int) -> None:
        """Write register over socket.

        Arguments:
            reg_address -- absolute address of register to write to.
            value -- value to write to the register.
        """
        with self._operation_lock:
            try:
                request = SocketRegIfPacket(
                    PROTOCOL_VERSION,
                    (SocketRegIfPacket.Operation.SET, self._operation_id),
                    (SocketRegIfPacket.Status.REQUEST, None),
                    reg_address,
                    value,
                )
                self._conn.send(request)
                self._operation_id += 1

                self._check_response(request, self._conn.recv())
            except PickleError as exc:
                raise RuntimeError(
                    "Failed to execute socket set command "
                    f"for register 0x{reg_address:X} = 0x{value:X}."
                ) from exc
