"""Register interface using `devmem` command."""

__authors__ = ["Marek Pikuła <marek.pikula at embevity.com>"]

from typing import List, Optional, Tuple

from ..regif import RegisterInterface


class MultiRegionRegIf(RegisterInterface):
    """Register interface mapping multiple regions to different separate regifs."""

    def __init__(self, regions: List[RegisterInterface], trace: Optional[bool] = None):
        """Initialize the multi-region register interface.

        The sub-regions need to:
        - have the same data width,
        - defined address bounds,
        - have no address bounds collisions between each other.

        Arguments:
            regions -- list of regions.

        Keyword Arguments:
            trace -- overrides operation tracing for all regions. If None doesn't modify the
                sub-regions.

        Raises:
            ValueError: forbidden configuration of sub-regions.
        """
        if len(regions) == 0:
            raise ValueError("A multi-region needs to have at least one sub-region.")

        bound_regions: List[Tuple[range, RegisterInterface]] = []
        for reg_id, region in enumerate(regions):
            if region.data_width != regions[0].data_width:
                raise ValueError(
                    "All sub-regions need to have the same data width "
                    f"(region {reg_id} has width {region.data_width}, "
                    f"expected {regions[0].data_width})."
                )
            if region._address_bounds is None:
                raise ValueError(
                    f"Sub-region {reg_id} doesn't have address bounds defined."
                )
            for bound_id, (bound, _) in enumerate(bound_regions):
                if (
                    region._address_bounds.start in bound
                    or region._address_bounds.stop in bound
                ):
                    raise ValueError(
                        f"Address bounds collision between sub-region {reg_id} and {bound_id}."
                    )
            bound_regions.append((region._address_bounds, region))

        self._regions = sorted(bound_regions, key=lambda region: region[0].start)
        super().__init__(
            regions[0].data_width,
            range(self._regions[0][0].start, self._regions[-1][0].stop),
            trace=False,
        )

        if trace is not None:
            self.tracing_enabled = trace

    @property
    def tracing_enabled(self) -> bool:
        """Check if any sub-region has operation tracing enabled."""
        return any(region[1].tracing_enabled for region in self._regions)

    @tracing_enabled.setter
    def tracing_enabled(self, trace: bool):
        for region in self._regions:
            region[1].tracing_enabled = trace

    def _address_to_region(self, reg_address: int) -> RegisterInterface:
        for bounds, regif in self._regions:
            if bounds.start <= reg_address < bounds.stop:
                return regif
        raise ValueError(f"The address {reg_address} isn't assigned to any sub-region.")

    def _get(self, reg_address: int) -> int:
        """Get value from register.

        Arguments:
            reg_address -- absolute register address.

        Returns:
            Register value.
        """
        return self._address_to_region(reg_address).get(reg_address)

    def _set(self, reg_address: int, value: int):
        """Set register value.

        Arguments:
            reg_address -- absolute register address.
            value -- value to write to the register.
        """
        self._address_to_region(reg_address).set(reg_address, value)
