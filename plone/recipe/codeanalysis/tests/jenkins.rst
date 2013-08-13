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

When running the code-analysis script::

    >>> import subprocess
    >>> subprocess.call(['bin/code-analysis'])
    0

a flake8 log file is written to the 'code-analyis' directory::

    >>> os.path.exists(os.path.join(os.getcwd(), 'parts', 'code-analysis', 'flake8.log'))
    True
