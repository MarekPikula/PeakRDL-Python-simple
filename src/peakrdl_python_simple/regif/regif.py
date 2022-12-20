"""Register interface abstraction."""

__authors__ = ["Marek Pikuła <marek.pikula at embevity.com>"]

import sys
from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Optional

try:
    from loguru import logger

    LOGURU_ACTIVE = True
except ImportError:
    LOGURU_ACTIVE = False  # type: ignore


class RegisterInterface(ABC):
    """Register interface abstraction.

    A basic register interface requires overriding `get()` and `set()`
    functions, depending on underlying hardware configuration.

    Example implementation can be found in the `impl` submodule.
    """

    def __init__(
        self,
        data_width: int,
        address_bounds: Optional[range] = None,
        trace: bool = False,
    ):
        """Initialize register interface abstraction.

        Arguments:
            data_width -- width of data in bits, should be divisible by 8.

        Keyword Arguments:
            address_bounds -- address range, which is allowed by this register
                interface. If not defined, addresses are not validated if they
                are in range.
            trace -- activate operation tracing (uses `loguru.trace()` under the hood).

        Raises:
            ValueError: raised if sanity check on the arguments doesn't pass.
        """
        if LOGURU_ACTIVE:
            if address_bounds is None:
                logger.info(
                    "Initializing register interface with {} bit data width.",
                    data_width,
                )
            else:
                logger.info(
                    "Initializing register interface for region:"
                    " 0x{:X}-0x{:X} with {} bit data width.",
                    address_bounds.start,
                    address_bounds.stop,
                    data_width,
                )

        if not 64 >= data_width > 0:
            raise ValueError("Unsupported register width.")
        if data_width % 8 != 0:
            raise ValueError("Data width should be divisible by 8 (a byte).")
        if address_bounds is not None:
            if address_bounds.start < 0:
                raise ValueError("Address bounds need to be positive.")
            if address_bounds.start > address_bounds.stop:
                raise ValueError("Address bounds need to be incremental.")

        self._data_width = data_width
        self._address_bounds = address_bounds

        self._trace_active = False
        self.tracing_enabled = trace

    @property
    def tracing_enabled(self) -> bool:
        """Check if the register operation tracing is enabled."""
        return self._trace_active

    @tracing_enabled.setter
    def tracing_enabled(self, trace: bool) -> None:
        if trace and not LOGURU_ACTIVE:
            print(
                "Tracing was requested for regif, but loguru is not installed.",
                file=sys.stderr,
            )
        self._trace_active = trace and LOGURU_ACTIVE

    def _sanitize_field_args(
        self,
        reg_address: int,
        field_pos: Optional[int] = None,
        field_width: Optional[int] = None,
        value: Optional[int] = None,
    ):
        """General argument sanitizer used both for register and field access.

        It's assumed that it's field if `field_pos` and `field_width_bits` are
        defined.

        Arguments:
            reg_address -- register address.

        Keyword Arguments:
            field_pos -- field position.
            field_width -- field width in bits.
            value -- value of register or field.

        Raises:
            ValueError: some inconsistency has been found.
        """
        if reg_address < 0:
            raise ValueError(f"Register address {reg_address} should be positive.")

        if self._address_bounds is not None and reg_address not in self._address_bounds:
            raise ValueError(
                f"Register address 0x{reg_address:X} not in register interface allowed range."
            )

        if field_pos is not None and field_pos < 0:
            raise ValueError(f"Field position ({field_pos}) should be positive.")

        if field_width is not None and field_width > self.data_width:
            raise ValueError(
                f"Field width ({field_width}) should not be bigger than"
                f"register width ({self.data_width})."
            )

        # If field use field_width otherwise use register data_width.
        bits = (
            field_width
            if field_pos is not None and field_width is not None
            else self.data_width
        )
        if value is not None and value & ((1 << bits) - 1) != value:
            raise ValueError(
                f"Register/field value (0x{value:X}) wider than "
                f"register/field width ({bits})."
            )

    class _Operation(Enum):
        """Register operation enum.

        Used for tracing.
        """

        GET = auto()
        SET = auto()

        def get_arrow(self) -> str:
            """Get an arrow representation of the operation."""
            if self == self.GET:
                return "->"
            if self == self.SET:
                return "<-"
            raise NotImplementedError("Unknown operation direction.")

    def _trace_field(  # pylint: disable=too-many-arguments
        self,
        operation: _Operation,
        reg_address: int,
        value: int,
        field_pos: int,
        field_width: int,
    ):
        """Add logger trace for the field operation."""
        if self._trace_active:
            logger.trace(
                "regif: 0x{:X}[{:2}:{:2}] {} 0x{:X}",
                reg_address,
                field_pos + field_width - 1,
                field_pos,
                operation.get_arrow(),
                value,
            )

    @property
    def data_width(self):
        """Get register data width."""
        return self._data_width

    @property
    def address_bounds(self) -> Optional[range]:
        """Get address bounds of this register interface."""
        return self._address_bounds

    @abstractmethod
    def get(self, reg_address: int) -> int:
        """Read register value abstraction.

        `super().get(reg_address)` should be called to validate aruments.

        Arguments:
            reg_address -- absolute address of register to read.

        Returns:
            Data from the register.
        """
        self._sanitize_field_args(reg_address)
        return 0

    @abstractmethod
    def set(self, reg_address: int, value: int) -> None:
        """Write register value abstraction.

        `super().set(reg_address, value)` should be called to validate aruments.

        Arguments:
            reg_address -- absolute address of register to write to.
            value -- value to write to the register.
        """
        self._sanitize_field_args(reg_address, value=value)

    def get_field(self, reg_address: int, field_pos: int, field_width: int) -> int:
        """Read register field abstraction.

        It sanitized arguments to ensure nothing is out of bounds.

        The default implementation can be overloaded, but
        `_sanitize_field_args()` should be called in the
        overloaded implementation.

        Arguments:
            reg_address -- absolute address of register to write to.
            field_pos -- field position in the register (counting from LSB).
            field_width -- width of the field in bits.

        Returns:
            Value in given field in given register.
        """
        self._sanitize_field_args(reg_address, field_pos, field_width)
        ret = (self.get(reg_address) >> field_pos) & ((1 << field_width) - 1)
        self._trace_field(self._Operation.GET, reg_address, ret, field_pos, field_width)
        return ret

    def set_field(  # pylint: disable=too-many-arguments
        self,
        reg_address: int,
        field_pos: int,
        field_width: int,
        value: int,
        ignore_other_fields: bool = False,
    ) -> None:
        """Write register field abstraction.

        It sanitized arguments to ensure nothing is out of bounds.

        The default implementation can be overloaded, but
        `_sanitize_field_args()` should be called in the
        overloaded implementation.

        Arguments:
            reg_address -- absolute address of register to write to.
            field_pos -- field position in the register (counting from LSB).
            field_width -- width of the field in bits.
            value -- new value of the field.

        Keyword Arguments:
            ignore_other_fields -- if set to True, other fields current values are ignored.
        """
        self._sanitize_field_args(reg_address, field_pos, field_width, value)

        field_negative_mask = ((1 << self.data_width) - 1) ^ (
            ((1 << field_width) - 1) << field_pos
        )
        prev_reg_value = (
            0
            if ignore_other_fields
            else self.get_field(reg_address, 0, self.data_width) & field_negative_mask
        )
        self._trace_field(
            self._Operation.SET, reg_address, value, field_pos, field_width
        )
        self.set(reg_address, prev_reg_value | (value << field_pos))
