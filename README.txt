.. contents::

Introduction
============

plone.recipe.codeanalysis provides static code analysis for buildout-based Python projects. For now this includes flake8 and jshint. The recipe creates
a script to run the code analysis::

    bin/code-analysis

By default plone.recipe.codeanalysis also creates a git pre-commit hook, so
the code analysis is run automatically before each commit.


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
    Skip errors or warnings. See http://flake8.readthedocs.org/en/latest/warnings.html#error-codes for error codes.

flake8-exclude
    Comma-separated filename and glob patterns default (e.g. .svn,CVS,.bzr,.hg,.git,__pycache).

flake8-complexity
    McCabe complexity threshold.

jshint
    If set to True, jshint code analysis is run. Default to False.

jshint-bin
    JSHint executable. Default is 'jshint'. If you have jshint installed on
    your system and in your path, there is nothing to do. If you install
    jshint in your buildout, e.g.:

        [node]
        recipe = gp.recipe.node
        npms = jshint
        url = http://nodejs.org/dist/v0.5.9/node-v0.5.9.tar.gz
        scripts = jshint

    set jshint-bin to '${buildout:directory}/bin/jshint'.
