.. image:: https://raw.githubusercontent.com/quantumlib/alphaclops/master/docs/images/alphaclops_logo_color.png
  :target: https://github.com/quantumlib/alphaclops
  :alt: alphaclops
  :width: 500px

alphaclops is a Python library for writing, manipulating, and optimizing quantum
circuits and running them against quantum computers and simulators.

This module is **alphaclops-core**, which contains everything you'd need to write quantum algorithms for NISQ devices and run them on the built-in alphaclops simulators.
In order to run algorithms on a given quantum hardware platform, you'll have to install the right alphaclops module as well.

Installation
------------

To install the stable version of only **alphaclops-core**, use `pip install alphaclops-core`.
To install the pre-release version of only **alphaclops-core**, use `pip install alphaclops-core --pre`.

To get all the optional modules installed as well, you'll have to use `pip install alphaclops` or `pip install alphaclops --pre` for the pre-release version.
