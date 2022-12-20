"""Dummy register interface."""

__authors__ = ["Marek Pikuła <marek.pikula at embevity.com>"]

from typing import Dict, Optional

from ..regif import RegisterInterface


class DummyRegIf(RegisterInterface):
    """Example implementation of RegisterInterface.

    It stores the register file in memory as dictionary.
    """

    def __init__(
        self,
        data_width: int,
        address_bounds: Optional[range],
        reset_value: int = 0,
        trace: bool = False,
    ):
        """Initialize the dummy register interface.

        Arguments:
            data_width -- width of data in bits, should be divisible by 8.

        Keyword Arguments:
            address_bounds -- address range, which is allowed by this register
                interface. If not defined, addresses are not validated if they
                are in range.
            reset_value -- default value present in the register on "reset".
            trace -- activate operation tracing (uses `loguru.trace()` under the hood).
        """
        super().__init__(data_width, address_bounds, trace)
        self._values: Dict[int, int] = {}
        self._reset_value = reset_value

    def _get(self, reg_address: int) -> int:
        """Get value from register.

        Arguments:
            reg_address -- absolute register address.

        Returns:
            Register value.
        """
        if reg_address not in self._values:
            return self._reset_value
        return self._values[reg_address]

    def _set(self, reg_address: int, value: int):
        """Set register value.

        Arguments:
            reg_address -- absolute register address.
            value -- value to write to the register.
        """
        self._values[reg_address] = value
