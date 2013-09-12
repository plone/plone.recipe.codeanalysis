1.0b3 (2013-09-12)
------------------

- Add return-status-codes option that allows to fail a CI-build on Travis.
  [timo]

- Make system wide installed csslint the default value for
  the csslint-bin option.
  [timo]


1.0b2 (2013-09-11)
------------------

- Deprecate 'csslint-quiet', 'csslint-ignore' and 'csslint-exclude-list'
  options; CSS Lint must be configured now using a '.csslintrc' file.
  'csslint-bin' option now defaults to ``bin/csslint``; documentation was
  updated (closes #20).
  [hvelarde]

- Implement removal of pre-commit hook (fixes #21).
  [hvelarde]


1.0b1 (2013-08-12)
------------------

- Workaround over JSHint limitations to avoid displaying warning messages as
  errors (closes #13).
  [hvelarde]

- Fix CSS Lint validation and implement new 'csslint-quiet' option.
  [hvelarde]

- Fix package distribution.
  [hvelarde]


1.0a1 (2013-08-04)
------------------

- Initial release.
  [timo]
