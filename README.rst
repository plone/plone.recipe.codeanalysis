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
    return-status-codes = True
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
    # Chameleon uses XML (there is no chameleon-lint-bin, it uses lxml)
    chameleon-lint = False
    # XML (there is no xmllint-bin, it uses lxml)
    xmllint = True
    # scss-lint
    scsslint = True
    scsslint-bin = ${buildout:bin-directory}/scss-lint
    # TS
    tslint = True
    tslint-bin = ${buildout:directory}/bin/tslint
    tslint-exclude = ${:jscs-exclude}
    # Conventions
    clean-lines = True
    clean-lines-exclude = ${:jscs-exclude}
    # dependency-checker
    dependencychecker = True
    dependencychecker-bin = ${buildout:directory}/bin/dependencychecker
    # i18n
    find-untranslated = True
    i18ndude-bin = ${buildout:bin-directory}/i18ndude
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


Git hooks
=========

- pre-commit-hook
- pre-commit-return-status-codes
- pre-push-hook
- pre-push-return-status-codes

You can choose to activate git ``pre-commit-hook`` and/or ``pre-push-hook`` hooks.
You can make these hooks blocking (aborting) by setting ``return-status-codes``
to 'True'. You can tune the return code behavior differently from the default
for each hook, using ``pre-commit-return-status-codes`` and
``pre-push-return-status-codes``.

What works best for you is a matter of taste, and code base.

If you want to ensure that your working area is always clean on each commit,
and you'd like to abort the commit if anything untowards is found, you can
configure::

  [code-analysis]
  return-status-codes = True
  pre-commit-hook = True

If you're working in a large code base, which takes a long time to
parse, and your workflow is to use many small commits, you may be
annoyed by the pre-commit delay.  Or maybe you like to check in parts
of your work, while having other files hanging around in your working
tree which aren't cleaned up yet.

In that case you may want to disable pre-commit checks, and have a blocking
pre-push check instead::

  [code-analysis]
  return-status-codes = True
  pre-commit-hook = False
  pre-push-hook = True

Or maybe you want ``code-analysis`` by default to run unblocking, to
please Jenkins, but still want to have blocking checks on both pre-commit
and pre-push? Can do::

  [code-analysis]
  return-status-codes = False
  pre-commit-hook = True
  pre-commit-return-status-codes = True
  pre-push-hook = True
  pre-push-return-status-codes = True

Yeah I know, it's a contrived example, but it illustrates the relevant options.

Configuration ``overrides``
===========================

The options documented above configure code-analysis at the project level.
Sometimes developers may want to deviate from the project-level settings locally,
for example to make the git pre-commit hook block on violations, even when
the project-wide setting is to not abort the commit on violations.

If for example the project ``buildout.cfg`` reads::

  [code-analysis]
  overrides = code-analysis-overrides-acmecorp
  return-status-codes = False
  pre-commit-hook = True

But as a developer I'd rather have a blocking pre-push instead of a nonblocking
pre-commit, I can configure overrides in my
``.buildout/default.cfg`` configuration as follows::

  [code-analysis-overrides-acmecorp]
  return-status-codes = True
  pre-commit-hook = False
  pre-push-hook = True

