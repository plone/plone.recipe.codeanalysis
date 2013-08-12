Jenkins Code Analysis
=====================

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
    >>> buildout_output_lower = system(buildout).lower()

The buildout creates a code-analysis directory where the output files for
Jenkins are stored::

    >>> import os
    >>> os.path.exists(os.path.join(os.getcwd(), 'parts', 'code-analysis'))
    True
