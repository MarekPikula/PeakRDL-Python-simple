"""Register interface using `devmem` command."""

__authors__ = ["Marek Pikuła <marek.pikula at embevity.com>"]

import subprocess
from typing import List, Optional, Union

from ..regif import RegisterInterface


class DevmemRegIf(RegisterInterface):
    """Register interface using `devmem` command."""

    def __init__(
        self,
        data_width: int,
        address_bounds: Optional[range] = None,
        devmem_command: Union[str, List[str]] = "devmem",
        trace: bool = False,
    ):
        """Initialize the UIO region register interface.

        Arguments:
            data_width -- width of data in bits, should be divisible by 8.
            address_bounds -- address range, which is allowed by this register
                interface. If not defined, addresses are not validated if they
                are in range.
            devmem_command -- `devmem` command used to execute register access.

        Keyword Arguments:
            trace -- activate operation tracing (uses `loguru.trace()` under the hood).

        Raises:
            ValueError: raised if sanity check on the arguments doesn't pass.
        """
        super().__init__(data_width, address_bounds, trace)
        if isinstance(devmem_command, str):
            self._cmd = [devmem_command]
        else:
            self._cmd = devmem_command

        try:
            subprocess.run([*self._cmd, "--help"], capture_output=True, check=True)
        except subprocess.CalledProcessError as exc:
            raise RuntimeError(
                f"Execution check of devmem command ({devmem_command}) failed."
            ) from exc

    def _get(self, reg_address: int) -> int:
        """Read register value with `devmem`.

        TODO: Sanitize command output.

        Arguments:
            reg_address -- absolute address of register to read.

        Returns:
            Data from the register.
        """
        try:
            return int(
                subprocess.run(
                    [*self._cmd, f"0x{reg_address:X}", str(self._data_width)],
                    capture_output=True,
                    check=True,
                ).stdout.strip(),
                0,
            )
        except subprocess.CalledProcessError as exc:
            raise RuntimeError(
                f"Failed to execute devmem get command for register 0x{reg_address:X}."
            ) from exc

    def _set(self, reg_address: int, value: int) -> None:
        """Write register using `devmem`.

        TODO: Sanitize command output.

        Arguments:
            reg_address -- absolute address of register to write to.
            value -- value to write to the register.
        """
        try:
            subprocess.run(
                [
                    *self._cmd,
                    f"0x{reg_address:X}",
                    str(self._data_width),
                    f"0x{value:X}",
                ],
                check=True,
            )
        except subprocess.CalledProcessError as exc:
            raise RuntimeError(
                "Failed to execute devmem set command for register "
                f"0x{reg_address:X} = 0x{value:X}."
            ) from exc
