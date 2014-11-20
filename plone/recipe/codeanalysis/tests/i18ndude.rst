i18ndude Code Analysis Test
==========================

i18ndude code analysis is included by default::

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
    >>> output = open('/tmp/output.txt', 'w').write(buildout_output_lower)

find-untranslated code analysis script has been created::

    >>> '/sample-buildout/bin/code-analysis-find-untranslated' in buildout_output_lower
    True
