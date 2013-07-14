Supported options
=================

The recipe supports the following options:

directory
    Directory that is subject to the code analysis. This option is required.

pre-commit-hook
    If set to True, a git pre-commit hook is installed that runs the code analysis before each commit.

flake8
    If set to True, run flake8 code analysis. Default is True.

flake8-ignore
    Skip errors or warnings. See http://flake8.readthedocs.org/en/latest/warnings.html#error-codes for error codes.

flake8-exclude
    Comma-separated filename and glob patterns default (e.g. .svn,CVS,.bzr,.hg,.git,__pycache).

flake8-complexity
    McCabe complexity threshold.

jshint
    If set to True, jshint code analysis is run. Default to False.

jshint-bin
    JSHint executable. Default is 'jshint'. If you have jshint installed on
    your system and in your path, there is nothing to do. If you install
    jshint in your buildout, e.g.:

        [node]
        recipe = gp.recipe.node
        npms = jshint
        url = http://nodejs.org/dist/v0.5.9/node-v0.5.9.tar.gz
        scripts = jshint

    set jshint-bin to '${buildout:directory}/bin/jshint'.


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
    >>> buildout_output_lower
    >>> '/sample-buildout/bin/code-analysis' in buildout_output_lower
    True

It is also possible to run single code analysis scripts::

    >>> '/sample-buildout/bin/code-analysis-flake8' in buildout_output_lower
    True
    >>> '/sample-buildout/bin/code-analysis-jshint' in buildout_output_lower
    True

Flake 8 is installed by the buildout, there is no need to install it on the
system::

    >>> '/sample-buildout/bin/flake8' in buildout_output_lower
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
