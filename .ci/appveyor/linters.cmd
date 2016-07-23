@ECHO OFF

%PYTHON%\\Scripts\\pep8.exe pywincffi tests
IF %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%

%PYTHON%\\Scripts\\pylint.exe pywincffi --reports no
IF %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%

%PYTHON%\\Scripts\\pylint.exe tests --reports no ^
    --disable missing-docstring,invalid-name,too-many-arguments ^
    --disable protected-access,no-self-use,unused-argument ^
    --disable too-few-public-methods
IF %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%
