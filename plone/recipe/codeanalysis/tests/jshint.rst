JSHint Code Analysis Test
=========================

JSHint code analysis is included by default::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts = code-analysis
    ...
    ... [code-analysis]
    ... recipe = plone.recipe.codeanalysis
    ... directory = %(directory)s
    ... jshint = True
    ... """ % {
    ...     'directory' : '${buildout:directory}/plone/recipe/codeanalysis',
    ... })
    >>> buildout_output_lower = system(buildout).lower()

JSHint code analysis script has been created::

    >>> '/sample-buildout/bin/code-analysis-jshint' in buildout_output_lower
    True
