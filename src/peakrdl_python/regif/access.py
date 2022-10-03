"""Register and field access Pythonic interface."""

__authors__ = ["Marek Pikuła <marek.pikula at embevity.com>"]

from abc import ABC
from typing import Any, Generic, Optional, Type, TypeVar

from .regif import RegisterInterface
from .spec import AddrmapNodeSpec, FieldNodeSpec, NodeSpec, RegNodeSpec

T = TypeVar("T", bound=int)
"""Generic type used for `FieldAccess`.

Needs to be castable to and from int.
"""


class FieldAccess(Generic[T]):
    """Field access Python interface.

    Field type is set as generic, but it needs to be castable to and from
    `int` to work with the register interface. This means it can be, e.g.,
    `int` or any `IntEnum`.

    TODO: Make field type be inferred from SystemRDL and generated.
    """

    def __init__(self, spec: FieldNodeSpec, field_type: Type[T]):
        """Initialize field access interface.

        Arguments:
            spec -- field specification. Used to ensure that the access rules
                defined in SystemRDL source are being followed.
            type -- generic type of the field. Read more in the class description.
        """
        self._spec = spec
        self._type = field_type

    def __get__(self, instance: Any, owner: Any) -> T:
        """Field getter.

        Arguments:
            instance -- parent class instance. Needs to be `RegAccess`.

        Raises:
            RuntimeError: field is not software-readable.

        Returns:
            Field value got from register interface.
        """
        assert isinstance(
            instance, RegAccess
        ), "FieldAccess needs to be used as a member of RegAccess."

        if not self._spec.is_sw_readable:
            raise RuntimeError(f"Field {self._spec.inst_name} is not SW readable.")

        return self._type(
            instance.regif.get_field(
                instance.spec.absolute_address, self._spec.lsb, self._spec.width
            )
        )

    def __set__(self, instance: Any, value: T):
        """Field setter.

        It checks whether the field is software readable.

        Arguments:
            instance -- parent class instance. Needs to be `RegAccess`.
            value -- value to set the field to.

        Raises:
            RuntimeError: field is not software-writable.
        """
        assert isinstance(
            instance, RegAccess
        ), "FieldAccess needs to be used as a member of RegAccess."

        # Check if value is correct (e.g., for IntEnum).
        if not isinstance(value, self._type):
            value = self._type(value)

        if not self._spec.is_sw_writable:
            raise RuntimeError(f"Field {self._spec.inst_name} is not SW writable.")

        instance.regif.set_field(
            instance.spec.absolute_address,
            self._spec.lsb,
            self._spec.width,
            int(value),
        )


SpecT = TypeVar("SpecT", bound=NodeSpec)


class AccessWithRegif(Generic[SpecT]):
    """Generic access class with register interface and specification."""

    def __init__(self, spec: SpecT, register_interface: Optional[RegisterInterface]):
        """Initialize access interface.

        Arguments:
            spec -- node specification.
            register_interface -- register interface. Can be set also by
                setting the `regif` property. Propagates to all members.
        """
        self._spec = spec
        self._regif = None

        if register_interface is not None:
            self.regif = register_interface

    @property
    def spec(self) -> SpecT:
        """Get the specification of the node."""
        return self._spec

    @property
    def regif(self) -> RegisterInterface:
        """Get register interface."""
        assert (
            self._regif is not None
        ), "RegisterInterface should be set in constructor or by constructor of parent."
        return self._regif

    @regif.setter
    def regif(self, regif: RegisterInterface):
        """Set register interface and propagate to members.

        Members need to be instances of AccessWithRegif itself.
        """
        self._regif = regif

        for member_name in vars(self):
            member = self.__dict__[member_name]
            if isinstance(member, AccessWithRegif):
                member.regif = regif


class RegAccess(AccessWithRegif[RegNodeSpec], ABC):
    """Register access Python interface.

    The children of this class should have all the fields (`FieldAccess`) set
    as members.
    """


class AddrmapAccess(AccessWithRegif[AddrmapNodeSpec], ABC):
    """Address map access Python interface.

    The children of this class should have all the SystemRDL children (either
    RegAccess or AddrmapAccess) set as members.
    """