This is especially handy to let users choose themselves whether they want
a pre-commit-hook or a pre-push-hook, and whether they want
to block on violations (so they don't have to amend commits) or whether they
want non-blocking checks (so they can have invalid files in their
working tree outside the commited c.q. pushed set of files). YMMV.

Note that if a project does not configure ``overrides`` at the project
level, you can as a dev still configure that in ``.buildout/default.cfg``::

  [code-analysis]
  overrides = code-analysis-overrides

  [code-analysis-overrides]
  return-status-codes = True

The recommended policy is to define an overrides name per project, so devs
can tune their overrides per project. Repo-specific override names only
make sense if the repo is really different (say much bigger) than typical.
Per-project override names would show up in a devs ``.buildout/default.cfg``
for example as follows::

  [code-analysis-overrides-plone]
  return-status-codes = True
  pre-commit-hook = True
  pre-push-hook = True

  [code-analysis-overrides-grok]
  <= code-analysis-overrides-plone

  [code-analysis-overrides-acmecorp]
  return-status-codes = True
  pre-commit-hook = False
  pre-push-hook = True


For projects that really really want to NOT offer this option to their
developers, there's the simple solution of blocking overrides in the
project ``buildout.cfg``::

  [code-analysis]
  overrides = False

It's recommended to actually talk to your fellow devs about which
overrides are not acceptable, instead of taking this nuclear option.
If a developer disagrees with the set of flake8 extensions you're validating
with, that's really a social issue, not something that can be solved in code.

A more suble way of controlling what local reconfigurations a dev is
allowed to perform is to configure the ``overrides-allowed`` whitelist
at the project level::

  [code-analysis]
  overrides-allowed = multiprocessing
                      return-status-codes
                      pre-commit-hook
                      pre-commit-return-status-codes
                      pre-push-hook
                      pre-push-return-status-codes

As a result, only the override options listed here will be taken from
the developer's local configuration, all other options will be taken
from the project buildout.cfg. Listing an empty ``overrides-allowed``
option allows all options to be overridden.

But of course, all of this runs on the developer's machine...

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

csslint::

    **/parts/code-analysis/scsslint.xml

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

**return-status-codes**
    If set to True, the ``bin/code-analysis`` script returns an error code
    that Continuous Integration servers (like Travis CI) can use to fail or
    pass a job, based on the code analysis output. Note that Jenkins usually
    does not need this option (this is better handled by the Jenkins
    Violations plugin). Note that this option does not have any effect on the
    other code analysis scripts. Default is ``False``.

    Note that this option can be overridden command-line by using the
    ``--return-status-codes`` or ``--no-return-status-codes`` command-line
    options.

    Note also that the pre-commit and post-commit hooks can be tuned to
    have a different status code behavior, if wanted, see below.

**pre-commit-hook**
    If set to True, a git pre-commit hook is installed that runs the code
    analysis before each commit. Default is ``True``.

**pre-commit-hook-return-status-codes**
    If set to True, if a pre-commit hook is run it will abort the commit
    if violations are found. Default value is the value configured for
    ``return-status-codes``.

**pre-push-hook**
    If set to True, a git pre-push hook is installed that runs the code
    analysis before it gets pushed to a remote. Default is ``False``.

**pre-push-hook-return-status-codes**
    If set to True, if a pre-push hook is run it will abort the push
    if violations are found. Default value is the value configured for
    ``return-status-codes``.

    Note that in general it will be advisable to set this option to ``True``
    so you will avoid pushing broken work. YMMV.

**multiprocessing**
    If set to ``True``, ``code-analysis`` will fork multiple processes and run
    all linters in parallel. This will dramatically increase speed on a
    multi-core system, specially when using ``code-analysis`` as pre-commit
    hook. Default is ``False``.

**jenkins**
    If set to True, the code analysis steps will
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


**flake8 Settings**

    Flake8 uses the following files to look for settings:

    - setup.cfg (recommended for Plone)
    - tox.ini
    - .flake8

.. code-block:: ini

    [flake8]
    exclude = bootstrap.py,boostrap-buildout.py,docs,*.egg
    max-complexity = 10
    max-line-length = 79

Look at `flake8 documentation <http://flake8.pycqa.org/en/latest/user/configuration.html#project-configuration>`_
 and it's plugins to see which options are available.

**check-manifest**
    If set to True, ``check-manifest`` will be run to check you MANIFEST.in
    file. Default is ``False``.

**check-manifest-directory**
    Default is ``.`` which means check the current package where you included
    code-analysis in buildout.

    EXPERIMENTAL: For project buildouts where you use several source
    packages you may want to enter multiple directories or use
    ``${buildout:develop}`` to include all your development packages.

**dependencychecker**
    If set to True, import statement analysis is run and verified
    against declared dependencies in setup.py. Default is ``False``.

**dependencychecker-bin**
    Set the path to a custom version of ``dependencychecker``.

**importchecker**
    If set to True, import statement analysis is run and unused
    imports are reported. Default is ``False``.

**importchecker-bin**
    Set the path to a custom version of ``importchecker``.

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

**chameleon-lint**
    If set to True, ChamleonLint code analysis is run. Default is ``False``.

    ChameleonLint uses ``lxml`` for xml parsing. There is no ``chameleon-lint-bin``.

    Note that you will want to activate either ``chameleon-lint`` or ``zpt-lint``,
    not both, since they will apply to the same set of file extensions (``.pt``,
    ``.cpt``, ``.zpt``). The ``zpt-lint`` parser uses the actual TAL expression engine
    to validate templates, and this will generally choke on the Chameleon extensions.
    The ``chameleon-lint`` parser on the other hand just checks that the template is
    valid XML basically.

**xmllint**
    If set to True, XMLLint code analysis is run. Default is ``False``.

    XMLLint uses ``lxml`` for xml parsing. There is no ``xmllint-bin``.

**clean-lines**
    If set to True, **any file** containing trailing spaces or tabs anywhere
    on the lines will cause a warning. Default is ``False``.

**clean-lines-exclude**
    Allows you to specify directories and/or files which you don't want to be
    checked. Default is none.

i18ndude, scsslint and zptlint support
--------------------------------------

To reduce the number of Zope/Plone direct dependencies, plone.recipe.codeanalysis no longer depends on `i18ndude`_ nor `SCSS Lint`_ nor `zptlint`_;
in order to use the following options you have to install them on your
system, see ``buildout.cfg`` for an example install.

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
    However, summaries will also be suppressed when ``jenkins`` is set to ``True.

**i18ndude-bin**
    Set the path to a custom version of `i18ndude`_.
    Default is none.

**scsslint**
    If set to True, `SCSS Lint`_ code analysis is run. Default is ``True``.

**scsslint-bin**
    Set the path to a custom version of `SCSS Lint`_.
    Default is none.

    Note that you'll typically install the gem ``scss_lint`` (with underscore)
    to get a bin file ``scss-lint`` (with a dash).

    If you have SCSS Lint installed in your system and path, you have nothing
    to do. To install SCSS Lint with Buildout, add the following section to
    your buildout and set scsslint-bin to
    ``{buildout:bin-directory}/scss-lint``:

.. code-block:: ini

    [rubygems]
    recipe = rubygemsrecipe
    gems = scss_lint

    Please note that due to some buildout weirdness this will break buildout
    on the first buildout run; a second buildout run will complete just fine.

**scsslint-configuration**

    SCSS Lint options can be configured, see `SCSS Lint`_ README.

**zptlint**
    If set to True, zptlint code analysis is run.
    Default is ``False``.
    To use this you will need to set the ``zptlint-bin`` option.

    Note that you will want to use either ``zptlint`` or ``chameleon-lint``, not both.

**zptlint-bin**
    Set the path to a custom version of `zptlint`_.
    Default is none.

**zptlint-exclude**
    Allows you to specify directories and/or files which you don't want to be
    checked. Default is none.

Self-tests for these extra linters are disabled by default.
To run a ``plone.recipe.codeanalysis`` self-test that covers these extra linters::

  TEST_ALL=true bin/test

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


Rubygems woes::

  Installing rubygems.
  rubygems: Extracting package to /app/plone.recipe.codeanalysis/parts
  ERROR:  While executing gem ... (Errno::EACCES)
  Permission denied @ rb_sysopen - /usr/lib/ruby/gems/2.3.0/specifications/default/bundler-1.16.1.gemspec
  rubygems: b''
  rubygems: Command failed with exit code 1: ['ruby', 'setup.rb', 'all', '--prefix=/app/plone.recipe.codeanalysis/parts/rubygems', '--no-rdoc', '--no-ri']
  While:
  Installing rubygems.
  Error: System error

Solution: run buildout again. Really.

Tests fail::

  Traceback (most recent call last):
  File "/app/plone.recipe.codeanalysis/plone/recipe/codeanalysis/__init__.py", line 18, in <module>
  import zc.buildout
  ModuleNotFoundError: No module named 'zc.buildout'

This is likely caused by https://github.com/pypa/pip/issues/4695.
Solution: run::

  bin/easy_install -U zc.buildout==2.11.0

before running ``bin/buildout``.


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
.. _`zptlint`: https://pypi.python.org/pypi/spirit.zptlint
.. _`i18ndude`: https://pypi.python.org/pypi/i18ndude
.. _`Unit testing framework documentation`: http://docs.python.org/2/library/unittest.html#deprecated-aliases
.. _`Mockup`: https://github.com/plone/mockup
.. _`jscs website`: https://www.npmjs.org/package/jscs
.. _`Plone's styleguide`: http://docs.plone.org/develop/styleguide/
.. _`extra configuration`: https://raw.githubusercontent.com/plone/plone.recipe.codeanalysis/master/.isort.cfg
