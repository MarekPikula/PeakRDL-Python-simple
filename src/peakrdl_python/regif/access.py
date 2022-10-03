"""Register and field access Pythonic interface."""

__authors__ = ["Marek Pikuła <marek.pikula at embevity.com>"]

from abc import ABC
from typing import Any, Generic, Type, TypeVar

from .regif import RegisterInterface
from .spec import FieldNodeSpec, RegNodeSpec


class RegAccess(ABC):
    """Register access Python interface.

    The children should have all the fields (`FieldAccess`) set as members.
    """

    _reg_spec: RegNodeSpec
    """Register specification. Should be defined in child."""

    def __init__(self, register_interface: RegisterInterface):
        """Initialize register access interface.

        Arguments:
            spec -- register node specification.
            register_interface -- register interface.
        """
        self._regif = register_interface

    @property
    def spec(self):
        """Get register specification."""
        return self._reg_spec

    @property
    def regif(self):
        """Get register interface."""
        return self._regif


T = TypeVar("T", bound=int)
"""Generic type used for `FieldAccess`.

Needs to be castable to and from int.
"""


class FieldAccess(Generic[T], object):
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
