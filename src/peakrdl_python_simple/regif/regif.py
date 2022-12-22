"""Register interface abstraction."""

__authors__ = ["Marek Pikuła <marek.pikula at embevity.com>"]

import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass
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

    @dataclass(frozen=True)
    class _FieldSpec:
        """Field specification used for internal functions."""

        pos: int
        """Field position in bits (bit shift value)."""

        width: int
        """Field width in bits."""

        data_width: int
        """Data width of the register interface."""

        def __post_init__(self):
            if not 0 <= self.pos < self.data_width:
                raise ValueError(
                    f"Field position ({self.pos}) should be positive and within the data width."
                )

            if not 0 < self.width <= self.data_width:
                raise ValueError(
                    f"Field width ({self.width}) should not be bigger than"
                    f"register width ({self.data_width}) but at least 1."
                )

    def _sanitize_field_args(
        self,
        reg_address: int,
        field: Optional[_FieldSpec] = None,
        value: Optional[int] = None,
    ):
        """General argument sanitizer used both for register and field access.

        It's assumed that it's field if `field_pos` and `field_width_bits` are
        defined.

        Arguments:
            reg_address -- register address.

        Keyword Arguments:
            field -- field specification.
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

        # If field use field_width otherwise use register data_width.
        bits = field.width if field is not None else self.data_width
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

    def _trace(
        self,
        operation: _Operation,
        reg_address: int,
        value: int,
        field: Optional[_FieldSpec] = None,
    ):
        """Add logger trace for the field operation."""
        if self._trace_active:
            logger.trace(
                "regif: 0x{:X}{:7} {} 0x{:X}",
                reg_address,
                "" if field is None else f"[{field.pos + field.width - 1}:{field.pos}]",
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
    def _get(self, reg_address: int) -> int:
        """Read register value abstraction."""
        return 0

    @abstractmethod
    def _set(self, reg_address: int, value: int) -> None:
        """Write register value abstraction."""

    def get(self, reg_address: int) -> int:
        """Read register value abstraction.

        Arguments:
            reg_address -- absolute address of register to read.

        Returns:
            Data from the register.
        """
        self._sanitize_field_args(reg_address)
        ret = self._get(reg_address)
        self._trace(self._Operation.GET, reg_address, ret)
        return ret

    def set(self, reg_address: int, value: int) -> None:
        """Write register value abstraction.

        Arguments:
            reg_address -- absolute address of register to write to.
            value -- value to write to the register.
        """
        self._sanitize_field_args(reg_address, value=value)
        self._trace(self._Operation.SET, reg_address, value)
        self._set(reg_address, value)

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
        field = self._FieldSpec(field_pos, field_width, self.data_width)
        self._sanitize_field_args(reg_address, field)

        ret = (self.get(reg_address) >> field_pos) & ((1 << field_width) - 1)
        self._trace(self._Operation.GET, reg_address, ret, field)
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
        field = self._FieldSpec(field_pos, field_width, self.data_width)
        self._sanitize_field_args(reg_address, field, value)

        field_negative_mask = ((1 << self.data_width) - 1) ^ (
            ((1 << field_width) - 1) << field_pos
        )
        prev_reg_value = (
            0 if ignore_other_fields else self.get(reg_address) & field_negative_mask
        )
        self._trace(self._Operation.SET, reg_address, value, field)
        self.set(reg_address, prev_reg_value | (value << field_pos))
