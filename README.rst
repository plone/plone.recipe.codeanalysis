.. contents::

.. image:: https://travis-ci.org/plone/plone.recipe.codeanalysis.png?branch=master

Introduction
============

plone.recipe.codeanalysis provides static code analysis for buildout-based Python projects. For now this includes flake8 and jshint. The recipe creates
a script to run the code analysis::

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

directory
    Directory that is subject to the code analysis. This option is required.

pre-commit-hook
    If set to True, a git pre-commit hook is installed that runs the code analysis before each commit.

flake8
    If set to True, run flake8 code analysis. Default is True.

flake8-ignore
    Skip errors or warnings. See http://flake8.readthedocs.org/en/latest/warnings.html#error-codes for error codes. Default is
    None.

flake8-exclude
    Comma-separated filename and glob patterns default. Say you want to
    exclude bootstrap.py, setup.py and all collective.* and plone.* packages. Just set "flake8-exclude=bootstrap.py,docs,*.egg,setup.py,collective.*,
    plone.*" in your buildout configuration. Default is 'bootstrap.py,docs,
    *.egg'.

flake8-complexity
    McCabe complexity threshold. Default is 10.

jshint
    If set to True, jshint code analysis is run. Default to False.

jshint-bin
    JSHint executable. Default is 'jshint'. If you have jshint installed on
    your system and in your path, there is nothing to do. If you install
    jshint in your buildout, e.g.::

        [node]
        recipe = gp.recipe.node
        npms = jshint
        url = http://nodejs.org/dist/v0.5.9/node-v0.5.9.tar.gz
        scripts = jshint

    set jshint-bin to '${buildout:directory}/bin/jshint'.

zptlint
    If set to True, zptlint code analysis is run. Default to False.

    Note that the buildout itself already depends on zptlint, so no extra
    configuration is needed.

zptlint-bin
    Set the path to a custom version of zptlint. Defaults to ``bin/zptlint``.

deprecated-methods
    If set to True, warnings about deprecated methods will be printed. Default
    to False.

utf8-header
    If set to True, python files without a utf-8 header (like
    ``# -*- coding: utf-8 -*-``) will cause a warning. Default to False.

clean-lines
    If set to True, **any file** containing trailing spaces or tabs anywhere
    on the lines will cause a warning. Default to False.

prefer-single-quotes
    If set to True, python files will be scanned searching for strings quoted
    with double quote signs (``"``). Default to False.

string-formatting
    If set to True, python files will be scanned searching for old-style string
    formatting (i.e. ``'%s' % var``). See `PEP 3101
    <http://www.python.org/dev/peps/pep-3101/>`_. Default to False.

imports
    If set to True, checks that imports in python files follow `the Plone style
    guide <http://ploneapi.readthedocs.org/en/latest/contribute/conventions.html#about-imports>`_.
    Default to False.

debug-statements
    If set to True, scan python files looking for debug-like statements.
    Default to False.
