"""Node specification dataclasses.

All are based on available properties of their systemrdl.node.* counterparts.
"""

__authors__ = ["Marek Pikuła <marek.pikula at embevity.com>"]

from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class NodeSpec:
    """Specification of systemrdl.node.Node."""

    # owning_addrmap: Optional["AddrmapNodeSpec"]
    inst_name: str
    type_name: Optional[str]
    orig_type_name: Optional[str]
    external: bool
    # cpuif_reset: Optional["SignalNode"]


@dataclass(frozen=True)
class AddressableNodeSpec(NodeSpec):  # pylint: disable=too-many-instance-attributes
    """Specification of systemrdl.node.AddressableNode."""

    raw_address_offset: int
    address_offset: int
    raw_absolute_address: int
    absolute_address: int
    size: int
    total_size: int
    is_array: bool
    array_dimensions: Optional[List[int]]
    array_stride: Optional[int]


@dataclass(frozen=True)
class VectorNodeSpec(NodeSpec):
    """Specification of systemrdl.node.VectorNode."""

    width: int
    msb: int
    lsb: int
    high: int
    low: int


@dataclass(frozen=True)
class RootNodeSpec(NodeSpec):
    """Specification of systemrdl.node.RootNode."""


@dataclass(frozen=True)
class SignalNodeSpec(VectorNodeSpec):
    """Specification of systemrdl.node.SignalNode."""


@dataclass(frozen=True)
class FieldNodeSpec(VectorNodeSpec):  # pylint: disable=too-many-instance-attributes
    """Specification of systemrdl.node.FieldNode."""

    is_virtual: bool
    is_volatile: bool
    is_sw_writable: bool
    is_sw_readable: bool
    is_hw_writable: bool
    is_hw_readable: bool
    implements_storage: bool
    is_up_counter: bool
    is_down_counter: bool
    # Aliases not supported:
    #   is_alias: bool
    #   alias_primary: "FieldNodeSpec"
    #   has_aliases: bool
    #   aliases: Iterator["FieldNodeSpec"]
    encode: str


@dataclass(frozen=True)
class RegNodeSpec(AddressableNodeSpec):  # pylint: disable=too-many-instance-attributes
    """Specification of systemrdl.node.RegNode."""

    is_virtual: bool
    has_sw_writable: bool
    has_sw_readable: bool
    has_hw_writable: bool
    has_hw_readable: bool
    is_interrupt_reg: bool
    is_halt_reg: bool
    # Aliases not supported:
    #   is_alias: bool
    #   alias_primaty: "RegNodeSpec"
    #   has_aliases: bool
    #   aliases: Iterator["RegNodeSpec"]
    field_count: int


@dataclass(frozen=True)
class RegfileNodeSpec(AddressableNodeSpec):
    """Specification of systemrdl.node.RegfileNode."""


@dataclass(frozen=True)
class AddrmapNodeSpec(AddressableNodeSpec):
    """Specification of systemrdl.node.AddrmapNode."""


@dataclass(frozen=True)
class MemNodeSpec(AddressableNodeSpec):
    """Specification of systemrdl.node.MemNode."""

    is_sw_writable: bool
    is_sw_readable: bool
