"""Register and field access Pythonic interface."""

__authors__ = ["Marek Pikuła <marek.pikula at embevity.com>"]

import itertools
from abc import ABC
from typing import Any, Generic, Optional, Type, TypeVar

from .regif import RegisterInterface
from .spec import (
    AddressableNodeSpec,
    AddrmapNodeSpec,
    FieldNodeSpec,
    NodeSpec,
    RegfileNodeSpec,
    RegNodeSpec,
)

SpecT = TypeVar("SpecT", bound=NodeSpec)
"""Node specification generic type."""


class SpecMixin(Generic[SpecT]):  # pylint: disable=too-few-public-methods
    """Specification mixin.

    `_spec` can be set in the constructor or in the final child class.
    """

    _spec: Optional[SpecT]

    def __init__(self, specification: Optional[SpecT] = None):
        """Initialize class with specification.

        Arguments:
            specification -- Node specification. Can be set to None, but then
                `_spec` class member needs to be set explicitly in the child
                class declaration.
        """
        if not hasattr(self.__class__, "_spec"):
            self._spec: Optional[SpecT] = specification

    @property
    def spec(self) -> SpecT:
        """Get the specification of the node."""
        if hasattr(self, "_spec") and self._spec is not None:
            return self._spec
        if (
            hasattr(self.__class__, "_spec")
            and self.__class__._spec is not None  # pylint: disable=protected-access
        ):
            return self.__class__._spec  # pylint: disable=protected-access
        assert False, "SpecMixin requires programmer to set `_spec` member."


T = TypeVar("T", bound=int)
"""Generic type used for `FieldAccess`.

Needs to be castable to and from int.
"""


class FieldAccess(Generic[T], SpecMixin[FieldNodeSpec], ABC):
    """Field access Python interface.

    Field type is set as generic, but it needs to be castable to and from
    `int` to work with the register interface. This means it can be, e.g.,
    `int` or any `IntEnum`.
    """

    def __init__(self, specification: FieldNodeSpec, field_type: Type[T]):
        """Field interface access.

        Arguments:
            specification -- field specification.
            field_type -- Python type of the data stored in the field.
        """
        super().__init__(specification)
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

        if not self.spec.is_sw_readable:
            raise RuntimeError(f"Field {self.spec.inst_name} is not SW readable.")

        return self._type(
            instance.regif.get_field(
                instance.spec.absolute_address, self.spec.lsb, self.spec.width
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

        if not self.spec.is_sw_writable:
            raise RuntimeError(f"Field {self.spec.inst_name} is not SW writable.")

        instance.regif.set_field(
            instance.spec.absolute_address,
            self.spec.lsb,
            self.spec.width,
            int(value),
            instance.spec.field_count == 1,
        )


class AccessWithRegifMixin:  # pylint: disable=too-few-public-methods
    """Generic access class with register interface and specification."""

    def __init__(self, register_interface: Optional[RegisterInterface]):
        """Initialize access interface.

        Arguments:
            spec -- node specification.
            register_interface -- register interface. Can be set also by
                setting the `regif` property. Propagates to all members.
        """
        self._regif = None

        if register_interface is not None:
            self.regif = register_interface

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

        for member in itertools.chain(
            self.__class__.__dict__.values(), self.__dict__.values()
        ):
            if isinstance(member, AccessWithRegifMixin):
                member.regif = regif


AddressableSpecT = TypeVar("AddressableSpecT", bound=AddressableNodeSpec)
"""Addressable node specification generic type."""


class HierarchicalAccess(
    Generic[AddressableSpecT], AccessWithRegifMixin, SpecMixin[AddressableSpecT], ABC
):
    """Hierarchical block access interface.

    Arguments:
        AddressableSpecT -- Node specification.
    """

    def __init__(
        self,
        register_interface: Optional[RegisterInterface] = None,
        specification: Optional[AddressableSpecT] = None,
    ):
        """Initialize the hierarchical access block.

        It's merging `AccessWithRegifMixin` and `SpecMixin` initializers.

        Keyword Arguments:
            register_interface -- register interface. Can be set also by
                setting the `regif` property. Propagates to all members.
            specification -- node specification. Can be also set by setting
                `_spec` child class member.
        """
        AccessWithRegifMixin.__init__(self, register_interface)
        # TODO: Figure out why mypy doesn't like it:
        SpecMixin.__init__(self, specification)  # type: ignore


class RegAccess(HierarchicalAccess[RegNodeSpec], ABC):
    """Register access Python interface.

    The children of this class should have all the fields (`FieldAccess`) set
    as members and `_spec` set to instance of RegNodeSpec.
    """


class AddrmapAccess(HierarchicalAccess[AddrmapNodeSpec], ABC):
    """Address map access Python interface.

    The children of this class should have all the SystemRDL children (either
    RegAccess or AddrmapAccess) set as members and `_spec` set to instance of
    AddrmapNodeSpec.
    """


class RegfileAccess(HierarchicalAccess[RegfileNodeSpec], ABC):
    """Register file access Python interface.

    The children of this class should have all the SystemRDL children (either
    RegAccess or AddrmapAccess) set as members and `_spec` set to instance of
    RegfileSpec.
    """
