Javascript Code Style Checker Test
==================================

JSCS code analysis is included by default::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts = code-analysis
    ...
    ... [code-analysis]
    ... recipe = plone.recipe.codeanalysis
    ... directory = %(directory)s
    ... jscs = True
    ... """ % {
    ...     'directory' : '${buildout:directory}/plone/recipe/codeanalysis',
    ... })
    >>> buildout_output_lower = system(buildout).lower()

JSCS code analysis script has been created::

    >>> '/sample-buildout/bin/code-analysis-jscs' in buildout_output_lower
    True
