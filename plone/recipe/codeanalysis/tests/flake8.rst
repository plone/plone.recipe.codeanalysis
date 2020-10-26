Flake8 Code Analysis Test
=========================

Flake 8 code analysis is included by default::

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
    >>> buildout_output_lower = system(buildout).lower()

Flake 8 code analysis script has been created::

    >>> '/sample-buildout/bin/code-analysis-flake8' in buildout_output_lower
    True
