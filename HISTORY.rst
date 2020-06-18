=======
History
=======

1.6.1 [2020-06-16]
------------------

- Update :code:`mythx-models` dependency to omit stale warning


1.6.0 [2020-06-16]
------------------

- Disable model json schema validation and tests
- Various dependency upgrades


1.5.7 [2020-04-27]
------------------

- Add property checking middleware and tests
- Various dependency upgrades


1.5.6 [2020-04-21]
------------------

- Various critical dependency upgrades
- Fix bug where tests failed due to a data mismatch


1.5.5 [2020-02-24]
------------------

- Allow direct injection of domain model into client analyze method


1.5.4 [2020-02-20]
------------------

- Fix various dependency conflicts
- Add better documentation to readme file
- Update middleware type hints and documentation
- Update API module type hints and documentation
- Various dependency upgrades


1.5.3 [2020-02-10]
------------------

- Handle ambiguous :code:`MYTHX_API_URL` declarations
- Various dependency upgrades


1.5.2 [2020-01-30]
------------------

- Add additional analysis/group list filter parameters
- Various dependency upgrades


1.5.1 [2020-01-29]
------------------

- Remove trial user support as it has been dropped from the API


1.5.0 [2020-01-29]
------------------

- Add pypy3 tests in Travis CI
- Add additional query param support to analysis list handler
- Add various test suite improvements
- Drop support for Python 3.5 and add support for Python 3.8
- Remove stale parameter config options
- Remove stale configuration object support
- Improve PyPI trove classifiers
- Various dependency upgrades


1.4.1 [2019-11-19]
------------------

- Extend status code range for failure check in API handler


1.4.0 [2019-11-19]
------------------

- Fix bug where empty query parameters were sent to the API
- Introduce group ID/name middleware
- Add group status support in client
- Add group creation/sealing support in client
- Add group list support in client
- Fix dependency conflict between :code:`mythx-cli` and :code:`mythx-models`
- Various dependency upgrades

1.3.2 [2019-10-04]
------------------

- Update :code:`mythx-models` to 1.4.1


1.3.1 [2019-10-04]
------------------

- Update pytest from 5.1.2 to 5.2.0
- Update :code:`mythx-models` to 1.4.0

1.3.0 [2019-09-20]
------------------

- Remove the PythX CLI PoC
- Add PSA about deprecation and link to new :code:`mythx-cli` repository

1.2.6 [2019-09-19]
------------------

- Update twine from 1.14.0 to 1.15.0
- Bump :code:`mythx-models` to 1.3.5

1.2.5 [2019-09-15]
------------------

- Update twine from 1.13.0 to 1.14.0
- Clean up dependencies
- Bump :code:`mythx-models` to 1.3.3

1.2.4 [2019-09-06]
------------------

- Bump :code:`mythx-models` to 1.3.2
- Add support to fetch analysis result input by UUID

1.2.3 [2019-09-05]
------------------

- Add an auth check override to handle situations where only the access token is given

1.2.2 [2019-08-30]
------------------

- Update :code:`mythx-models` to 1.3.1

1.2.1 [2019-08-29]
------------------

- Update :code:`mythx-models` to 1.3.0

1.2.0 [2019-08-26]
------------------

- Add `mythx-models <https://github.com/dmuhs/mythx-models>`_ integration

1.1.8 [2019-06-05]
------------------

- Add debug flag to CLI
- Add support for the :code:`clientToolName` response field
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
