Introduction
============

This package implements a simple Python register abstraction layer export for
the PeakRDL toolchain.


Installing
----------

Install from `PyPi`_ using pip:

.. code-block:: bash

    python3 -m pip install peakrdl-python-simple[generator]

.. _PyPi: https://pypi.org/project/peakrdl-python-simple

If you want to use official PeakRDL CLI you can install with ``cli`` extra:

.. code-block:: bash

    python3 -m pip install peakrdl-python-simple[cli]

Quick Start
-----------

Exporting to Python interface
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The module integrates with PeakRDL CLI interface (via optional extra ``cli``):

.. code-block:: bash

    peakrdl python-simple input_file.rdl -o output_interface.py


Links
-----

- `Source repository <https://github.com/MarekPikula/PeakRDL-Python-simple>`_
- `Release Notes <https://github.com/MarekPikula/PeakRDL-Python-simple/releases>`_
- `Issue tracker <https://github.com/MarekPikula/PeakRDL-Python-simple/issues>`_
- `PyPi <https://pypi.org/project/peakrdl-python-simple>`_



.. toctree::
    :hidden:

    self
    exporter
