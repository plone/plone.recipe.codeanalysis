.. contents::

.. image:: https://travis-ci.org/plone/plone.recipe.codeanalysis.png?branch=master
    :target: http://travis-ci.org/plone/plone.recipe.codeanalysis

Introduction
============

plone.recipe.codeanalysis provides static code analysis for Buildout-based
Python projects, including `flake8`_, `JSHint`_, `CSS Lint`_, `zptlint`_, and
other code checks.

This buildout recipe creates a script to run the code analysis::

    bin/code-analysis

By default plone.recipe.codeanalysis also creates a git pre-commit hook, in
order to run the code analysis automatically before each commit.


Installation
============

Just add a code-analysis section to your buildout.cfg::

    [buildout]
    parts += code-analysis

    [code-analysis]
    recipe = plone.recipe.codeanalysis
    directory = ${buildout:directory}/src

The directory option is not required. Though, if you don't specify a directory
the code analysis will check every file in your buildout directory.


Links
=====

Code repository:

    https://github.com/plone/plone.recipe.codeanalysis

Continuous Integration:

    https://travis-ci.org/plone/plone.recipe.codeanalysis

Issue Tracker:

    https://github.com/plone/plone.recipe.codeanalysis/issues


Supported options
=================

The recipe supports the following options:

**directory**
    Directory that is subject to the code analysis.

**pre-commit-hook**
    If set to True, a git pre-commit hook is installed that runs the code
    analysis before each commit.

**flake8**
    If set to True, run Flake8 code analysis. Default is ``True``.

**flake8-ignore**
    Skip errors or warnings. See `Flake8 documentation`_ for error codes.
    Default is none.

**flake8-exclude**
    Comma-separated filename and glob patterns default. Say you want to
    exclude bootstrap.py, setup.py and all collective.* and plone.* packages.
    Just set "flake8-exclude=bootstrap.py,docs,*.egg,setup.py,collective.*,
    plone.*" in your buildout configuration. Default is
    ``bootstrap.py,docs,*.egg``.

**flake8-max-complexity**
    McCabe complexity threshold. Default is ``10``.

**flake8-max-line-length**
    Set maximum allowed line length. Default is ``79``.

**jshint**
    If set to True, jshint code analysis is run. Default is ``False``. Note
    that plone.recipe.codeanalysis requires jshint >= 1.0.

**jshint-bin**
    JSHint executable. Default is ``jshint``. If you have JSHint installed on
    your system and in your path, there is nothing to do. To install JSHint in
    your buildout, use the following::

        [jshint]
        recipe = gp.recipe.node
        npms = jshint
        scripts = jshint

    set jshint-bin to '${buildout:directory}/bin/jshint'.

**jshint-exclude**
    Allows you to specify directories which you don't want to be linted.
    Default is none. If you want JSHint to skip some files you can list them
    in a file named ``.jshintignore``. See `JSHint documentation`_ for more
    details.

**csslint**
    If set to True, CSS Lint code analysis is run. Default is ``False``.

    CSS Lint options should be configured using a ``.csslintrc`` file. A
    typical ``.csslintrc`` file will look like this::

        --format=compact
        --quiet
        --ignore=adjoining-classes,floats,font-faces,font-sizes,ids,qualified-headings,unique-headings
        --exclude-list=foo/bar/static/third-party.css

    This typical configuration includes a list of CSS rules that will be
    ignored as they are `considered useless`_.

    See `CSS Lint documentation`_ for a detailed list and description of the
    rules.

**csslint-bin**
    Set the path to a custom version of CSS Lint. Default is ``bin/csslint``.

    If you have CSS Lint installed in your system and path, set csslint-bin to
    'csslint'. To install CSS Lint in your buildout, use the following::

        [csslint]
        recipe = gp.recipe.node
        npms = csslint
        scripts = csslint

**zptlint**
    If set to True, zptlint code analysis is run. Default is ``False``.

    Note that the buildout itself already depends on zptlint, so no extra
    configuration is needed.

**zptlint-bin**
    Set the path to a custom version of zptlint. Default is ``bin/zptlint``.

**deprecated-methods**
    If set to True, warnings about deprecated methods will be printed. Default
    is False.

**utf8-header**
    If set to True, Python files without a utf-8 header (like
    ``# -*- coding: utf-8 -*-``) will cause a warning. Default is ``False``.

**clean-lines**
    If set to True, **any file** containing trailing spaces or tabs anywhere
    on the lines will cause a warning. Default is ``False``.

**prefer-single-quotes**
    If set to True, Python files will be scanned searching for strings quoted
    with double quote signs (``"``). Default is ``False``.

**string-formatting**
    If set to True, Python files will be scanned searching for old-style
    string formatting (i.e. ``'%s' % var``). See `PEP 3101`_. Default is
    ``False``.

**imports**
    If set to True, checks that imports in Python files follow `plone.api
    conventions`_. Default is ``False``.

**debug-statements**
    If set to True, scan Python files looking for debug-like statements.
    Default is ``False``.


Known Issues
============

JSHint "ERROR: Unknown option --verbose"::

    JSHint                [ OK ]
    ERROR: Unknown option --verbose

Upgrade JSHint to latest version (>= 1.0) to fix this issue, e.g.::

    $ sudo npm install -g jshint

.. _`considered useless`: http://2002-2012.mattwilcox.net/archive/entry/id/1054/
.. _`CSS Lint documentation`: https://github.com/stubbornella/csslint/wiki/Rules
.. _`CSS Lint`: http://csslint.net/
.. _`Flake8 documentation`: http://flake8.readthedocs.org/en/latest/warnings.html#error-codes
.. _`flake8`: https://pypi.python.org/pypi/flake8
.. _`JSHint documentation`: http://jshint.com/docs/
.. _`JSHint`: http://www.jshint.com/
.. _`PEP 3101`: http://www.python.org/dev/peps/pep-3101/
.. _`plone.api conventions`: http://ploneapi.readthedocs.org/en/latest/contribute/conventions.html#about-imports
.. _`zptlint`: https://pypi.python.org/pypi/zptlint
