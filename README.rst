=====
PythX
=====


.. image:: https://img.shields.io/pypi/v/pythx.svg
        :target: https://pypi.python.org/pypi/pythx

.. image:: https://img.shields.io/travis/dmuhs/pythx.svg
        :target: https://travis-ci.org/dmuhs/pythx

.. image:: https://readthedocs.org/projects/pythx/badge/?version=latest
        :target: https://pythx.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/dmuhs/pythx/shield.svg
        :target: https://pyup.io/repos/github/dmuhs/pythx/
        :alt: Updates

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
PythX runs on Python 3.5+.

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


    # login as free trial user
    c = Client(eth_address="0x0000000000000000000000000000000000000000", password="trial")

    # submit bytecode, source files, their AST and more!
    resp = c.analyze(bytecode="0xfe")

    # wait for the analysis to finish
    while not c.analysis_ready(resp.uuid):
        time.sleep(1)

    # have all your security report data at your fingertips
    for issue in report:
        print(issue.swc_title or "Undefined", "-", issue.description_short)

    # Output:
    # Assert Violation - A reachable exception has been detected.
    # Undefined - MythX API trial mode.


The PythX CLI
-------------
The PythX CLI aims to be a simple example implementation to show developers on
a practical example how PythX can be used in action. It provides a simple (and
pretty!) interface to list analyses, submit new ones, check the status of a
job, and get report data on the found issues.

.. code-block:: console

    $ pythx
    Usage: pythx [OPTIONS] COMMAND [ARGS]...

    Options:
    --help  Show this message and exit.

    Commands:
    check    Submit a new analysis job based on source code, byte code, or...
    login    Login to your MythX account
    logout   Log out of your MythX account
    openapi  Get the OpenAPI spec in HTML or YAML format
    ps       Get a greppable overview of submitted analyses
    refresh  Refresh your MythX API token
    report   Check the detected issues of a finished analysis job
    status   Get the status of an analysis by its UUID
    top      Display the most recent analysis jobs and their status
    version  Print version information of PythX and the API


By default, PythX comes with a pre-enabled trial user. To get started right
away, simply login with the default values:

.. code-block:: console

    $ pythx login
    Please enter your Ethereum address [0x0000000000000000000000000000000000000000]:
    Please enter your MythX password [trial]:
    Successfully logged in as 0x0000000000000000000000000000000000000000

If you already have an account on MythX_, simply login with your Ethereum
address and the API password you have set on the website.

Submit an Solidity source file for analysis:

.. code-block:: console

    $ pythx check -sf test.sol
    Analysis submitted as job df137587-7fc1-466a-a4b2-d63392099682


Check the status of your analysis job:

.. code-block:: console

    $ pythx status df137587-7fc1-466a-a4b2-d63392099682
    ╒════════════════╤══════════════════════════════════════╕
    │ uuid           │ df137587-7fc1-466a-a4b2-d63392099682 │
    ├────────────────┼──────────────────────────────────────┤
    │ apiVersion     │ v1.4.3                               │
    ├────────────────┼──────────────────────────────────────┤
    │ mythrilVersion │ 0.20.0                               │
    ├────────────────┼──────────────────────────────────────┤
    │ maestroVersion │ 1.2.3                                │
    ├────────────────┼──────────────────────────────────────┤
    │ harveyVersion  │ 0.0.13                               │
    ├────────────────┼──────────────────────────────────────┤
    │ maruVersion    │ 0.3.4                                │
    ├────────────────┼──────────────────────────────────────┤
    │ queueTime      │ 0                                    │
    ├────────────────┼──────────────────────────────────────┤
    │ runTime        │ 0                                    │
    ├────────────────┼──────────────────────────────────────┤
    │ status         │ Finished                             │
    ├────────────────┼──────────────────────────────────────┤
    │ submittedAt    │ 2019-03-05T10:24:05.071Z             │
    ├────────────────┼──────────────────────────────────────┤
    │ submittedBy    │ 123456789012345678901234             │
    ╘════════════════╧══════════════════════════════════════╛


Get the analysis report. Pinpointing the line and column locations is still
a bit buggy, sorry. :)

.. code-block:: console

    $ pythx report df137587-7fc1-466a-a4b2-d63392099682
    Report for Unknown
    ╒════════╤══════════╤══════════════════╤════════════╤═══════════════════════════════════╕
    │   Line │   Column │ SWC Title        │ Severity   │ Short Description                 │
    ╞════════╪══════════╪══════════════════╪════════════╪═══════════════════════════════════╡
    │      0 │        0 │ Reentrancy       │ High       │ persistent state read after call  │
    ├────────┼──────────┼──────────────────┼────────────┼───────────────────────────────────┤
    │      0 │        0 │ Reentrancy       │ High       │ persistent state write after call │
    ├────────┼──────────┼──────────────────┼────────────┼───────────────────────────────────┤
    │      0 │        0 │ Assert Violation │ Medium     │ assertion violation               │
    ╘════════╧══════════╧══════════════════╧════════════╧═══════════════════════════════════╛


.. _MythX: https://mythx.io/
