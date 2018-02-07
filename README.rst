.. image:: https://img.shields.io/pypi/status/plone.recipe.codeanalysis.svg
    :target: https://pypi.python.org/pypi/plone.recipe.codeanalysis/
    :alt: Egg Status

.. image:: https://img.shields.io/travis/plone/plone.recipe.codeanalysis/master.svg
    :target: http://travis-ci.org/plone/plone.recipe.codeanalysis
    :alt: Travis Build Status

.. image:: https://img.shields.io/coveralls/plone/plone.recipe.codeanalysis/master.svg
    :target: https://coveralls.io/r/plone/plone.recipe.codeanalysis
    :alt: Test Coverage

.. image:: https://img.shields.io/pypi/dm/plone.recipe.codeanalysis.svg
    :target: https://pypi.python.org/pypi/plone.recipe.codeanalysis/
    :alt: Downloads

.. image:: https://img.shields.io/pypi/pyversions/plone.recipe.codeanalysis.svg
    :target: https://pypi.python.org/pypi/plone.recipe.codeanalysis/
    :alt: Python Versions

.. image:: https://img.shields.io/pypi/v/plone.recipe.codeanalysis.svg
    :target: https://pypi.python.org/pypi/plone.recipe.codeanalysis/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/l/plone.recipe.codeanalysis.svg
    :target: https://pypi.python.org/pypi/plone.recipe.codeanalysis/
    :alt: License

.. contents::

Introduction
============

``plone.recipe.codeanalysis`` provides static code analysis for Buildout-based
Python projects, including `flake8`_, `JSHint`_, `CSS Lint`_, and
other code checks.

This buildout recipe creates a script to run the code analysis::

    bin/code-analysis

By default ``plone.recipe.codeanalysis`` also creates a git pre-commit hook, in
order to run the code analysis automatically before each commit.

``plone.recipe.codeanalysis`` comes with a Jenkins integration, that allows to
use the same code analysis settings on your local machine as well as on
Jenkins.

It also allows to run code analysis to any arbitrary folder::

    bin/code-analysis src/Products.CMFPlone


Installation
============

Just add a code-analysis section to your buildout.cfg:

.. code-block:: ini

    [buildout]
    parts += code-analysis

    [code-analysis]
    recipe = plone.recipe.codeanalysis
    directory = ${buildout:directory}/src

The directory option is not required. Though, if you don't specify a directory
the code analysis will check every file in your buildout directory.

This configuration is helpful for working on already existing packages.
If you create a new package you might want to enable all checks.
This configuration looks like this:

.. code-block:: ini

    [code-analysis]
    recipe = plone.recipe.codeanalysis[recommended]
    multiprocessing = True
    jenkins = False
    directory =
        ${buildout:directory}/src
    pre-commit-hook = True
    # JS
    jshint = True
    jshint-bin = ${buildout:bin-directory}/jshint
    jshint-suppress-warnings = False
    jscs = True
    jscs-bin = ${buildout:bin-directory}/jscs
    jscs-exclude =
        ${buildout:directory}/dev/bower_components
        ${buildout:directory}/node_modules
    # CSS
    csslint = True
    csslint-bin = ${buildout:bin-directory}/csslint
    # ZPT
    zptlint = True
    zptlint-bin = ${buildout:bin-directory}/zptlint
    # XML (there is not xmllint-bin, it uses lxml)
    xmllint = True
    # TS
    tslint = True
    tslint-bin = ${buildout:directory}/bin/tslint
    tslint-exclude = ${:jscs-exclude}
    # Conventions
    clean-lines = True
    clean-lines-exclude = ${:jscs-exclude}
    # i18n
    find-untranslated = True
    i18ndude-bin = ${buildout:bin-directory}/i18ndude
    return-status-codes = True
    flake8-exclude = bootstrap.py,bootstrap-buildout.py,docs,*.egg,*.cpy,*.vpy,overrides

    [node]
    recipe = gp.recipe.node
    npms = csslint jshint jscs tslint
    scripts = csslint jshint jscs tslint

``[recommended]`` extra
=======================

This extra enables a host of flake8 plugins.
They are mostly coding `Plone's styleguide`_ (specially the Python section).

These are the current extras installed:

