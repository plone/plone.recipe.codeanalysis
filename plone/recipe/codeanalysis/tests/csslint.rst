Flake8 Code Analysis Test
=========================

CSS Lint code analysis is not included by default::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts = code-analysis
    ...
    ... [code-analysis]
    ... recipe = plone.recipe.codeanalysis
    ... directory = %(directory)s
    ... csslint = True
    ... """ % {
    ...     'directory' : '${buildout:directory}/plone/recipe/codeanalysis',
    ... })
    >>> buildout_output_lower = system(buildout).lower()

CSS Lint code analysis script has been created::

    >>> '/sample-buildout/bin/code-analysis-csslint' in buildout_output_lower
    True
