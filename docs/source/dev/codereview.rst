Code Review
===========

This document gives a basic overview of code reviews for the pywincffi
projects.  All code reviews are performed on GitHub by using pull
requests.  Information about pull requests and how to submit one can be found
here:

    https://help.github.com/articles/using-pull-requests/

What branch should I use?
-------------------------

You should always base your code from the master branch unless you've been
told otherwise.  The master branch should be considered production ready and
other branches are usually for testing and development.

Pre-Merge Requirements
----------------------

The following are required before a pull request can normally be merged:

    * All conflicts with the target branch should be resolved.
    * The unittests, which are executed on AppVeyor, must pass
    * The style checks, which are executed in Travis, must pass
    * There should not be any major drops in coverage.  If there are it will
      be up to the reviewer(s) if the pull request should merge.
    * A brief description of the changes should be included in
      ``docs/changelog.rst`` under the 'latest' version.
    * Breaking changes should not occur on minor or micro versions unless the
      existing behavior can be preserved somehow.