- flake8-blind-except: warns about catching any exception, i.e ``except:``
- flake8-coding: warns about python files with missing coding header
- flake8-debugger: warns about debug statements found in code (like pdb...)
- flake8-deprecated: warns about deprecated method calls
- flake8-isort: warns about imports not sorted properly (note that an `extra configuration`_ is needed)
- flake8-pep3101: warns about old-style formatting, i.e ``'format a %s' % string``
- flake8-plone-api: warns about code that could be replaced by plone.api calls (note that this is forbidden for Plone core packages)
- flake8-plone-hasattr: warns about using ``hasattr`` as it shallows exceptions
- flake8-print: warns about ``print`` being used
- flake8-quotes: warns about using double quotes (plone style guide says single quotes)
- flake8-string-format: warns about errors on string formatting
- flake8-todo: warns if there are ``TODO``, ``XXX`` found on the code
- flake8-commas: warns if the last element on a method call, list or dictionary does not end with a comma

Jenkins Installation
====================

plone.recipe.codeanalysis provides a Jenkins setting that allows to run it on a Jenkins CI server and to process and integrate the output via the
`Jenkins Violations plugin`_.

Usually you don't want the recipe to create Jenkins output files on your
local machine. Therefore it makes sense to enable the Jenkins output only
on the CI machine. To do so, just create a jenkins.cfg that extends and
overrides the default buildout file (that includes the other settings):

.. code-block:: ini

    [buildout]
    parts += code-analysis

    [code-analysis]
    recipe = plone.recipe.codeanalysis
    jenkins = True

The Jenkins job itself should run ``bin/code-analysis``::

    python bootstrap.py -c jenkins.cfg
    bin/buildout -c jenkins.cfg
    bin/jenkins-test --all
    bin/code-analysis

The `Jenkins Violations plugin`_ needs to be configured to read the output
files generated by this configuration.

pep8 (to read the flake8 output)::

    **/parts/code-analysis/flake8.log

csslint::

    **/parts/code-analysis/csslint.xml

jslint (to read the jshint output)::

    **/parts/code-analysis/jshint.xml

checkstyle (to read the jscs output)::

    **/parts/code-analysis/jscs.xml

Filesystem output
=================

If jenkins is set to False, you can still store the output on the filesystem by setting ``flake8-filesystem = True``.
This is ignored if jenkins is set to True.

output::

    **/parts/code-analysis/flake8.txt

Links
=====

Code repository:

    https://github.com/plone/plone.recipe.codeanalysis

Continuous Integration:

    https://travis-ci.org/plone/plone.recipe.codeanalysis

Issue Tracker:

    https://github.com/plone/plone.recipe.codeanalysis/issues


Supported options
=================

If you need to bypass checks for some reasons on a specific line you may use
``# noqa`` in Python or ``// noqa`` in Javascript files. This works for most
of our checks.

The recipe supports the following options:

**directory**
    Directory that is subject to the code analysis.

**pre-commit-hook**
    If set to True, a git pre-commit hook is installed that runs the code
    analysis before each commit. Default is ``True``.

**multiprocessing**
    If set to ``True``, ``code-analysis`` will fork multiple processes and run
    all linters in parallel. This will dramatically increase speed on a
    multi-core system, specially when using ``code-analysis`` as pre-commit
    hook. Default is ``False``.

**jenkins**
    If set to True, the flake8, jshint and csslint code analysis steps will
    write output files that can be processed by the
    `Jenkins Violations plugin`_. Default is ``False``.

**flake8-filesystem**
    If set to True, the flake8 code analysis step will
    write an output file. Ignored if jenkins is True. Default is ``False``.

**flake8**
    If set to True, run Flake8 code analysis. Default is ``True``.

**flake8-extensions**
    Flake8 now takes advantage of ``flake8`` extension system. Default is none.
    If ``flake8`` is set to False, this option will be ignored. Example to
    supercharge with some extensions:

.. code-block:: ini

    [code-analysis]
    recipe = plone.recipe.codeanalysis
    flake8 = True
    flake8-extensions =
        flake8-blind-except
        flake8-coding
        flake8-debugger
        flake8-quotes
        pep8-naming

All through flake8 extensions raised validation errors may be suppressed
using the ``flake8-ignore`` option.

**flake8-ignore**
    Skip errors or warnings. See `Flake8 documentation`_ for error codes.
    Default is none.

**flake8-exclude**
    Comma-separated filename and glob patterns default. Say you want to
    exclude bootstrap.py, setup.py and all collective.* and plone.* packages.
    Just set ``flake8-exclude=bootstrap.py,docs,*.egg,setup.py,collective.*,plone.*``
    in your buildout configuration. Default is
    ``bootstrap.py,bootstrap-buildout.py,docs,*.egg``.

