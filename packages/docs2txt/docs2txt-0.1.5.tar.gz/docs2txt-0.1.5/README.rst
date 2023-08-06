=============
docs2txt
=============


.. image:: https://img.shields.io/pypi/v/docs2txt.svg
        :target: https://pypi.python.org/pypi/docs2txt

.. image:: https://img.shields.io/travis/ehutzle/docs2txt.svg
        :target: https://travis-ci.com/ehutzle/docs2txt

.. image:: https://readthedocs.org/projects/docs2txt/badge/?version=latest
        :target: https://docs2txt.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status




A simple program to download documentation from docs.rs and convert it into a plaintext file.


* Free software: MIT license
* Documentation: https://docs2txt.readthedocs.io.


Features
--------

Rust
^^^^
- Download documentation from docs.rs and convert it into a plaintext file.

Usage
-----
- Create a virtual environment and install the package ``python -m venv venv``
- Install the package with ``pip install docs2txt``
- Activate the virtual environment
    - OSX / Linux: ``source venv/bin/activate``
    - Windows: ``venv\Scripts\activate``

- Run the program:
    - ``python -m docs2txt``

Examples
--------

To download the documentation of the redb crate and save it to a folder on your desktop named "Rust Docs":

- ``python -m docs2txt docs-rs --url https://docs.rs/redb/1.0.4/redb/ --output-dir '~/Desktop/Rust Docs'``

