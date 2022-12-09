[![Documentation Status](https://readthedocs.org/projects/peakrdl-python-simple/badge/?version=latest)](http://peakrdl-python-simple.readthedocs.io)
[![build](https://github.com/MarekPikula/PeakRDL-Python-simple/workflows/build/badge.svg)](https://github.com/MarekPikula/PeakRDL-Python-simple/actions?query=workflow%3Abuild+branch%3Amain)
[![Coverage Status](https://coveralls.io/repos/github/MarekPikula/PeakRDL-Python-simple/badge.svg?branch=main)](https://coveralls.io/github/MarekPikula/PeakRDL-Python-simple?branch=main)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/peakrdl-python-simple.svg)](https://pypi.org/project/peakrdl-python-simple)

# PeakRDL-Python

This package implements Python register abstraction layer export for the
PeakRDL toolchain.

- **Export:** Convert compiled SystemRDL input into Python register interface.

For the command line tool, see the [PeakRDL
project](https://peakrdl.readthedocs.io).

## Usage

The basic install comes without the exporter capability, so that the package
can be installed on low-end devices without the need to install
`systemrdl-compiler`. To have the generator capability install with `generator`
extra:

    $ pip install peakrdl-python-simple[generator]

PeakRDL project provides a standard CLI interface. It can be installed directly
via pip or by installing this package with `cli` extra:

    $ pip install peakrdl-python-simple[cli]

Then this package can be used with the following command:

    $ peakrdl python-simple input_file.rdl -o output_interface.py

## Documentation

See the [PeakRDL-Python-simple
Documentation](http://peakrdl-python-simple.readthedocs.io) for more details.
