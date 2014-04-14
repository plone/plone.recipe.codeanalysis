zptlint Code Analysis Test
==========================

zptlint code analysis is included by default::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts = code-analysis
    ...
    ... [code-analysis]
    ... recipe = plone.recipe.codeanalysis
    ... directory = ${buildout:directory}/plone/recipe/codeanalysis
    ... """
    ... )
    >>> buildout_output_lower = system(buildout).lower()

zptlint code analysis script has been created::

    >>> '/sample-buildout/bin/code-analysis-zptlint' in buildout_output_lower
    True
