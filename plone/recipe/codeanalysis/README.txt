Supported options
=================

The recipe supports the following options:

directory
    Description for ``option1``...

pre-commit hook
    Description for ``option2``...


Example usage
=============

Minimal buildout::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts = code-analysis
    ...
    ... [code-analysis]
    ... recipe = plone.recipe.codeanalysis
    ... directory = %(directory)s
    ... """ % {
    ...     'directory' : '${buildout:directory}/plone/recipe/codeanalysis',
    ... })

Running the buildout gives us a 'code-analysis' script that runs the entire
code analysis::

    >>> buildout_output_lower = system(buildout).lower()
    >>> '/sample-buildout/bin/code-analysis' in buildout_output_lower
    True

It is also possible to run single code analysis scripts::

    >>> '/sample-buildout/bin/code-analysis-flake8' in buildout_output_lower
    True
    >>> '/sample-buildout/bin/code-analysis-jshint' in buildout_output_lower
    True

Flake 8 is installed by the buildout, there is no need to install it on the
system::

    >>> '/sample-buildout/bin/flake8' in buildout_output_lower
    True
