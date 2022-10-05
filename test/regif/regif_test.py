import pytest

from peakrdl_python_simple.regif import __main__ as test_classes
from peakrdl_python_simple.regif.regif import DummyRegIf


@pytest.fixture
def test_regif():
    """Create register interface."""
    return DummyRegIf(8 * 4, range(0, 0x1000), 0)


@pytest.fixture
def test_reg(test_regif: DummyRegIf) -> test_classes.TestReg:
    """Create test register definition."""
    return test_classes.TestReg(test_regif)


def test_read(test_reg: test_classes.TestReg):
    """Simple read using TestEnum."""
    assert (
        test_reg.test_field == test_classes.TestEnum.VALUE_0
    ), "By default the register should be filled with 0."


def test_write_read_enum(test_reg: test_classes.TestReg):
    """Simple write/read using TestEnum."""
    test_reg.test_field = test_classes.TestEnum.VALUE_1
    assert (
        test_reg.test_field == test_classes.TestEnum.VALUE_1
    ), "The field should hold updated value."
    assert isinstance(
        test_reg.test_field, test_classes.TestEnum
    ), "The field should be an instance of declared type."


def test_write_read_enum_int(test_reg: test_classes.TestReg):
    """Simple write/read using integer as written value."""
    test_reg.test_field = 2  # type: ignore
    assert (
        test_reg.test_field == test_classes.TestEnum.VALUE_2
    ), "The field should hold updated value correctly casted to declared type."
    assert isinstance(
        test_reg.test_field, test_classes.TestEnum
    ), "The field should be an instance of declared type."


def test_write_wrong_int(test_reg: test_classes.TestReg):
    """Passing wrong value to the field."""
    with pytest.raises(ValueError):
        test_reg.test_field = 3  # type: ignore