**flake8-max-complexity**
    McCabe complexity threshold. Default is ``10``.

**flake8-max-line-length**
    Set maximum allowed line length. Default is ``79``.

.. note::
   You can add additional flake8 options as long as they are valid for flake8
   itself or any of its plugins. Just prefix them with ``flake8-``.

   For example, if you are using ``pep8-naming`` and want to change the list
   of ignored names, add the following line on your buildout.cfg:
   ``flake8-ignore-names = setUp,tearDown,setUpClass,tearDownClass``

   Look at flake8 documentation and its plugins to see which options are available.

**check-manifest**
    If set to True, ``check-manifest`` will be run to check you MANIFEST.in
    file. Default is ``False``.

**check-manifest-directory**
    Default is ``.`` which means check the current package where you included
    code-analysis in buildout.

    EXPERIMENTAL: For project buildouts where you use several source
    packages you may want to enter multiple directories or use
    ``${buildout:develop}`` to include all your development packages.

**jshint**
    If set to True, jshint code analysis is run. Default is ``False``. Note
    that plone.recipe.codeanalysis requires jshint >= 1.0.

**jshint-bin**
    JSHint executable. Default is ``jshint``. If you have JSHint installed on
    your system and in your path, there is nothing to do. To install JSHint in
    your buildout, use the following:

.. code-block:: ini

    [jshint]
    recipe = gp.recipe.node
    npms = jshint
    scripts = jshint

set jshint-bin to ``${buildout:bin-directory}/jshint``.

**jshint-exclude**
    Allows you to specify directories which you don't want to be linted.
    Default is none. If you want JSHint to skip some files you can list them
    in a file named ``.jshintignore``. See `JSHint documentation`_ for more
    details.

**jshint-suppress-warnings**
    By default warnings of jshint are suppressed and not shown. You may disable
    this by setting to False, default is ``True`` for backward compatibility
    reasons.

**jscs**
    If set to True, jscs code analysis is run. Default is ``False``.

    JavaScript Code Style options should be configured using a ``.jscs.json``
    file. You should align your javascript code to the next generation of
    Plone's javascript framework Mockup_ and take it's ``.jscs.json`` file
    which is available here:
    https://github.com/plone/mockup/blob/master/mockup/.jscs.json

    All configuration options are documented on the `jscs website`_.

**jscs-bin**
    Set the path to a custom version of JSCS, e.g. ``/usr/local/bin/jscs``.

    If you have Javascript Code Style Checker installed in your system and
    path, you have nothing to do. To install with Buildout, add the following
    section to your buildout and set jscs-bin to
    ``{buildout:bin-directory}/jscs``:

.. code-block:: ini

    [jscs]
    recipe = gp.recipe.node
    npms = jscs
    scripts = jscs

**jscs-exclude**
    Allows you to specify directories and/or files which you don't want to be
    checked. Default is none. Note that these directories have to be given in
    absolute paths, use ``${buildout:directory}/foo/bar/static/js-3rd-party``
    for example.

**csslint**
    If set to True, CSS Lint code analysis is run. Default is ``False``.

    CSS Lint options should be configured using a ``.csslintrc`` file. A
    typical ``.csslintrc`` file will look like this::

        --format=compact
        --quiet
        --ignore=adjoining-classes,floats,font-faces,font-sizes,ids,qualified-headings,unique-headings
        --exclude-list=foo/bar/static/third-party.css

    This typical configuration includes a list of CSS rules that will be
    ignored as they are `considered useless`_.

    See `CSS Lint documentation`_ and `CSS Lint command-line interface`_ for a
    detailed list and description of the rules.

**csslint-bin**
    Set the path to a custom version of CSS Lint, e.g. ``/usr/local/bin/csslint``.

    If you have CSS Lint installed in your system and path, you have nothing
    to do. To install CSS Lint with Buildout, add the following section to
    your buildout and set csslint-bin to
    ``{buildout:bin-directory}/csslint``:

.. code-block:: ini

    [csslint]
    recipe = gp.recipe.node
    npms = csslint
    scripts = csslint

**csslint-exclude**
    Allows you to specify directories and/or files which you don't want to be
    checked. Default is none.

**scsslint**
    If set to True, `SCSS Lint`_ code analysis is run. Default is ``True``.

**csslint-bin**
    Set the path to a custom version of SCSS Lint.

    If you have CSS Lint installed in your system and path, you have nothing
    to do. To install CSS Lint with Buildout, add the following section to
    your buildout and set csslint-bin to
    ``{buildout:bin-directory}/csslint``:

