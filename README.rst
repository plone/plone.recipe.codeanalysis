.. contents::

.. image:: https://travis-ci.org/plone/plone.recipe.codeanalysis.png?branch=master
    :target: http://travis-ci.org/plone/plone.recipe.codeanalysis

Introduction
============

plone.recipe.codeanalysis provides static code analysis for buildout-based
Python projects. For now this includes flake8 and jshint. The recipe creates a
script to run the code analysis::

    bin/code-analysis

By default plone.recipe.codeanalysis also creates a git pre-commit hook, so
the code analysis is run automatically before each commit.

Code repository::

    https://github.com/plone/plone.recipe.codeanalysis

Issue Tracker::

    https://github.com/plone/plone.recipe.codeanalysis/issues


Supported options
=================

The recipe supports the following options:

**directory**
    Directory that is subject to the code analysis. This option is required.

**pre-commit-hook**
    If set to True, a git pre-commit hook is installed that runs the code
    analysis before each commit.

**flake8**
    If set to True, run Flake8 code analysis. Default is True.

**flake8-ignore**
    Skip errors or warnings. See `Flake8 documentation`_ for error codes.
    Default is None.

**flake8-exclude**
    Comma-separated filename and glob patterns default. Say you want to
    exclude bootstrap.py, setup.py and all collective.* and plone.* packages.
    Just set "flake8-exclude=bootstrap.py,docs,*.egg,setup.py,collective.*,
    plone.*" in your buildout configuration. Default is 
    'bootstrap.py,docs,*.egg'.

**flake8-max-complexity**
    McCabe complexity threshold. Default is 10.

**flake8-max-line-length**
    Set maximum allowed line length. Default is 79.

**jshint**
    If set to True, jshint code analysis is run. Default is False.

**jshint-bin**
    JSHint executable. Default is 'jshint'. If you have JSHint installed on
    your system and in your path, there is nothing to do. To install JSHint in
    your buildout, use the following::

        [jshint]
        recipe = gp.recipe.node
        npms = jshint
        scripts = jshint

    set jshint-bin to '${buildout:directory}/bin/jshint'.

**jshint-exclude**
    Exclude files matching the given filename pattern. Default is none.

**csslint**
    If set to True, CSSLint code analysis is run. Default is False.

**csslint-bin**
    CSSLint executable. Default is 'csslint'. If you have CSSLint installed on
    your system and in your path, there is nothing to do. To install CSSLint
    in your buildout, use the following::

        [csslint]
        recipe = gp.recipe.node
        npms = csslint
        scripts = csslint

    set csslint-bin to '${buildout:directory}/bin/csslint'.

**csslint-ignore**
    This option allows you to specify which CSSLint rules to turn off. The
    rules are represented as a comma-delimited list of rule IDs. By default,
    the following rules will be ignored as they are `considered useless`_::

    * adjoining-classes
    * floats
    * font-faces
    * font-sizes
    * ids
    * qualified-headings
    * unique-headings

    For a detailed list and description of the rules see
    `CSSLint documentation`_.

**csslint-exclude-list**
    This option specifies the files and directories CSSLint will ignore.
    Default is no exclude list.

    You can specify more than one file or directory using a comma, such as::

        csslint-exclude-list = style.css,extras/

.. Note::
    You should use the full path of the file or directory you want to exclude.

**zptlint**
    If set to True, zptlint code analysis is run. Default is False.

    Note that the buildout itself already depends on zptlint, so no extra
    configuration is needed.

**zptlint-bin**
    Set the path to a custom version of zptlint. Default is ``bin/zptlint``.

**deprecated-methods**
    If set to True, warnings about deprecated methods will be printed. Default
    is False.

**utf8-header**
    If set to True, Python files without a utf-8 header (like
    ``# -*- coding: utf-8 -*-``) will cause a warning. Default is False.

**clean-lines**
    If set to True, **any file** containing trailing spaces or tabs anywhere
    on the lines will cause a warning. Default is False.

**prefer-single-quotes**
    If set to True, Python files will be scanned searching for strings quoted
    with double quote signs (``"``). Default is False.

**string-formatting**
    If set to True, Python files will be scanned searching for old-style
    string formatting (i.e. ``'%s' % var``). See `PEP 3101`_. Default is
    False.

**imports**
    If set to True, checks that imports in Python files follow `plone.api
    conventions`_. Default is False.

**debug-statements**
    If set to True, scan Python files looking for debug-like statements.
    Default is False.

.. _`considered useless`: http://2002-2012.mattwilcox.net/archive/entry/id/1054/
.. _`CSSLint documentation`: https://github.com/stubbornella/csslint/wiki/Rules
.. _`Flake8 documentation`: http://flake8.readthedocs.org/en/latest/warnings.html#error-codes
.. _`PEP 3101`: http://www.python.org/dev/peps/pep-3101/
.. _`plone.api conventions`: http://ploneapi.readthedocs.org/en/latest/contribute/conventions.html#about-imports
