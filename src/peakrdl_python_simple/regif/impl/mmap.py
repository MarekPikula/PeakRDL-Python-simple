"""Register interface using `devmem` command."""

__authors__ = ["Marek Pikuła <marek.pikula at embevity.com>"]

import mmap
from pathlib import Path

from ..regif import RegisterInterface


class MmapRegIf(RegisterInterface):
    """Memory mapped register interface.

    Can be for example /dev/mem or /dev/uioX device.
    """

    def __init__(
        self, device: Path, data_width: int, address_bounds: range, trace: bool = False
    ):
        """Initialize the UIO region register interface.

        Arguments:
            device -- UIO device path (e.g., "/dev/uio0").
            data_width -- width of data in bits, should be divisible by 8.
            address_bounds -- address range, which is allowed by this register
                interface. If not defined, addresses are not validated if they
                are in range.

        Keyword Arguments:
            trace -- activate operation tracing (uses `loguru.trace()` under the hood).

        Raises:
            ValueError: raised if sanity check on the arguments doesn't pass.
        """
        super().__init__(data_width, address_bounds, trace)
        self._address_bounds: range = address_bounds
        self._data_bytes = self._data_width // 8
        self._mem_file = open(device, "r+b", 0)  # pylint: disable=consider-using-with
        self._mmap = mmap.mmap(
            self._mem_file.fileno(),
            address_bounds.stop - address_bounds.start,
            mmap.MAP_SHARED,
            mmap.PROT_READ | mmap.PROT_WRITE,
            offset=address_bounds.start,
        )

    def __del__(self):
        """Ensure the mmap is closed."""
        if hasattr(self, "_mmap"):
            self._mmap.close()
        if hasattr(self, "_mem_file"):
            self._mem_file.close()

    def _get(self, reg_address: int) -> int:
        """Get value from register.

        Arguments:
            reg_address -- absolute register address.

        Returns:
            Register value.
        """
        self._mmap.seek(reg_address - self._address_bounds.start)
        return int.from_bytes(self._mmap.read(self._data_bytes), "little")

    def _set(self, reg_address: int, value: int):
        """Set register value.

        Arguments:
            reg_address -- absolute register address.
            value -- value to write to the register.
        """
        self._mmap.seek(reg_address - self._address_bounds.start)
        self._mmap.write(value.to_bytes(self._data_bytes, "little", signed=False))
