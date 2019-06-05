=======
History
=======

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
