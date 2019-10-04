=======
History
=======

1.3.1 [2019-10-04]
------------------

- Update pytest from 5.1.2 to 5.2.0
- Update `mythx-models` to 1.4.0

1.3.0 [2019-09-20]
------------------

- Remove the PythX CLI PoC
- Add PSA about deprecation and link to new `mythx-cli` repository

1.2.6 [2019-09-19]
------------------

- Update twine from 1.14.0 to 1.15.0
- Bump `mythx-models` to 1.3.5

1.2.5 [2019-09-15]
------------------

- Update twine from 1.13.0 to 1.14.0
- Clean up dependencies
- Bump `mythx-models` to 1.3.3

1.2.4 [2019-09-06]
------------------

- Bump `mythx-models` to 1.3.2
- Add support to fetch analysis result input by UUID

1.2.3 [2019-09-05]
------------------

- Add an auth check override to handle situations where only the access token is given

1.2.2 [2019-08-30]
------------------

- Update `mythx-models` to 1.3.1

1.2.1 [2019-08-29]
------------------

- Update `mythx-models` to 1.3.0

1.2.0 [2019-08-26]
------------------

- Add `mythx-models <https://github.com/dmuhs/mythx-models>`_ integration

1.1.8 [2019-06-05]
------------------

- Add debug flag to CLI
- Add support for the `clientToolName` response field
- Add support for the new source list format validation
- Update the bumpversion expression to support black formatting

1.1.7 [2019-04-20]
------------------

- Add main docstring description


1.1.6 [2019-04-19]
------------------

- Add :code:`mainSource` support to CLI
- Fix bug where submission object was malformed ("AST" -> "ast")
- Upgrade pytest dependency


1.1.5 [2019-04-16]
------------------

- Add middleware to disable analysis cache
- Add CLI support to analyze compiled Truffle projects
- Fix bug where reports were not completely shown
- Update the authentication data format
- Add support for the mainSource field
- Add shortcut to inject middlewares in Client


1.1.4 [2019-03-28]
------------------

- Fix issue in schema detection
- Upgrade Sphinx dependency


1.1.3 [2019-03-25]
------------------

- Initial release!
- 100% branch coverage achieved
- 100% doc coverage achieved
- Examples provided in repo readme
- Automatic PyPI deployment on version tag change
