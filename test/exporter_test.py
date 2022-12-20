"""Exporter tests."""

__authors__ = ["Marek Pikuła <marek.pikula at embevity.com>"]

import difflib

import pytest
from systemrdl import RDLCompiler  # type: ignore

from example.accelera_generic_example import SomeRegisterMapAddrmap
from peakrdl_python_simple.exporter import PythonExporter
from peakrdl_python_simple.regif.impl.dummy import DummyRegIf


def test_exporter_basic():
    """Basic exporter test comparing with a reference file."""
    in_path = "example/accelera_generic_example.rdl"
    ref_out_path = "example/accelera_generic_example.py"
    out_path = "output/accelera_generic_example.py"

    # Generate the file.
    rdlc = RDLCompiler()
    rdlc.compile_file(in_path)
    PythonExporter().export(
        rdlc.elaborate(),  # type: ignore
        out_path,
        input_files=[in_path],
    )

    # Check if the generated file matches reference file.
    with open(out_path, encoding="UTF-8") as out_file, open(
        ref_out_path, encoding="UTF-8"
    ) as ref_out_file:
        result = "\n".join(
            difflib.unified_diff(
                out_file.readlines(),
                ref_out_file.readlines(),
                out_path,
                ref_out_path,
            )
        )
    print(result)
    assert len(result) == 0, "Generated file doesn't match reference file."


@pytest.fixture
def test_regif():
    """Create register interface."""
    return DummyRegIf(8 * 4, range(0, 0x1000), 0, trace=True)


def test_exporter_regif(test_regif: DummyRegIf):
    """Perform some register interface tests on the generated file."""
    regmap = SomeRegisterMapAddrmap(test_regif)

    # Write value to a field.
    regmap.myRegInst.data0 = 3
    assert test_regif.get(regmap.myRegInst.spec.absolute_address) == 3
    assert regmap.myRegInst.data0 == 3

    # Write value to a second field in the register and check if it didn't mess
    # up other fields.
    regmap.myRegInst.data1 = 2
    assert test_regif.get(regmap.myRegInst.spec.absolute_address) == 3 + (2 << 2)
    assert regmap.myRegInst.data0 == 3
    assert regmap.myRegInst.data1 == 2
    assert regmap.myRegInst.data2 == 0
