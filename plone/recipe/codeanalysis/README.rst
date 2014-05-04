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

Deprecated aliases analysis script is installed::

    >>> '/sample-buildout/bin/code-analysis-deprecated-aliases' in buildout_output_lower
    True

The script to check if python files have an utf-8 encoding header is installed::

    >>> '/sample-buildout/bin/code-analysis-utf8-header' in buildout_output_lower
    True

The script to warn about trailing spaces or tabs on files is installed::

    >>> '/sample-buildout/bin/code-analysis-clean-lines' in buildout_output_lower
    True

Double quotes checker script is installed::

    >>> '/sample-buildout/bin/code-analysis-prefer-single-quotes' in buildout_output_lower
    True

The script to check for old style string formatting is installed::

    >>> '/sample-buildout/bin/code-analysis-pep3101' in buildout_output_lower
    True

The script to check for plone.api style imports is installed::

    >>> '/sample-buildout/bin/code-analysis-imports' in buildout_output_lower
    True

The script to check for debug-like statements in python code is installed::

    >>> '/sample-buildout/bin/code-analysis-debug-statements' in buildout_output_lower
    True

The script to check for untranslated strings in templates is installed::

    >>> '/sample-buildout/bin/code-analysis-find-untranslated' in buildout_output_lower
    True

By default a git pre-commit hook is installed. Though, this does not work if
the current directory is not a git repository::

    >>> 'unable to create git pre-commit hook, this does not seem to be a git repository' in buildout_output_lower
    True

If we have a git repository::

    >>> import subprocess
    >>> subprocess.call(['mkdir', '-p', '.git/hooks'])
    0

And run buildout again::

    >>> buildout_output_lower = system(buildout).lower()

Then the git pre-commit hook has been installed::

    >>> 'install git pre-commit hook.' in buildout_output_lower
    True
