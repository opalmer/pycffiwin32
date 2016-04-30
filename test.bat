@ECHO OFF

:: A simple script for testing on Windows.  This does almost the same thing
:: that Travis and AppVeyor do.
:: NOTE: This script does not perform any kind of setup (virtualenv, build
:: tool chanin, etc)

ECHO =================================
ECHO pep8 pywincffi
ECHO =================================
pep8 pywincffi
IF %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%

ECHO =================================
ECHO pep8 tests
ECHO =================================
pep8 tests
IF %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%

ECHO =================================
ECHO pylint pywincffi
ECHO =================================
pylint pywincffi --reports no
IF %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%

ECHO =================================
ECHO pylint tests
ECHO =================================
pylint tests --reports no ^
    --disable missing-docstring,invalid-name,too-many-arguments ^
    --disable protected-access,no-self-use,unused-argument ^
    --disable too-few-public-methods
IF %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%

ECHO =================================
ECHO docs\make.bat html
ECHO =================================
sphinx-build -q -b html  -W -E -a -d docs/build/doctrees docs/source docs/build/html
make.bat html
IF %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%

ECHO =================================
ECHO docs\make.bat linkcheck
ECHO =================================
cd docs
make.bat html
echo %ERRORLEVEL%
IF %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%
cd ..


ECHO =================================
ECHO setup.py bdist_wheel
ECHO =================================
python setup.py bdist_wheel > NUL
IF %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%

ECHO =================================
ECHO nosetests -v tests
ECHO =================================
nosetests -sv tests
IF %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%
ECHO =================================