.. code-block:: ini

    [rubygems]
    recipe = rubygemsrecipe
    gems = bundler scss_lint

**scsslint-configuration**

    SCSS Lint options can be configured, see `SCSS Lint`_ README.

**clean-lines**
    If set to True, **any file** containing trailing spaces or tabs anywhere
    on the lines will cause a warning. Default is ``False``.

**clean-lines-exclude**
    Allows you to specify directories and/or files which you don't want to be
    checked. Default is none.

**return-status-codes**
    If set to True, the ``bin/code-analysis`` script returns an error code
    that Continuous Integration servers (like Travis CI) can use to fail or
    pass a job, based on the code analysis output. Note that Jenkins usually
    does not need this option (this is better handled by the Jenkins
    Violations plugin). Note that this option does not have any effect on the
    other code analysis scripts. Default is ``False``.

i18ndude and zptlint support
----------------------------

To reduce the number of Zope/Plone direct dependencies, plone.recipe.codeanalysis no longer depends on `i18ndude`_ nor `zptlint`_;
in order to use the following options you have to install them on your
system:

**find-untranslated**
    If set to True, scan Zope templates to find untranslated strings.
    Default is ``False``.
    To use this you will need to set the ``i18ndude-bin`` option.

**find-untranslated-exclude**
    Allows you to specify directories and/or files which you don't want to be
    checked. Default is none.

**find-untranslated-no-summary**
    The report will contain only the errors for each file.
    Default is ``False``.

**i18ndude-bin**
    Set the path to a custom version of `i18ndude`_.
    Default is none.

**zptlint**
    If set to True, zptlint code analysis is run.
    Default is ``False``.
    To use this you will need to set the ``zptlint-bin`` option.

**zptlint-bin**
    Set the path to a custom version of `zptlint`_.
    Default is none.

**zptlint-exclude**
    Allows you to specify directories and/or files which you don't want to be
    checked. Default is none.

XMLLint support
---------------

XMLLint uses ``lxml`` for xml parsing. There is not ``xmllint-bin``.
Buildout options:

**xmllint**
    If set to True, XMLLint code analysis is run. Default is ``True``.


Known Issues
============

JSHint "ERROR: Unknown option --verbose"::

    JSHint                [ OK ]
    ERROR: Unknown option --verbose

Upgrade JSHint to latest version (>= 1.0) to fix this issue, e.g.::

    $ sudo npm install -g jshint


JSHint "ERROR: Unknown option --exclude"::

    JSHint                [ OK ]
    ERROR: Unknown option --exclude

Upgrade JSHint to latest version (>= 2.1.6) to fix this issue, e.g.::

    $ sudo npm install -g jshint


.. _`considered useless`: http://2002-2012.mattwilcox.net/archive/entry/id/1054/
.. _`CSS Lint documentation`: https://github.com/CSSLint/csslint/wiki/Rules
.. _`CSS Lint command-line interface`: https://github.com/CSSLint/csslint/wiki/Command-line-interface
.. _`CSS Lint`: http://csslint.net/
.. _`SCSS Lint`: https://github.com/brigade/scss-lint
.. _`Flake8 documentation`: http://flake8.readthedocs.org/en/latest/warnings.html#error-codes
.. _`Jenkins Violations plugin`: https://wiki.jenkins-ci.org/display/JENKINS/Violations
.. _`flake8`: https://pypi.python.org/pypi/flake8
.. _`JSHint documentation`: http://jshint.com/docs/
.. _`JSHint`: http://www.jshint.com/
.. _`PEP 3101 (Advanced String Formatting)`: http://www.python.org/dev/peps/pep-3101/
.. _`plone.api conventions`: http://ploneapi.readthedocs.org/en/latest/contribute/conventions.html#about-imports
.. _`zptlint`: https://pypi.python.org/pypi/zptlint
.. _`i18ndude`: https://pypi.python.org/pypi/i18ndude
.. _`Unit testing framework documentation`: http://docs.python.org/2/library/unittest.html#deprecated-aliases
.. _`Mockup`: https://github.com/plone/mockup
.. _`jscs website`: https://www.npmjs.org/package/jscs
.. _`Plone's styleguide`: http://docs.plone.org/develop/styleguide/
.. _`extra configuration`: https://raw.githubusercontent.com/plone/plone.recipe.codeanalysis/master/.isort.cfg
