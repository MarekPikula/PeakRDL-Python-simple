"""PeakRDL Python exporter."""

__authors__ = ["Marek Pikuła <marek.pikula at embevity.com>"]

import random
import string
from dataclasses import dataclass
from pathlib import Path
from typing import Any, List, Optional, Tuple, Union

from systemrdl.messages import MessageHandler  # type: ignore
from systemrdl.node import (  # type: ignore
    AddrmapNode,
    FieldNode,
    Node,
    RegfileNode,
    RegNode,
    RootNode,
)


class PythonExporter:  # pylint: disable=too-few-public-methods
    """PeakRDL Python exporter main class."""

    SpecList = List[Any]
    """Specification list. Later reformatted to string."""

    @dataclass
    class GenStageOutput:
        """Generation stage output."""

        node: Node
        """Node on which generation has been performed."""

        type_name: str
        """Name of Python type of this node."""

        spec_list: "PythonExporter.SpecList"
        """List of specification items."""

        generated_code: str
        """Python code generated during this stage."""

    def __init__(self):
        """Initialize the exporter."""
        # List of existing types to prevent duplication.
        self._existing_types: List[str] = []

    def export(
        self,
        node: Union[AddrmapNode, RootNode],
        output_path: str,
        rename: Optional[str] = None,
    ):
        """Export the `node` to generated Python interface file.

        Arguments:
            node -- node to export.
            output_path -- path to the exported file.
            rename -- name to rename the top-level to.
        """
        # Each export should start fresh.
        self._existing_types.clear()

        # Get the top node.
        top = node.top if isinstance(node, RootNode) else node
        top_name = rename if rename is not None else node.inst_name

        # Ensure proper format of the output path and that the directory exists.
        if not output_path.endswith(".py"):
            raise ValueError("The output file is not Python file.")
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        # Generate the file.
        with open(output_path, "w", encoding="UTF-8") as output:
            output.write(
                (
                    '"""Python abstraction for SystemRDL register description.\n\n'
                    f"Generated from {top_name}. Don't override.\n"
                    '"""\n\n'
                    "from peakrdl_python_simple.regif import spec, access\n"
                )
                + self._add_addrmap_regfile(
                    top, node.env.msg, is_top=True
                ).generated_code
            )

    @staticmethod
    def _format_spec_list(spec_list: SpecList) -> str:
        """Format specification list.

        Arguments:
            spec_list -- specification list with arbitrary types.

        Returns:
            Generated string of specification values.
        """
        return ", ".join(
            str(s) if not isinstance(s, str) else f'"{s}"' for s in spec_list
        )

    def _generate_docstring(
        self, node: Node, indent: int = 4, add_final_newline: bool = True
    ) -> str:
        """Generate docstring basing on the Node properties.

        Arguments:
            node -- Node to generate the docstring for.

        Keyword Arguments:
            indent -- count of spaces of indentation.
            add_final_newline -- whether to add endline at the end or not of
                the docstring. If name and desc are empty the newline is not
                generated either way.

        Returns:
            Generated docstring.
        """
        indent_str = "\n" + " " * indent
        name = node.get_property("name", default="").replace("\n", indent_str)
        desc = node.get_property("desc", default="").replace("\n", indent_str)

        start = indent_str + '"""'
        end = '"""' + ("\n" if add_final_newline else "")
        if name == "" and desc == "":
            return ""
        if name != "" and desc == "":
            return start + name + end
        if name == "" and desc != "":
            return start + desc + end
        return start + name + "\n" + indent_str + desc + indent_str + end

    def _format_member(
        self, member: GenStageOutput, indent: int = 4, last: bool = False
    ) -> str:
        """Format class member.

        Arguments:
            member -- member definition to create the definition for.

        Keyword Arguments:
            indent -- count of spaces of indentation.
            last -- the member is the last in the class declaration.

        Returns:
            Generated member with docstring if applicable.
        """
        is_field = isinstance(member.node, FieldNode)
        return (
            (" " * indent)
            + f"{member.node.inst_name} = {member.type_name}("
            + f"specification=spec.{member.node.__class__.__name__}Spec("
            + self._format_spec_list(member.spec_list)
            + ")"
            + (", field_type=int" if is_field else "")
            + ")"
            + self._generate_docstring(member.node, indent, not last)
        )

    @staticmethod
    def _to_pascal_case(unknown_str: str):
        """Convert arbitrary string to PascalCase.

        Used for generating class names.

        Arguments:
            unknown_str -- arbitrary string.

        Returns:
            (Hopefully) PascalCase string.
        """
        out = unknown_str
        if "_" in unknown_str:
            out = "".join(
                s[0].upper() + (s[1:] if len(s) > 1 else "")
                for s in unknown_str.split("_")
            )
        return out[0].upper() + (out[1:] if len(out) > 1 else "")

    def _format_class(
        self,
        node: Node,
        spec_list: Optional[List[Any]] = None,
        member_list: Optional[List[GenStageOutput]] = None,
        check_if_exists: bool = True,
    ) -> Tuple[str, str]:
        """Generage class definition.

        Arguments:
            node -- node to generate the class for.

        Keyword Arguments:
            spec_list -- optional specification list for `_spec` member generation.
            member_list -- optional list of members. If none are present `pass`
                is added.
            check_if_exists -- check if the type exists and don't generate code
                if indeed it exists. Uses `self._existing_types` list.

        Returns:
            Class name and generated code tuple.
        """
        node_type = node.__class__.__name__.replace("Node", "")
        type_name = self._to_pascal_case(
            node.type_name + node_type
            if node.type_name is not None
            else "".join(random.choice(string.ascii_lowercase) for _ in range(16))
        )
        if check_if_exists:
            if type_name in self._existing_types:
                return type_name, ""
            self._existing_types.append(type_name)

        generic = "[int]" if isinstance(node, FieldNode) else ""
        gen = (
            f"\n\nclass {type_name}(access.{node_type}Access{generic}):"
            + self._generate_docstring(node, 4, True)
            + "\n"
        )
        if spec_list is not None:
            gen += (
                f"    _spec = spec.{node_type}NodeSpec("
                + self._format_spec_list(spec_list)
                + ")\n"
            )
        if member_list is not None and len(member_list) > 0:
            gen += "\n".join(
                self._format_member(member, 4, i == len(member_list) - 1)
                for i, member in enumerate(member_list)
            )
        else:
            gen += "    pass"

        return type_name, gen + "\n"

    def _add_addrmap_regfile(
        self,
        node: Union[AddrmapNode, RegfileNode],
        msg: MessageHandler,
        is_top: bool = False,
    ) -> GenStageOutput:
        """Generate addrmap or regfile.

        Arguments:
            node -- RegfileNode or AddrmapNode.
            msg -- message handler from top-level.

        Keyword Arguments:
            is_top -- if the current not is the top node. If True the
                specification is embedded as class member.

        Returns:
            Generated addrmap output.
        """
        members: List[PythonExporter.GenStageOutput] = []
        gen: str = ""
        for child in node.children(unroll=True, skip_not_present=False):
            if isinstance(child, (AddrmapNode, RegfileNode)):
                output = self._add_addrmap_regfile(child, msg)
                gen += output.generated_code
                members.append(output)
            elif isinstance(child, RegNode):
                output = self._add_reg(child, msg)
                gen += output.generated_code
                members.append(output)
            else:
                msg.warning(
                    f"Unsupported type of node ({child.type_name}) for {child.inst_name}."
                )

        spec = [
            node.inst_name,
            node.type_name,
            node.orig_type_name,
            node.external,
            node.raw_address_offset,
            node.address_offset,
            node.raw_absolute_address,
            node.absolute_address,
            node.size,
            node.total_size,
        ]
        type_name, gen_node = self._format_class(
            node, spec if is_top else None, members
        )
        return PythonExporter.GenStageOutput(node, type_name, spec, gen + gen_node)

    def _add_reg(self, node: RegNode, msg: MessageHandler) -> GenStageOutput:
        """Generate register.

        Arguments:
            node -- RegNode.
            msg -- message handler from top-level.

        Returns:
            Generated register output.
        """
        gen: str = ""
        members: List[PythonExporter.GenStageOutput] = []
        for field in node.fields(skip_not_present=True):
            output = self._add_field(field, msg)
            gen += output.generated_code
            members.append(output)

        spec = [
            node.inst_name,
            node.type_name,
            node.orig_type_name,
            node.external,
            node.raw_address_offset,
            node.address_offset,
            node.raw_absolute_address,
            node.absolute_address,
            node.size,
            node.total_size,
            node.is_virtual,
            node.has_sw_writable,
            node.has_sw_readable,
            node.has_hw_writable,
            node.has_hw_readable,
            node.is_interrupt_reg,
            node.is_halt_reg,
        ]
        type_name, gen_node = self._format_class(node, member_list=members)
        return PythonExporter.GenStageOutput(node, type_name, spec, gen + gen_node)

    def _add_field(
        self,
        node: FieldNode,
        msg: MessageHandler,  # pylint: disable=unused-argument
    ) -> GenStageOutput:
        """Generate field.

        Arguments:
            node -- FieldNode.
            msg -- message handler from top-level.

        Returns:
            Generated field output.
        """
        spec = [
            node.inst_name,
            node.type_name,
            node.orig_type_name,
            node.external,
            node.width,
            node.msb,
            node.lsb,
            node.high,
            node.low,
            node.is_virtual,
            node.is_volatile,
            node.is_sw_writable,
            node.is_sw_readable,
            node.is_hw_writable,
            node.is_hw_readable,
            node.implements_storage,
            node.is_up_counter,
            node.is_down_counter,
        ]
        return PythonExporter.GenStageOutput(node, "access.FieldAccess", spec, "")


if __name__ == "__main__":
    from systemrdl import RDLCompiler  # type: ignore

    rdlc = RDLCompiler()
    rdlc.compile_file("tests/test_sources/accelera-generic_example.rdl")
    e = PythonExporter()
    e.export(
        rdlc.elaborate(),  # type: ignore
        "tests/test_sources/accelera-generic_example.py",
    )
