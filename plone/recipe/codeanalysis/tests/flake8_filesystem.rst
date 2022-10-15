Filesystem Code Analysis
========================

Minimal buildout::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts = code-analysis
    ...
    ... [code-analysis]
    ... recipe = plone.recipe.codeanalysis
    ... directory = %(directory)s
    ... flake8-filesystem = %(flake8-filesystem)s
    ... """ % {
    ...     'directory' : '${buildout:directory}/plone/recipe/codeanalysis',
    ...     'flake8-filesystem': 'True',
    ... })
    >>> buildout_output_lower = system(buildout).lower()

The buildout creates a code-analysis directory where the output files are stored::

    >>> import os
    >>> os.path.exists(os.path.join(os.getcwd(), 'parts', 'code-analysis'))
    True

When running the code-analysis script::

    >>> import subprocess
    >>> f = open("bla.txt", "w")
    >>> subprocess.call(['bin/code-analysis'], stdout=f)
    0
    >>> f.close()

a flake8 log file is written to the 'code-analysis' directory::

    >>> os.path.exists(os.path.join(os.getcwd(), 'parts', 'code-analysis', 'flake8.txt'))
    True
