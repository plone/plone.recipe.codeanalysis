Change history
==============

2.0b1 (2015-05-03)
------------------

- Allow usage of wildcards in exclude statements.
  [saily]

- Add ``check-manifest`` as new dependency and a basic check. Fixes #69
  [saily]

- Add a new option to disable ``jshint`` warning suppression, fixes #94.
  [saily]

- If an executable could not be found the code-analysis always failed. We've
  changed this behaviour to return True and succeed the code-analysis, this
  fixes #71.
  [saily]

- Exclude paths directly in ``find`` unix command which speeds up again a lot.
  [saily]

- Exclude empty strings in ``self.extensions`` which broke install with
  ``zc.buildout 1.7.1``. Fixes #115
  [saily]

- Add check for relative imports. Fixes #44
  [saily]


2.0a2 (2015-04-30)
------------------

- Replace manual comparisons of buildout options to ``False`` with a
  ``bool_option`` method.
  [saily]

- Removed some plugins and replaced them with ``flake8`` plugins. Please
  not the API change in buildout. Following options have been removed:

  - **utf8-headers** has been removed, replace it with ``flake8-coding`` if
    needed.
  - **utf8-headers-exclude**
  - **prefer-single-quotes** has been removed, replace it with
    ``flake8-quotes``.
  - **prefer-single-quotes-exclude**
  - **debug-statements** has some reduced functionality, because python
    debugger checks should be included using ``flake8-debugger`` extension which
    also checks for ``ipdb``.

  Fixes #112.
  [saily]

- Add missing tests for deprecated_aliases parser.
  [saily]

- Add new double quotes parser and add test for it. It now also supports
  # noqa statments and nested quotes.
  [saily]


2.0a1 (2015-04-27)
------------------

- Added multiprocessing. This will dramatically increase speed on large
  packages when using pre-commit hooks.
  [saily]

- Return correct exit codes for console-scripts, fixes #66.
  [saily]

- Refactor whole linters framework to use OO design patterns, inherit from
  ``Analyser`` abstract base class. This fixes #62
  [saily]

- Add bootstrap-buildout.py to flake8-exclude default. zc.buildout > 2 uses
  bootstrap-buildout.py instead of bootstrap.py.
  [timo]


1.1 (2014-12-04)
----------------

- Add a check to look for hasattr() calls, which are considered bad practice.
  [gforcada, jensens]

- Add option to store flake8 output if jenkins is False
  [Michael Davis]

- Fix find_files from utils to find files, not directories
  [do3cc]


1.0 (2014-12-04)
----------------

- Nothing changed since 1.0rc1.


1.0rc1 (2014-06-18)
-------------------

- Return a string to avoid TypeError when no file was checked with ``jscs``.
  [saily]

- Check import sorting in ``code_analysis_imports`` and add tests for
  clean and sorted imports.
  [saily]

- Refactor ``code_analysis_clean_lines`` to use a new method to retrieve
  files and avoid too complex violation.
  [saily]


1.0b8 (2014-06-05)
------------------

- Add ``clean-lines-exclude`` support and updated README.
  [saily]

- Added tests for clean-lines checks.
  [saily]

- Use indices for format() to support Python 2.6. This fixes #77.
  [timo]


1.0b7 (2014-05-04)
------------------

- Add Javascript Code Style Checker ``jscs`` support.
  [saily]

- Remove hard dependency on i18ndude and zptlint; this will reduce the number
  of Zope/Plone direct dependencies to make life happier to people using
  Pyramid and other web Python-based development frameworks (closes `#53`_).
  [hvelarde]

- Do not print out jshint and csslint output for Jenkins. Those files can
  become quite large.
  [timo]


1.0b6 (2013-10-16)
------------------

- Remove progress bullets from flake8 check.
  [timo]

- Improve the way to handle an exception if the command used in popen does
  not exist.
  [flohcim]


1.0b5 (2013-10-08)
------------------

- Fix code analysis method by making it call each check only if the option
  is activated.
  [flohcim]

- Keep backward compatibility with 'string-formatting' option.
  [hvelarde]

- Rename 'deprecated-alias' to 'deprecated-aliases' and keep backward
  compatibility.
  [hvelarde]


1.0b4 (2013-10-06)
------------------

- Implement Jenkins option on CSS Lint and JSHint.
  [hvelarde, ramiroluz]

- Rename 'deprecated-methods' to 'deprecated-alias'.
  [gforcada]

- Rename 'string-formatting' option to 'pep3101' to keep consistency.
  [hvelarde]

- Remove unused CSSLINT_IGNORE remainings.
  [timo]

- Simplify code analysis method and make it more readable.
  [timo]


1.0b3 (2013-09-12)
------------------

- Add return-status-codes option that allows to fail a CI-build on Travis.
  [timo]

- Make system wide installed csslint the default value for
  the csslint-bin option.
  [timo]


1.0b2 (2013-09-11)
------------------

- Deprecate 'csslint-quiet', 'csslint-ignore' and 'csslint-exclude-list'
  options; CSS Lint must be configured now using a '.csslintrc' file.
  'csslint-bin' option now defaults to ``bin/csslint``; documentation was
  updated (closes #20).
  [hvelarde]

- Implement removal of pre-commit hook (fixes #21).
  [hvelarde]


1.0b1 (2013-08-12)
------------------

- Workaround over JSHint limitations to avoid displaying warning messages as
  errors (closes #13).
  [hvelarde]

- Fix CSS Lint validation and implement new 'csslint-quiet' option.
  [hvelarde]

- Fix package distribution.
  [hvelarde]


1.0a1 (2013-08-04)
------------------

- Initial release.
  [timo]

.. _`#53`: https://github.com/plone/plone.recipe.codeanalysis/issues/53
