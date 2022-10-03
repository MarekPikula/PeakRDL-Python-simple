Introduction
============

This package implements Python register abstraction layer export for the
PeakRDL toolchain.


Installing
----------

Install from `PyPi`_ using pip

.. code-block:: bash

    python3 -m pip install peakrdl-python

.. _PyPi: https://pypi.org/project/peakrdl-python



Quick Start
-----------

Exporting to IP-XACT
^^^^^^^^^^^^^^^^^^^^

Below is a simple example that shows how to convert a SystemRDL register model
into IP-XACT.

.. code-block:: python
    :emphasize-lines: 3, 13-15, 17

    import sys
    from systemrdl import RDLCompiler, RDLCompileError
    from peakrdl_ipxact import IPXACTExporter, Standard

    rdlc = RDLCompiler()

    try:
        rdlc.compile_file("path/to/my.rdl")
        root = rdlc.elaborate()
    except RDLCompileError:
        sys.exit(1)

    exporter = IPXACTExporter(
        standard=Standard.IEEE_1685_2014
    )

    exporter.export(root, "path/to/output.xml")


Links
-----

- `Source repository <https://github.com/MarekPikula/PeakRDL-Python>`_
- `Release Notes <https://github.com/MarekPikula/PeakRDL-Python/releases>`_
- `Issue tracker <https://github.com/MarekPikula/PeakRDL-Python/issues>`_
- `PyPi <https://pypi.org/project/peakrdl-python>`_



.. toctree::
    :hidden:

    self
    importer
    exporter
