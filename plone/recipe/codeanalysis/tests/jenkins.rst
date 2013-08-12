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
    ... jenkins = %(jenkins)s
    ... """ % {
    ...     'directory' : '${buildout:directory}/plone/recipe/codeanalysis',
    ...     'jenkins': 'True',
    ... })
    >>> buildout_output_lower = system(buildout).lower()

The buildout creates a code-analysis directory where the output files for
Jenkins are stored::

    >>> import os
    >>> os.path.exists(os.path.join(os.getcwd(), 'parts', 'code-analysis'))
    True

If the jenkins param is set, the buildout creates a jenkins-code-analysis
script::

    >>> '/sample-buildout/bin/jenkins-code-analysis' in buildout_output_lower
    True
