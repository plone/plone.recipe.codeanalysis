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

Flake 8 is installed by the buildout script, there is no need to install it on
the system::

    >>> '/sample-buildout/bin/flake8' in buildout_output_lower
    True


Pre-commit hook
===============

If we have a git repository::

    >>> import subprocess
    >>> subprocess.call(['mkdir', '-p', '.git/hooks'])
    0

And run buildout again::

    >>> buildout_output_lower = system(buildout).lower()

Then the git pre-commit hook is installed::

    >>> 'install git pre-commit hook.' in buildout_output_lower
    True
