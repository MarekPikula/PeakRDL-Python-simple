"""Reister interface simple test and demonstration of the package."""

from enum import IntEnum

from .access import FieldAccess, RegAccess
from .impl.dummy import DummyRegIf
from .spec import FieldNodeSpec, RegNodeSpec


class TestEnum(IntEnum):
    """Test enumaration type to check type casting for field access."""

    VALUE_0 = 0
    VALUE_1 = 1
    VALUE_2 = 2
    VALUE_4 = 4


class TestReg(RegAccess):
    """Test register."""

    _spec = RegNodeSpec(
        inst_name="test_reg",
        type_name="int",
        orig_type_name="int",
        external=False,
        raw_address_offset=0,
        address_offset=0,
        raw_absolute_address=0,
        absolute_address=0,
        size=1,
        total_size=1,
        is_array=False,
        array_dimensions=None,
        array_stride=None,
        is_virtual=False,
        has_sw_writable=True,
        has_sw_readable=True,
        has_hw_writable=True,
        has_hw_readable=True,
        is_interrupt_reg=False,
        is_halt_reg=False,
        field_count=1,
    )

    test_field = FieldAccess(
        FieldNodeSpec(
            inst_name="test_field",
            type_name="TestEnum",
            orig_type_name="TestEnum",
            external=False,
            width=3,
            msb=12,
            lsb=10,
            high=12,
            low=10,
            is_virtual=False,
            is_volatile=False,
            is_sw_writable=True,
            is_sw_readable=True,
            is_hw_writable=True,
            is_hw_readable=True,
            implements_storage=True,
            is_up_counter=False,
            is_down_counter=False,
            encode="TestEnum",
        ),
        TestEnum,
    )


if __name__ == "__main__":
    test_reg = TestReg(DummyRegIf(4 * 8, range(0, 0x1000), 0, trace=True))

    # Simple read using TestEnum.
    print(test_reg.test_field)
    assert test_reg.test_field == TestEnum.VALUE_0

    # Simple write/read using TestEnum.
    test_reg.test_field = TestEnum.VALUE_1
    print(test_reg.test_field)
    assert test_reg.test_field == TestEnum.VALUE_1

    # Simple write/read using integer as written value.
    test_reg.test_field = 2  # type: ignore
    print(test_reg.test_field)
    assert test_reg.test_field == TestEnum.VALUE_2

    # Passing wrong value to the field.
    try:
        test_reg.test_field = 3  # type: ignore
    except ValueError:
        print("TestEnum cast error correctly caught.")
