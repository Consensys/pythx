=====
PythX
=====


.. image:: https://img.shields.io/pypi/v/pythx.svg
        :target: https://pypi.org/project/pythx/

.. image:: https://travis-ci.org/dmuhs/pythx.svg?branch=master
        :target: https://travis-ci.org/dmuhs/pythx

.. image:: https://readthedocs.org/projects/pythx/badge/?version=latest
        :target: https://pythx.readthedocs.io/en/latest/?badge=latest

.. image:: https://coveralls.io/repos/github/dmuhs/pythx/badge.svg?branch=master
        :target: https://coveralls.io/github/dmuhs/pythx?branch=master


PythX is a library for the MythX_ smart contract security analysis platform.

.. contents:: Table of Contents


What is MythX?
--------------
MythX is a security analysis API that allows anyone to create purpose-built
security tools for smart contract developers. Tools built on MythX integrate
seamlessly into the development environments and continuous integration
pipelines used throughout the Ethereum ecosystem.


Installation
------------
PythX runs on Python 3.6+ and PyPy3.

To get started, simply run

.. code-block:: console

    $ pip3 install pythx

Alternatively, clone the repository and run

.. code-block:: console

    $ pip3 install .

Or directly through Python's :code:`setuptools`:

.. code-block:: console

    $ python3 setup.py install

Example
-------
PythX aims to provide an easy-to-use interface to the official MythX_ API.
Its goal is to turbocharge tool development and make it easy to deal with
even complex use cases.

.. code-block:: python3

    from pythx import Client


    c = Client(api_key="...")

    # submit bytecode, source files, their AST and more!
    resp = c.analyze(bytecode="0xfe")

    # wait for the analysis to finish
    while not c.analysis_ready(resp.uuid):
        time.sleep(1)

    # have all your security report data at your fingertips
    for issue in c.report(resp.uuid):
        print(issue.swc_title or "Undefined", "-", issue.description_short)

    # Output:
    # Assert Violation - A reachable exception has been detected.


The PythX CLI has now become the MythX CLI!
-------------------------------------------

Originally, the PythX CLI was a proof of concept to display to interested
developers what can be done using the library. The interest in the CLI grew
so large that a lot of developers contacted me and asked for support and
new features.

This is the PSA that **I will no longer maintain the PythX CLI**. But wait!
There's more!

Because a PoC is not exactly what you would call future-proof and maintainable
software, I have decided to do a complete revamp. It is called `mythx-cli` and
incorporates all feature requests I have gotten so far. Check it out
`here <https://github.com/dmuhs/mythx-cli/>`_ and let me know what you think!

Enjoy! :)

.. _MythX: https://mythx.io/
